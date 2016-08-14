from path import Path
import click


def change_dir(command, args, client):
    if len(args) == 0:
        raise ArgumentError('No directory specified')

    arg = args[0]
    new_path = Path(client, arg)
    if not new_path.exists():
        raise ArgumentError('No such directory: ' + arg)
    if not new_path.is_directory():
        raise ArgumentError('Not a directory: ' + arg)

    client.cwd = new_path


def list_blobs(blobs):
    for (obj_name, is_dir) in sorted(blobs):
        click.secho(obj_name, nl=True, bold=(True if is_dir else False),
                    fg=('blue' if is_dir else 'yellow'))
    print("")


def list_contents(command, args, client):
    if client.cwd.is_root():
        result = ((b.name, True) for b in client.list_buckets())
    else:
        if client.cwd.is_bucket_root():
            blobs = client.cwd.get_bucket().list_blobs()
            prefix_length = 0
        else:
            blobs = client.cwd.get_bucket().list_blobs(
                prefix=client.cwd.blob + '/')
            prefix_length = len(client.cwd.blob) + 1

        result = set()
        for b in blobs:
            name_split = b.name[prefix_length:].split('/')
            name = name_split[0]
            if name == "":
                continue
            if len(name_split) > 1:
                result.add((name, True))
            else:
                result.add((name, False))

    list_blobs(result)


def list_buckets(command, args, client):
    result = ((b.name, True) for b in client.list_buckets())
    list_blobs(result)


def print_blob_contents(command, args, client):
    if len(args) < 1:
        raise ArgumentError('No file specified')

    arg = args[0]
    path = Path(client, arg)
    if path.is_directory():
        raise ArgumentError('Is a directory: ' + arg)
    elif not path.exists():
        raise ArgumentError('No such file: ' + arg)

    contents_raw = path.get_blob().download_as_string()
    contents = None
    try:
        contents = contents_raw.decode('utf-8')
    except UnicodeDecodeError:
        if click.confirm(
                '''Failed to decode file as UTF-8. It might not be a text file.
Still display the contents?'''):
            contents = contents_raw.decode('utf-8', 'replace')

    if contents is not None:
        print(contents)


def exit(command, args, client):
    raise EOFError()


class ArgumentError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


def not_implemented(command, args, client):
    raise NotImplementedError("command not implemented")

commands = {
    'cd': change_dir,
    'changeproject': not_implemented,
    'ls': list_contents,
    'lsbucket': list_buckets,
    'lb': not_implemented,
    'mv': not_implemented,
    'cp': not_implemented,
    'cat': print_blob_contents,
    'rm': not_implemented,
    'removebucket': not_implemented,
    'rb': not_implemented,
    'du': not_implemented,
    'hash': not_implemented,
    'mkdir': not_implemented,
    'makebucket': not_implemented,
    'mb': not_implemented,
    'rsync': not_implemented,
    'stat': not_implemented,
    'exit': exit
}
