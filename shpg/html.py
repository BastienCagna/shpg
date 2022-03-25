import os.path as op
import typing
import imghdr
from uuid import uuid4


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
        self.children = []

        if not self.orphan:
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
