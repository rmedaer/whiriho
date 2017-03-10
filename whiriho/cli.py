# -*- coding: utf-8 -*-

import click
import json

from .whiriho import Whiriho
from .errors import WhirihoException

class CLIContext(object):
    """
    CLI context class. Contains all context configurations used by CLI commands.
    """

    def __init__(self, path, format=None):
        self.path = path
        self.whiriho = Whiriho(path, format=format)

def dump(data):
    """
    All CLI displayed data, should use this method to format output JSON.
    """
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

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
def meta(ctx, path, **kwargs):
    try:
        ctx.obj.whiriho.load()
        uri, format, schema = ctx.obj.whiriho.get_config_meta(path)
        click.echo('URI: %s' % uri)
        click.echo('Format: %s' % format)
        click.echo('Schema: %s' % schema)
    except WhirihoException as error:
        ctx.fail(error.message)

@main.command()
@click.argument('path')
@click.pass_context
def get(ctx, path, **kwargs):
    try:
        ctx.obj.whiriho.load()
        click.echo(dump(ctx.obj.whiriho.get_config_data(path)))
    except WhirihoException as error:
        ctx.fail(error.message)

@main.command()
@click.argument('path')
@click.argument('data')
@click.pass_context
def set(ctx, path, data, **kwargs):
    try:
        data = json.loads(data)
    except:
        ctx.fail('Could not read input JSON, check \'data\' argument')

    try:
        ctx.obj.whiriho.load()
        ctx.obj.whiriho.set_config_data(path, data)
    except WhirihoException as error:
        ctx.fail(error.message)

@main.command()
@click.argument('path')
@click.pass_context
def schema(ctx, path, **kwargs):
    try:
        ctx.obj.whiriho.load()
        click.echo(dump(ctx.obj.whiriho.get_config_schema(path)))
    except WhirihoException as error:
        ctx.fail(error.message)

@main.command()
@click.option(
    u'--format',
    help=u'Which file format to use'
)
@click.option(
    u'--version',
    help=u'Version of catalog format to use',
    default='1.0.0'
)
@click.option(
    u'--force', is_flag=True,
    help=u'Force reinitialization if catalog already exists',
)
@click.pass_context
def init(ctx, format, version, force, **kwargs):
    try:
        ctx.obj.whiriho.initialize(format, version, force)
    except WhirihoException as error:
        ctx.fail(error.message)

if __name__ == "__main__":
    main()
