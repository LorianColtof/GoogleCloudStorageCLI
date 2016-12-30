from pygments.lexer import RegexLexer
from pygments.token import Name, String, Text
from .commands import commands_dict


class GCSShellLexer(RegexLexer):
    name = 'Google Cloud Storage shell lexer'
    tokens = {
        'root':
        [
            (r'\b({})\s*\b'.format('|'.join(commands_dict.keys())),
             Name.Builtin),
            (r'(?s)\$?"(\\\\|\\[0-7]+|\\.|[^"\\])*"', String.Double),
            (r"(?s)\$?'(\\\\|\\[0-7]+|\\.|[^'\\])*'", String.Single),
            (r"\w+", Text)
        ]
    }
