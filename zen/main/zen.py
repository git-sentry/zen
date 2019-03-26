#/usr/local/bin/python3

import os
import click

from github3 import login


@click.group()
def zen_cli():
    pass


@zen_cli.command()
def repos():
    git = login(token=os.environ['ZEN'])

    click.echo(f'{git.me().login} owns the following repositories:')
    for repository in git.repositories_by(git.me().login):
        click.echo(f'{repository.name}')


def main():
    zen_cli()


if __name__ == '__main__':
    main()
