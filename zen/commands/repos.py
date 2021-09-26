import pprint

import click
import fuzzyfinder
from simple_term_menu import TerminalMenu
from zen_core.handlers.git_client import GitClient
from zen_core.handlers.git_repo import GitRepo


@click.group()
@click.pass_context
def repos(ctx):
    git: GitClient = ctx.obj.get('client')
    if git._repos is None:
        git._repos = [GitRepo(repo) for repo in git._git_client.repositories()]
    ctx.obj['client'] = git


@repos.command()
@click.argument('query', required=False)
@click.pass_context
def show(ctx, query):
    git: GitClient = ctx.obj['client']
    print(f'Welcome back {git.me().name()}')
    if query is not None:
        results = list(fuzzyfinder.main.fuzzyfinder(query, [repo.full_name() for repo in git._repos]))
    else:
        results = [repo.full_name() for repo in git._repos]
    pprint.pprint(results)


@repos.command()
@click.argument('query', required=False)
@click.pass_context
def clone(ctx, query):
    git: GitClient = ctx.obj['client']
    print(f'Welcome back {git.me().name()}')
    if query is not None:
        results = list(
            fuzzyfinder.main.fuzzyfinder(query, [repo for repo in git._repos], accessor=lambda repo: repo.full_name()))
    else:
        results = git._repos

    terminal_menu = TerminalMenu([r.full_name() for r in results],
                                 multi_select=True,
                                 show_multi_select_hint=True)
    menu_entry_indices = terminal_menu.show()
    repos = [results[index] for index in menu_entry_indices]
    for repo in repos:
        print(repo.ssh_url())
