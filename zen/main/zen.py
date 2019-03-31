#/usr/local/bin/python3

import os
import click
import re

from github3 import login
from click import pass_context
from functools import update_wrapper

@click.group(chain=True)
def zen_cli():
    pass



@zen_cli.command()
@click.argument('username', default=None, required=False)
@click.option('-p', '--patterns',  default=['.*'], multiple=True)
@pass_context
def clone(ctx, username, patterns):

    repositories = ctx.forward(repos)

    for repo in repositories:
        click.echo(f'Cloning {repo.name}')

    return repositories


@zen_cli.command()
@click.argument('username', default=None, required=False)
@click.option('-p', '--patterns', multiple=True, default=['.*'])
@pass_context
def repos(ctx, username, patterns):

    git = login(token=os.environ['ZEN'])
    if not username:
        username = git.me().login
        repositories = git.repositories()
    else:
        repositories = git.repositories_by(username)

    filter_by = '|'.join([r'(\S*{}\S*)'.format(p) for p in patterns])
    regex = re.compile(filter_by)

    repositories = [r for r in repositories if regex.search(r.name)]

    if ctx.parent.parent is None:
        click.echo(f'{username} has access to the following repositories:')

        for repository in repositories:
            click.echo(f'{repository.name}')

    return repositories


def main():
    zen_cli(obj={})


if __name__ == '__main__':
    main()
