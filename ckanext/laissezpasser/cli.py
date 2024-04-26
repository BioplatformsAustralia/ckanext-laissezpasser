import click


@click.group(short_help="laissezpasser CLI.")
def laissezpasser():
    """laissezpasser CLI."""
    pass


@laissezpasser.command()
@click.argument("name", default="laissezpasser")
def command(name):
    """Docs."""
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [laissezpasser]
