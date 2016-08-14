import prompt_toolkit as pt
import prompt_toolkit.history as pthistory
from prompt_toolkit.token import Token
from prompt_toolkit.layout.lexers import PygmentsLexer

from gcloud import storage
import os.path
import click
import shlex

from .lexer import GCSShellLexer
from .commands import commands, ArgumentError
from .path import Path


class ClientWrapper:
    def __init__(self, client):
        self.client = client
        self.cwd = Path(self, '/')

    def __getattr__(self, name):
        return getattr(self.client, name)


def get_prompt(path):
    return "gs://{} > ".format(path)


def print_error(s):
    click.secho(str(s), err=True, fg='red', bold=True)


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

    if command in commands:
        try:
            commands[command](command, args, client)
        except ArgumentError as e:
        #except Exception as e:
            print_error(command + ": " + str(e))
    else:
        print_error(command + ": command not found")


def get_rprompt(project):
    return lambda cli: [
        (Token.Rprompt, project),
        (Token, ' ')
    ]


def run():
    history = pthistory.FileHistory(
        os.path.join(os.path.expanduser('~'), '.gcloudstorageclihistory'))

    client = ClientWrapper(storage.Client())

    while True:
        try:
            text = pt.prompt(get_prompt(client.cwd.get_path()),
                             history=history,
                             lexer=PygmentsLexer(GCSShellLexer),
                             get_rprompt_tokens=get_rprompt(client.project))
            execute_command(text, client)
        except EOFError:
            break
        except KeyboardInterrupt:
            continue

    print("Bye!")
