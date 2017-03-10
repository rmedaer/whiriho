# -*- coding: utf-8 -*-

import click

from .whiriho import Whiriho
from .errors import WhirihoException

class CLIContext(object):
    """
    CLI context class. Contains all context configurations used by CLI commands.
    """

    def __init__(self, path, format=None):
        self.path = path
        self.whiriho = Whiriho(path, format=format)

@click.group()
@click.option(
    u'-c', '--config',
    help=u'Whiriho catalog path.',
    default=u'whiriho.json',
    type=click.Path()
)
@click.pass_context
def main(ctx, config):
    ctx.obj = CLIContext(config)

@main.command()
@click.pass_context
def list(ctx, **kwargs):
    try:
        ctx.obj.whiriho.load()
        for path in ctx.obj.whiriho.get_paths():
            click.echo(path)
    except WhirihoException as error:
        ctx.fail(error.message)

@main.command()
@click.argument('path')
@click.pass_context
def get(ctx, path, **kwargs):
    try:
        ctx.obj.whiriho.load()
        uri, format, schema = ctx.obj.whiriho.get_config_meta(path)
        click.echo('URI: %s' % uri)
        click.echo('Format: %s' % format)
        click.echo('Schema: %s' % schema)
    except WhirihoException as error:
        ctx.fail(error.message)

if __name__ == "__main__":
    main()
