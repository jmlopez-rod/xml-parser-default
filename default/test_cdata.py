"""XML: DEFAULT parser CDATA test

Testing suite to parse xml cdata in the default style.

"""

from lexor.command.test import nose_msg_explanations


def test_cdata():
    """xml.parser.default.cdata: MSG_EXPLANATION """
    nose_msg_explanations(
        'xml', 'parser', 'default', 'cdata'
    )
