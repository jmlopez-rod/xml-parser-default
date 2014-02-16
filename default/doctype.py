"""XML: DOCTYPE NodeParser

Processes the document type. Warns if DOCTYPE is not in uppercase.

See: http://www.w3.org/TR/REC-xml/#dtd

"""

from lexor.core.parser import NodeParser
from lexor.core.elements import DocumentType


class DocumentTypeNP(NodeParser):
    """Obtains the content enclosed within `<!DOCTYPE` and `>`. """

    def make_node(self):
        parser = self.parser
        caret = parser.caret
        if parser.text[caret:caret+9].upper() != '<!DOCTYPE':
            return None
        char = parser.text[caret+9:caret+10]
        if char not in ' \t\n\r\f\v':
            return None
        if not parser.text[caret:caret+9].isupper():
            self.msg('E101', parser.pos, [parser.text[caret+2:caret+9]])
        index = parser.text.find('>', caret+10)
        if index == -1:
            self.msg('E100', parser.pos)
            parser.update(parser.end)
            return DocumentType(parser.text[caret+10:parser.end])
        parser.update(index+1)
        return DocumentType(parser.text[caret+10:index])


MSG = {
    'E100': '`>` not found',
    'E101': 'found `{0}` instead of `DOCTYPE`'
}
MSG_EXPLANATION = [
    """
    - A `doctype` element starts with `<!DOCTYPE` and is terminated
      by `>`. Note that the character sequence 'DOCTYPE' must be in
      uppercase letters: see <http://www.w3.org/TR/REC-xml/#dtd>.

    Okay: <!DOCTYPE html>

    E100: <!DOCTYPE html
    E101: <!doctype html>
""",
]
