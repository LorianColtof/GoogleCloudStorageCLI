from pygments.lexer import RegexLexer
from pygments.token import Name, String, Text
from .commands import commands


class GCSShellLexer(RegexLexer):
    name = 'Google Cloud Storage shell lexer'
    tokens = {
        'root':
        [
            (r'\b({})\s*\b'.format('|'.join(commands.keys())), Name.Builtin),
            (r'(?s)\$?"(\\\\|\\[0-7]+|\\.|[^"\\])*"', String.Double),
            (r"(?s)\$?'(\\\\|\\[0-7]+|\\.|[^'\\])*'", String.Single),
            (r"\w+", Text)
        ]
    }
