import pprint

import click
from zen_core.handlers.git_client import GitClient


@click.group()
def zen_cli():
    pass


@zen_cli.command()
@click.argument('query', nargs=1)
def search(query):
    git = GitClient()
    matching_repos = git.search_repos(query)
    for repo in matching_repos:
        pprint.pprint(f'{repo.full_name()}')


# @zen_cli.command()
# @click.argument('query', nargs=1)
# def clone(query):
#     git = GitClient()
#     git.clone(query)


def main():
    zen_cli()


if __name__ == '__main__':
    main()
