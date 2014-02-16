"""XML: DEFAULT parser COMMENT test

Testing suite to parse xml comment in the default style.

"""

from lexor.command.test import nose_msg_explanations


def test_comment():
    """xml.parser.default.comment: MSG_EXPLANATION """
    nose_msg_explanations(
        'xml', 'parser', 'default', 'comment'
    )
