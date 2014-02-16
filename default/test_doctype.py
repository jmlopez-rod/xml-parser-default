"""XML: DEFAULT parser DOCTYPE test

Testing suite to parse xml doctype in the default style.

"""

from lexor.command.test import nose_msg_explanations


def test_doctype():
    """xml.parser.default.doctype: MSG_EXPLANATION """
    nose_msg_explanations(
        'xml', 'parser', 'default', 'doctype'
    )
