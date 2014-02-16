"""XML: DEFAULT parser ELEMENT test

Testing suite to parse xml element in the default style.

"""

from lexor.command.test import nose_msg_explanations


def test_element():
    """xml.parser.default.element: MSG_EXPLANATION """
    nose_msg_explanations(
        'xml', 'parser', 'default', 'element'
    )
