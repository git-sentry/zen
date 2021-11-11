# /usr/local/bin/python3

import os
import click
import re
import subprocess

from github3 import login
from click import pass_context
from zen_core.handlers.git_client import GitClient

from zen.commands.prs import prs
from zen.commands.repos import repos


@click.group()
@pass_context
def zen_cli(ctx):
    pass


#
# # TODO: Add config.ini support later on
# # TODO: Add workspace env variable for cloning
# # TODO: Improve testability.
# # TODO: Consider Cucumber tests for python
# @zen_cli.command()
# @click.argument('username', default=None, required=False)
# @click.option('-p', '--patterns', multiple=True, default=['.*'])
# @pass_context
# def repos(ctx, username, patterns):
#
#     git = login(token=os.environ['ZEN'])
#     if not username:
#         username = git.me().login
#         repositories = git.repositories()
#     else:
#         repositories = git.repositories_by(username)
#
#     filter_by = '|'.join([r'(\S*{}\S*)'.format(p) for p in patterns])
#     regex = re.compile(filter_by)
#
#     repositories = [r for r in repositories if regex.findall(r.name)]
#
#     if ctx.parent.parent is None:
#         click.echo(f'{username} has access to the following repositories:')
#
#         for repository in repositories:
#             click.echo(f'{repository.name}')
#
#     return repositories
#
#
# @zen_cli.command()
# @click.argument('username', default=None, required=False)
# @click.option('-p', '--patterns',  default=['.*'], multiple=True)
# @pass_context
# def clone(ctx, username, patterns):
#
#     repositories = ctx.forward(repos)
#
#     for repo in repositories:
#         _repository_clone(repo)
#
#     return repositories
#
#
# def _repository_clone(repository, path=os.environ.get('WORKSPACE')):
#     repo_dir = os.path.join(path, repository.name)
#     if os.path.isdir(repo_dir):
#         click.echo(f'{repo_dir} already exists')
#         return False
#
#     subprocess.run(['git', 'clone', repository.ssh_url, repo_dir])
#     return True


def main():
    git = GitClient()
    zen_cli.add_command(repos)
    zen_cli.add_command(prs)
    zen_cli(obj={'client': git})


if __name__ == '__main__':
    main()
