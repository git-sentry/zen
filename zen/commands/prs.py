import webbrowser
from collections import OrderedDict

import click
from zen_core.handlers.git_client import GitClient


@click.group()
@click.pass_context
def prs(ctx):
    pass


@prs.command()
@click.pass_context
def mine(ctx):
    git: GitClient = ctx.obj.get('client')
    prs = git._git_client.search_issues(
        "is:pr user:gocardless pushed:<2021-08-31 author:dragosdumitrache author:tajoku author:stephenbinns author:gc-carlar author:meronkha author:alfredrichards state:open")
    # org = git.organization('gocardless')
    pr_navigation = _compute_open_prs(prs)
    navigable_map = []
    for org, repos in pr_navigation.items():
        if len(repos.values()) != 0:
            click.echo(org)
        for repo, open_prs in repos.items():
            click.echo('\t{} open PRs:'.format(repo))
            for pr in open_prs:
                click.echo(
                    '\t\t{}: {} - {}'.format(click.style(len(navigable_map), fg='cyan', bold=True),
                                             click.style(pr.title, fg='green'), click.style(pr.user.login, fg='yellow')))
                navigable_map += [pr]
    #
    pr_index = None
    if navigable_map:
        click.echo(
            '\nInput the number shown next to a PR to it to open it in your browser or \'q\' to terminate. ')
        while pr_index != 'q':
            pr_index = input('PR: ')
            if pr_index == 'q':
                break
            pr_index = int(pr_index)
            if pr_index > len(navigable_map) or pr_index < 0:
                click.echo(
                    'No PR mapped to index {}. Please enter a valid value.'.format(click.style(pr_index, fg='red')))
            else:
                pr_to_open = navigable_map[pr_index]
                pr_url = pr_to_open.html_url
                webbrowser.open(pr_url)
    else:
        click.echo('No open PRs for the organisations you requested')


def _compute_open_prs(prs):
    pr_navigation = OrderedDict()

    # for org in filtered_orgs:
    # pr_navigation[org.login()] = OrderedDict()
    pr_navigation['gocardless'] = OrderedDict()
    for i in prs:
        pr = i.issue.pull_request()
        if pr is not None:
            name = pr.repository.name
            if name not in pr_navigation['gocardless']:
                pr_navigation['gocardless'][name] = []
            pr_navigation['gocardless'][name].append(pr)
    return pr_navigation
