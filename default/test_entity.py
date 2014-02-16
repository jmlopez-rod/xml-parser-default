"""XML: DEFAULT parser ENTITY test

Testing suite to parse xml entity in the default style.

"""

from lexor.command.test import nose_msg_explanations


def test_entity():
    """xml.parser.default.entity: MSG_EXPLANATION """
    nose_msg_explanations(
        'xml', 'parser', 'default', 'entity'
    )
