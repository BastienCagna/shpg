from enum import Enum
from genericpath import exists
from logging.handlers import WatchedFileHandler
from operator import index
import os.path as op
from os import makedirs
from posixpath import relpath
import shutil
import typing
import imghdr
from uuid import uuid4

from prompt_toolkit import HTML



INDEX_DIR_SUFFIX = "_index"
CONTENT_DIRNAME = "content"
PAGES_DIRNAME = "pages"
DEFAULT_TITLE = "Untitled page"


class HTMLProvider:
    def __init__(self, id:str=None) -> None:
        self.id = id or uuid4().hex[-8:]

    def to_html(self) -> str:
        raise NotImplementedError()


class HTMLTag(HTMLProvider):
    def __init__(self, tagname: str, children: 'list[HTMLTag]' = [], attributes: dict= None, orphan=False) -> None:
        super().__init__(id=tagname + "_" + uuid4().hex[-8:])
        self.tagname = tagname
        self.attributes = attributes or {}
        self.orphan = orphan

        if not self.orphan:
            self.children = []
            for child in children:
                self.append(child)
                
    def append(self, child: 'HTMLTag') -> None:
        if self.orphan:
            raise RuntimeError("Cannot add item to {} as it is an orphan tag".format(self.tagname))
        if isinstance(child, HTMLProvider):
            self.children.append(child)
        elif isinstance(child, str):
            if op.exists(child) and imghdr.what(child):
                self.children.append(Image(child))
            else:
                self.children.append(child)
        else:
            raise ValueError("Invalid child.")

    def inner_html(self) -> str:
        if self.orphan:
            return None
        inner = ""
        for child in self.children:
            if isinstance(child, HTMLProvider):
                inner += child.to_html()
            elif isinstance(child, str):
                inner += child
            else:
                raise ValueError(
                    "Unrecognize child type. Cannot generate HTML script.")
        return inner

    def to_html(self) -> str:
        attributes = ""
        for key, value in self.attributes.items():
            attributes += ' {}="{}"'.format(key, value)
        if not self.orphan:
            inner = self.inner_html()
            return '<{} {}>{}</{}>'.format(self.tagname, attributes, inner, self.tagname)
        else:
            return '<{} {} />'.format(self.tagname, attributes)


# class URL:
#     def __init__(self, filepath: str) -> None:
#         self.path = filepath

#     def set_local(self)


class Heading1(HTMLTag):
    def __init__(self, text: str) -> None:
        super().__init__('h1', [text])
class Heading2(HTMLTag):
    def __init__(self, text: str) -> None:
        super().__init__('h2', [text])
class Heading3(HTMLTag):
    def __init__(self, text: str) -> None:
        super().__init__('h3', [text])
class Heading4(HTMLTag):
    def __init__(self, text: str) -> None:
        super().__init__('h4', [text])
class Heading5(HTMLTag):
    def __init__(self, text: str) -> None:
        super().__init__('h5', [text])
class Heading6(HTMLTag):
    def __init__(self, text: str) -> None:
        super().__init__('h6', [text])


class Paragraph(HTMLTag):
    def __init__(self, text: str) -> None:
        super().__init__('p', [text])


class Link(HTMLTag):
    def __init__(self, url: str) -> None:
        super().__init__('a')
        self.attributes['href'] = url


class Image(HTMLTag):
    def __init__(self, img_path: str) -> None:
        super().__init__('img', attributes={'src': img_path}, orphan=True)

class Div(HTMLTag):
    def __init__(self, *children) -> None:
        super().__init__('div', children)


class Section(HTMLTag):
    def __init__(self, *children) -> None:
        super().__init__('section', children)


class DictVTable(HTMLTag):
    def __init__(self, data: str) -> None:
        super().__init__('table')
        self.data = data

    def inner_html(self) -> str:
        inner = ''
        for k, v in self.data.items():
            inner += '<tr><th>{}</th><td>{}</td>'.format(k, v)
        return inner


def _generate_submenu(items:dict, depth=0):
    inner = '<ul>'
    for label, item in items.items():
        inner += '<li>' + create_tmp_tag(TempTagType.LINK, id=item.id, label=label)
        if isinstance(item, dict):
            inner += _generate_submenu(item, depth+1)
        inner += '</li>'
    return inner + '</ul>'

class HMenu(Div):
    def __init__(self, items: dict=None) -> None:
        super().__init__()
        self.attributes['class'] = 'hmenu'
        self.items = items or {}
        self.children = []

    def append(self, k, item):
        self.items[k] = item

    def inner_html(self) -> str:
        return _generate_submenu(self.items)

class SiteMap(Div):
    def __init__(self, links_dict:dict) -> None:
        super().__init__()
        self.attributes['class'] = 'sitemap'
        self.links = links_dict or {}

    def inner_html(self) -> str:
        html = ''
        for title, links in self.links.items():
            html += '<div><h4>' + title + '</h4>'
            if isinstance(links, dict):
                html += '<ul>'
                for label, item in links.items():
                    html += '<li>' + create_tmp_tag(TempTagType.LINK, id=item.id, label=label) + '</li>'
                html += '</ul>'
            else:
                html += links.to_html()
            html += "</div>"
        return html

class Header(Div):
    def __init__(self, title:str, menu_dict: dict=None) -> None:
        super().__init__()
        self.attributes['class'] = "header"
        self.append(Heading1(title))
        if menu_dict:
            self.append(HMenu(menu_dict))

class Footer(Div):
    def __init__(self, message:str=None, links_dict: dict=None) -> None:
        super().__init__()
        self.attributes['class'] = "footer"
        if message:
            self.append(message)
        if links_dict:
            self.append(SiteMap(links_dict))
        self.append(Paragraph("Generated with Static Page Generator."))

import re
from os import listdir
import json

def find_urls(html: str, attributes=['src', 'href']) -> list[str]:
    # """ Return URLs included in a string
    
    #     Source: https://www.geeksforgeeks.org/python-check-url-string/
    # """
    # regex = r"(?i)\b((/|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    # url = re.findall(regex,string)      
    # return [x[0] for x in url]
    urls = []
    for attr in attributes:
        parts = html.split(attr + '=')
        for p in parts[1:]:
            p = p.strip()
            if p[0] == "'":
                urls.append(p.split("'")[1])
            elif p[0] == '"':
                urls.append(p.split('"')[1])
            else:
                pass
    return urls


def find_content_urls(string: str) -> list[str]:
    #return list(filter(lambda url: op.splitext(url)[1] in valid_ext, find_urls(string)))
    results = []
    for url in find_urls(string):
        if url.startswith('http://') or url.startswith('https://'):
            continue
        results.append(url)
    return results

def make_script_portable(html:str, abs_target_path: str, rel_target_path: str) -> str:
    files = find_content_urls(html)

    for f in set(files):
        original_dir, fname = op.split(f)
        # If the file is not from the target directory
        abs_original_dir = op.abspath(original_dir)
        if abs_original_dir != abs_target_path and not abs_original_dir.startswith(abs_target_path):
            # If a file with same name is present, increment the filename
            orig_fname = fname
            name, ext = op.splitext(orig_fname)
            i = 0
            while fname in listdir(abs_target_path):
                fname = "{}{:d}{}".format(name, i, ext)
                i += 1
            new_abs_path = op.join(abs_target_path, fname)
            new_rel_path = op.join(rel_target_path, fname)

            if op.exists(f):
                shutil.copy(f, new_abs_path)

            # Then, replace filename occurance in the html script
            html = html.replace(f, new_rel_path)
        
    return html

def create_index_dir(fname: str, parent_dir:str):
    fbasename, _ = op.splitext(fname)
    index_dir = op.join(parent_dir, fbasename + INDEX_DIR_SUFFIX)
    if op.exists(index_dir):
        shutil.rmtree(index_dir)
    makedirs(index_dir, exist_ok=True)
    return index_dir


TEMP_TAG_START_DELIMITER = "$[$"
TEMP_TAG_END_DELIMITER = "$]$"
class TempTagType(Enum):
    UNKNOWN = 0
    LINK = 1

def create_tmp_tag(type:TempTagType, **data):
    data['_tag_type'] = type.value
    data_str = json.dumps(data)
    return "{}{}{}".format(TEMP_TAG_START_DELIMITER, data_str, TEMP_TAG_END_DELIMITER)


def generate_tag(serialized_tmp_tag:str, items:list[HTMLProvider]) -> str:
    data = json.loads(serialized_tmp_tag.split(TEMP_TAG_START_DELIMITER)[-1])
    t = TempTagType(data['_tag_type'])

    if t == TempTagType.LINK:
        link = None
        for item in items:
            if item.id == data['id']:
                if isinstance(item, Page):
                    link = item.filename
                else:
                    raise NotImplementedError("If HTML tag of a page, it should link as an anchor")
                break
        if not link:
            raise ValueError("Cannot find item {}".format(data['id']))
        return '<a href="{}">{}</a>'.format(link, data['label'])
    raise NotImplementedError("Unknown tak type or not implemented decoding.")

def _decode_first_temporary_tag(html: str, items: list[HTMLProvider]) -> str:
    parts = html.split(TEMP_TAG_END_DELIMITER)
    if len(parts) > 1:
        ppart = parts[0].split(TEMP_TAG_START_DELIMITER)
        out = ''.join(ppart[:-1])
        if len(ppart) > 1:
            out+= generate_tag(ppart[-1], items)
        else:
            raise ValueError('Wrong pre-formatted HTML: Failed to find starting bound of temporary tag.')
        return out + TEMP_TAG_END_DELIMITER.join(parts[1:])
    return None


def decode_tmp_tags(html: str, items: list[HTMLProvider]) -> str:
    new_html = _decode_first_temporary_tag(html, items)
    while new_html:
        html = new_html
        new_html = _decode_first_temporary_tag(html, items)
    return html

def get_chidrens_tags(tag:HTMLTag) -> list[HTMLTag]:
    if isinstance(tag, HTMLTag):
        tags = [tag]
        for t in tag.children:
            tags.extend(get_chidrens_tags(t))
        return tags
    return []

class StyleSheets(Enum):
    DEFAULT = 'default.css'

class Page(HTMLProvider):
    def __init__(self, title: str = DEFAULT_TITLE, stylesheet:'str|StyleSheets'=StyleSheets.DEFAULT) -> None:
        super().__init__()
        self.title = title
        self.content = Div()
        self.content.attributes['class'] = "page"
        self.stylesheet = stylesheet

        # self.path_from_root = None
        # self.path_to_root = None
        self.filename = None

    def link(self, label:str) -> str:
        return create_tmp_tag(TempTagType.LINK, id=self.id, label=label)

    def to_html(self, data: dict = {}) -> str:
        if isinstance(self.stylesheet, StyleSheets):
            style_url = op.realpath(op.join(op.split(__file__)[0], 'style', self.stylesheet.value))
        else:
            if not op.exists(self.stylesheet):
                raise IOError("Cannot find custom stylesheet: {}".format(self.stylesheet))
            style_url = self.stylesheet

        body = self.content.to_html()
        html = '<html><head><title>{}</title><link rel="stylesheet" href="{}"></head><body>{}</body>'.format(self.title, style_url, body)
        # TODO: process template to input data
        return html

    # def set_filename(self, filename, root:str=None):
    #     self.filename = filename
        # self.root = root

    def get_relative_path_to(self, filename):
        if not self.filename:
            raise ValueError("Page filename should be set before requesting relative paths")
        return op.relpath(filename, op.split(self.filename)[0])
        # if not root:
        #     self.path_from_root = './'
        #     self.path_to_root = './'
        # else:
        #     self.path_from_root = relpath(filename, op.abspath(op.split(root)[0]))
        #     self.path_to_root = relpath(root, op.abspath(op.split(filename)[0]))

    def save(self, filename: str=None, portable = False, index_dir:str=None, items:list[HTMLProvider]=None):
        if filename:
            self.filename = filename
        html = self.to_html()

        # Decode temporary tags
        if not items:
            items = get_chidrens_tags(self.content)
        html = decode_tmp_tags(html, items)

        if portable:
            parent_dir, fname = op.split(filename)
            if not index_dir:
                index_dir = create_index_dir(fname, parent_dir)
            content_dir = op.join(index_dir, CONTENT_DIRNAME)
            makedirs(content_dir, exist_ok=True)
            make_script_portable(html, op.abspath(content_dir), op.relpath(content_dir, parent_dir))

        with open(filename, 'w') as f:
            f.write(html)


class Book:
    def __init__(self, title: str = DEFAULT_TITLE, stylesheet:'str|StyleSheets'=StyleSheets.DEFAULT) -> None:
        self.title = title
        self.stylesheet = stylesheet
        self.index = Page(title, stylesheet)
        self.pages: list[Page] = []

    def save(self, filename: str, portable = False, index_dir:str=None):
        parent_dir, fname = op.split(filename)
        if not index_dir:
            index_dir = create_index_dir(fname, parent_dir)
        content_dir = op.join(index_dir, CONTENT_DIRNAME)
        makedirs(content_dir)
        pages_dir = op.join(index_dir, PAGES_DIRNAME)
        makedirs(pages_dir)

        items: list[HTMLProvider] = [self.index] + get_chidrens_tags(self.index.content)
        for page in self.pages:
            page.filename = op.join(pages_dir, page.title.replace(' ', '_') + ".html")
            items.append(page)
            items.extend(get_chidrens_tags(page.content))
        self.index.filename = filename

        for page in self.pages:
            page.save(page.filename, portable, index_dir, items)
        self.index.save(self.index.filename, portable, index_dir, items)