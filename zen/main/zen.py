#/usr/local/bin/python3

import os
import click

from github3 import login


@click.group()
def zen_cli():
    pass


@zen_cli.command()
@click.argument('username', required=False)
def repos(username=None):
    git = login(token=os.environ['ZEN'])

    if not username:
        username = git.me().login

    click.echo(f'{username} owns the following repositories:')
    for repository in git.repositories_by(username):
        click.echo(f'{repository.name}')


def main():
    zen_cli()


if __name__ == '__main__':
    main()
