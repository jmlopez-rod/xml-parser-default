"""XML: DEFAULT parser PI test

Testing suite to parse xml pi in the default style.

"""

from lexor.command.test import nose_msg_explanations


def test_pi():
    """xml.parser.default.pi: MSG_EXPLANATION """
    nose_msg_explanations(
        'xml', 'parser', 'default', 'pi'
    )
