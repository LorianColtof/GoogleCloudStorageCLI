import prompt_toolkit as pt
import prompt_toolkit.history as pthistory
from prompt_toolkit.token import Token
from prompt_toolkit.layout.lexers import PygmentsLexer

from prompt_toolkit.styles import style_from_pygments
from pygments.styles.default import DefaultStyle

from gcloud import storage
import os.path
import click
import shlex

from .lexer import GCSShellLexer
from .path import Path
from .commands import commands_dict, ArgumentError

style = style_from_pygments(
    DefaultStyle, {
        Token.RPrompt: '#7baec0 bold',
    })


class ClientWrapper:
    def __init__(self, client):
        self.client = client
        self.cwd = Path(self, '/')

    def __getattr__(self, name):
        return getattr(self.client, name)


def get_prompt(path):
    return "gs://{} > ".format(path)


def print_error(s, bold=True):
    click.secho(str(s), err=True, fg='red', bold=bold)


def execute_command(input_line, client):
    try:
        tokens = shlex.split(input_line)
    except ValueError as e:
        print_error("Lexical error: " + str(e))
        return

    if len(tokens) == 0:
        return

    command = tokens[0]
    args = tokens[1:]

    if command in commands_dict:
        try:
            commands_dict[command](command, args, client)
        except ArgumentError as e:
            print_error(command + ": " + str(e))
    else:
        print_error(command + ": command not found")


def get_rprompt(project):
    return lambda cli: [
        (Token.RPrompt, project),
        (Token, ' ')
    ]


def exit_client_error(exception=None):
    print_error("Could not initialize GCloud client")
    if exception is not None:
        print("\nThe error message was:")
        print_error("  " + str(exception), bold=False)

    print("""
There are two likely reasons for this:
1. An an authentication error occurred.
   If you did not authenticate yet, run:

     $ gcloud auth login

2. The default project has not been set.
   To set the default project, run:

     $ gcloud config set project PROJECT_ID

""")
    exit()


def run():
    history = pthistory.FileHistory(
        os.path.join(os.path.expanduser('~'), '.gcloudstorageclihistory'))

    try:
        client = ClientWrapper(storage.Client())
    except EnvironmentError:
        exit_client_error()
    except Exception as ex:
        exit_client_error(ex)

    while True:
        try:
            text = pt.prompt(get_prompt(client.cwd.get_path()),
                             lexer=PygmentsLexer(GCSShellLexer),
                             style=style, history=history,
                             get_rprompt_tokens=get_rprompt(client.project))
            execute_command(text, client)
        except EOFError:
            break
        except KeyboardInterrupt:
            continue

    print("Bye!")
