"""XML: DEFAULT Parsing Style

This style attempts to follow all the XML rules and gathers all the
information in an xml file. This includes all the extra spaces, new
lines and tab characters the file might contain.

"""

from lexor import init, load_aux


INFO = init(
    version=(0, 0, 1, 'final', 0),
    lang='xml',
    type='parser',
    description='Parse XML files using all the valid rules.',
    url='http://jmlopez-rod.github.io/lexor-lang/xml-parser-default',
    author='Manuel Lopez',
    author_email='jmlopez.rod@gmail.com',
    license='BSD License',
    path=__file__
)
MOD = load_aux(INFO)
MAPPING = {
    '__default__': (
        '<&', [
            MOD['element'].ElementNP,
            MOD['cdata'].CDataNP,
            MOD['doctype'].DocumentTypeNP,
            MOD['comment'].CommentNP,
            MOD['pi'].ProcessingInstructionNP,
            MOD['entity'].EntityNP,
        ]),
}
