"""XML: Element NodeParser

An XML element is a `Node` object that is allowed to have child nodes
and attributes. For instance,

    <tagname att1="val1" att2="val2">
        ...
    </tagname>

is an element of name 'tagname' and has attributes `att1` and `att2`.
All values in xml must be enclosed within quotes.

"""

import re
from lexor.core.parser import NodeParser
from lexor.core.elements import Element

RE = re.compile(r'.*?[ \t\n\r\f\v/>]')
RE_NOSPACE = re.compile(r"\s*")
RE_NEXT = re.compile(r'.*?[ \t\n\r\f\v/>=]')


class ElementNP(NodeParser):
    """Parses xml elements """

    def is_element(self, parser):
        """Check to see if the parser's caret is positioned in an
        element and return the index where the opening tag ends. """
        caret = parser.caret
        if parser.text[caret:caret+1] != '<':
            return None
        char = parser.text[caret+1:caret+2]
        if char.isalpha() or char in [":", "_"]:
            endindex = parser.text.find('>', caret+1)
            if endindex == -1:
                return None
            start = parser.text.find('<', caret+1)
            if start != -1 and start < endindex:
                self.msg('E100', parser.pos, parser.compute(start))
                return None
        else:
            return None
        return endindex

    def make_node(self):
        parser = self.parser
        caret = parser.caret
        endindex = self.is_element(parser)
        if endindex is None:
            return None
        pos = parser.copy_pos()
        match = RE.search(parser.text, caret+1)
        node = Element(parser.text[parser.caret+1:match.end(0)-1])
        parser.update(match.end(0)-1)
        if parser.text[parser.caret] is '>':
            parser.update(parser.caret+1)
        elif parser.text[parser.caret] is '/':
            parser.update(endindex+1)
            return [node]  # Closed element no need to add position
        else:
            if self.read_attributes(parser, node, endindex):
                return [node]
        node.pos = pos
        return node

    def close(self, node):
        """Return the position where the element was closed. """
        parser = self.parser
        caret = parser.caret
        if parser.text[caret] != '<':
            return None
        if parser.text[caret+1:caret+2] == '/':
            index = parser.text.find('>', caret+2)
            if index == -1:
                return None
            if parser.text[caret+2:index] == node.name:
                pos = parser.copy_pos()
                parser.update(index+1)
                return pos
        return None

    def is_empty(self, parser, index, end):
        """Checks to see if the parser has reached '/'. """
        if parser.text[index] == '/':
            parser.update(end+1)
            if end - index > 1:
                self.msg('E120', parser.compute(index))
            return True
        return False

    def read_prop(self, parser, node, end):
        """Return [prop, prop_index, implied, empty]. """
        prop = None
        prop_index = None
        match = RE_NOSPACE.search(parser.text, parser.caret, end)
        if self.is_empty(parser, match.end(0), end):
            return prop, prop_index, False, True
        if parser.text[match.end(0)] == '>':
            parser.update(end+1)
            return prop, prop_index, False, False
        prop_index = match.end(0)
        if prop_index - parser.caret == 0 and node.attlen > 0:
            self.msg('E130', parser.pos)
        match = RE_NEXT.search(parser.text, prop_index, end)
        if match is None:
            prop = parser.text[prop_index:end]
            parser.update(end+1)
            return prop, prop_index, True, False
        prop = parser.text[prop_index:match.end(0)-1]
        if self.is_empty(parser, match.end(0)-1, end):
            return prop, prop_index, True, True
        if parser.text[match.end(0)-1] == '=':
            parser.update(match.end(0))
            return prop, prop_index, False, False
        match = RE_NOSPACE.search(parser.text, match.end(0), end)
        if parser.text[match.end(0)] == '=':
            implied = False
            parser.update(match.end(0)+1)
        else:
            implied = True
            parser.update(match.end(0)-1)
        return prop, prop_index, implied, False

    def read_val(self, parser, end):
        """Return the attribute value. """
        match = RE_NOSPACE.search(parser.text, parser.caret, end)
        if self.is_empty(parser, match.end(0), end):
            return ''
        if parser.text[match.end(0)] == '>':
            parser.update(end+1)
            return ''
        val_index = match.end(0)
        if parser.text[val_index] in ["'", '"']:
            quote = parser.text[val_index]
            index = parser.text.find(quote, val_index+1, end)
            if index == -1:
                self.msg('E132', parser.pos, parser.compute(end))
                parser.update(end+1)
                return parser.text[val_index+1:end]
            parser.update(index+1)
            return parser.text[val_index+1:index]
        else:
            pos = parser.copy_pos()
            self.msg('E131', parser.compute(val_index))
            match = RE.search(parser.text, val_index, end)
            if match is None:
                parser.update(end+1)
                return parser.text[val_index:end]
            if parser.text[match.end(0)-1] == '/':
                self.msg('E140', pos)
                parser.update(match.end(0)-1)
            else:
                parser.update(match.end(0)-1)
            return parser.text[val_index:match.end(0)-1]

    def read_attributes(self, parser, node, end):
        """Parses the string

            parser.text[parser.caret:end]

        and writes the information in node. XML is very strict about
        attributes. They must be in the form

            att1="val1" att2="val2" ...

        This function returns True if the Element is empty, that is, if
        the opening tag ends with `/`. """
        while parser.caret < end:
            prop, prop_index, implied, empty = self.read_prop(
                parser, node, end
            )
            if prop is None:
                return empty
            if prop in node:
                self.msg('E150', parser.compute(prop_index), [prop])
            if implied is True:
                self.msg('E151', parser.compute(prop_index))
                node[prop] = ""
                if empty is True:
                    return empty
            else:
                val = self.read_val(parser, end)
                node[prop] = val
        parser.update(end+1)


MSG = {
    'E100': 'element discarded due to `<` at {0}:{1:2}',
    'E120': '`/` not immediately followed by `>`',
    'E130': 'no space between attributes',
    'E131': 'attribute values must be wrapped in quotes',
    'E132': 'assuming quoted attribute to close at {0}:{1:2}',
    'E140': '`/` found in unquoted attribute value',
    'E150': 'attribute name "{0}" has already been declared',
    'E151': 'XML does not support implied attributes.'
}
MSG_EXPLANATION = [
    """
    - The opening tag of an element cannot contain `<`. This means
      that attributes cannot contain `<` in them.

    Okay: <apple att1="val1"></apple>

    E100: <apple att1="a < b"></apple>
""",
    """
    - An empty Element opening tag must end with `/>`. Anything in
      between the characters `/` and `>` will be ignored.

    - When using empty tags be careful to not use its closing tag.
      Otherwise you will be getting the stray tag error.

    Okay: <img href="/path/to/image.png"/>
    Okay: <p>starting a new paragraph</p>

    E120: <img href="/path/to/image.png"/  >
    E120: An empty element: <p / >A stray tag: </p>
""",
    """
    - Attributes must be quoted and need to be separated by one space.

    - Finish the quoted attribute.

    - Do not repeat attributes since the values will only get
      overwritten.

    Okay: <tag att1="val1" att2="val2">content</tag>
    Okay: <tag att1='1' att2='2'></tag>

    E130: <tag att1="val1"att2="val2">content</tag>
    E131: <tag att1=1 att2=2></tag>
    E132: <tag att1="num></tag>
    E150: <tag att1='1' att1='2'></tag>
""",
    """
    - Quote your attribute values. This will get rid of E140.
    
    - Give a value to your attributes. There are no implied
      attributes in XML.

    Okay: <img href="path/to/image.png" />
    Okay: <tag att1="" att2="val2">content</tag>

    E140: <img href=path/to/image.png />
    E151: <tag att1 att2="val2">content</tag>

""",
]


