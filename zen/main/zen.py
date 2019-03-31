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


@zen_cli.resultcallback()
def process_pipeline(processors, **kwargs):
    # iterator = (x.rstrip('\r\n') for x in input)
    """This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    """
    # Start with an empty iterable.
    stream = ()

    # Pipe it through all stream processors.
    for processor in processors:
        stream = processor(stream)

    # Evaluate the stream and throw away the items.
    # print(stream)
    # return stream
    for _ in stream:
        click.echo(_)
        # pass

    # for processor in processors:
        # print(processor)
        # for repo in processor(kwargs):
            # print(repo)
        # iterator = processor(iterator)
    # for item in iterator:
        # click.echo(item)


def generator(f):
    """Similar to the :func:`processor` but passes through old values
    unchanged and does not pass through the values as parameter.
    """
    @processor
    def new_func(stream, *args, **kwargs):
        for item in stream:
            yield item
        for item in f(*args, **kwargs):
            yield item
    return update_wrapper(new_func, f)


def processor(f):
    """Helper decorator to rewrite a function so that it returns another
    function from it.
    """
    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)
        return processor
    return update_wrapper(new_func, f)


# TODO: Actually replace usage of the above processor with a decorator
@zen_cli.command()
# @click.option('-p', '--patterns', default=['.*'], multiple=True)
@processor
def clone(repositories):
    # filter_by = '|'.join([r'(\S*{}\S*)'.format(p) for p in patterns])
    # regex = re.compile(filter_by)

    # repos = [r.name for r in repositories if regex.search(r.name)]
    with click.progressbar(repositories) as bar:
        for item in bar:
            click.echo(f'Cloning {item.name}')
            # do_something_with(item)
    # for repo in repositories:
        # click.echo_via_pager(f'Cloning {repo.name}')


    return repositories

# for repo in repositories:

        # click.echo(repo.name)
    # user_repositories = ctx.invoke(repos, username=username)
    # print(user_repositories)
    # regex = re.compile(repositories)

    # matching_repos = [repo for repo in user_repositories if regex.match(repo.name)]
    # for r in matching_repos:
        # click.echo(r.name)
    # click.echo(f'Cloning {ctx.obj["repos"]}')


@zen_cli.command()
@click.argument('username', default=None, required=False)
@click.option('-p', '--patterns', multiple=True, default=['.*'])
# @pass_context
@generator
def repos(username, patterns):

    git = login(token=os.environ['ZEN'])
    if not username:
        username = git.me().login
        repositories = git.repositories()
    else:
        repositories = git.repositories_by(username)

    filter_by = '|'.join([r'(\S*{}\S*)'.format(p) for p in patterns])
    regex = re.compile(filter_by)

    repositories = [r.name for r in repositories if regex.search(r.name)]
    return repositories

    # click.echo(f'{username} has access to the following repositories:')

    # for repository in repositories:
    #     click.echo(f'{repository.name}')

    # return repositories


def main():
    zen_cli(obj={})


if __name__ == '__main__':
    main()
