from .html import *
from .page import create_tmp_tag, TempTagType, Page, StyleSheets
import typing


class SimpleHeader(Div):
    def __init__(self, title:str, menu_dict: dict=None) -> None:
        super().__init__()
        self.attributes['class'] = "header"
        self.append(Heading1(title))
        if menu_dict:
            self.append(SimpleHMenu(menu_dict))

class SimpleFooter(Div):
    def __init__(self, message:str=None, links_dict: dict=None) -> None:
        super().__init__()
        self.attributes['class'] = "footer"
        if message:
            self.append(message)
        if links_dict:
            self.append(SimpleSiteMap(links_dict))
        self.append(Paragraph('Generated with <a target="_blank" href="https://github.com/BastienCagna/shpg">Static HTML Page Generator</a>.'))

class SimpleDictVTable(HTMLTag):
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

class SimpleHMenu(Div):
    def __init__(self, items: dict=None) -> None:
        super().__init__()
        self.attributes['class'] = 'hmenu'
        self.items = items or {}
        self.children = []

    def append(self, k, item):
        self.items[k] = item

    def inner_html(self) -> str:
        return _generate_submenu(self.items)

class SimpleSiteMap(Div):
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

class SimplePage(Page):
    def __init__(self, title: str = ..., stylesheet: 'str|StyleSheets' = ...) -> None:
        super().__init__(title, stylesheet)
        self.content = Div()
        self.content.attributes['class'] = "simple-maincontent"
        self.header = SimpleHeader(title=title)
        self.footer = SimpleFooter()

    def to_html(self, data: dict = ...) -> str:
        memo = self.content
        self.content = [self.header, self.content, self.footer]
        html = super().to_html(data)
        self.content = memo
        return html