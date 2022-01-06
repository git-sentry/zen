import configparser
import os
import webbrowser

import click
import simple_term_menu
from zen_core.handlers.git_client import GitClient
from zen_core.handlers.git_repo import GitRepo

QUERY_CONFIG_FILE_PATH = os.path.expanduser('~/.config/sentry/query.ini')


def read_query():
    config_parser = configparser.ConfigParser()
    config_parser.read(QUERY_CONFIG_FILE_PATH, encoding='utf-8')
    queries = [(name, query) for name, query in config_parser['queries'].items()]
    return queries

@click.group()
@click.pass_context
def prs(ctx):
    pass


@prs.command()
@click.option('-q', '--query')
@click.pass_context
def search(ctx, query=None):
    git: GitClient = ctx.obj.get('client')
    if query is not None:
        pass
    else:
        predefined_queries = read_query()
        queries = [f'{name} - {query}' for name, query in predefined_queries]
        queries.append('Exit')
        top_term = simple_term_menu.TerminalMenu(queries)
        terminal_menu_exit = False
        while not terminal_menu_exit:
            os.system('clear')
            query_index = top_term.show()
            # query_index = simple_term_menu.TerminalMenu([f'{name} - {query}' for name, query in predefined_queries]).show()
            if queries[query_index] == 'Exit':
                terminal_menu_exit = True
                continue
            query_name, query_to_run = predefined_queries[query_index]
            issues = git._git_client.search_issues(query_to_run)
            repositories = {}
            for i in issues:
                pr = i.issue.pull_request()
                if pr is not None:
                    repository = GitRepo(pr.repository)
                    if repository.full_name() not in repositories:
                        repositories[repository.full_name()] = []
                    repositories[repository.full_name()].append(pr)
            repo_choices = list(repositories.keys())
            repo_choices.append('Back')
            repo_feed = simple_term_menu.TerminalMenu(repo_choices)
            feed_menu_back = False
            while not feed_menu_back:
                os.system('clear')
                repo_index = repo_feed.show()
                if repo_choices[repo_index] == 'Back':
                    feed_menu_back = True
                    continue
                repo = list(repositories.keys())[repo_index]
                open_prs = repositories[repo]
                choices = []
                for pr in open_prs:
                    description = f'#{pr.number} {pr.title} by {pr.user} {len(list(pr.review_comments()))} ✉'
                    state = any(r.state != 'APPROVED' for r in pr.reviews())
                    if state:
                        description = f'⨯ {description}'
                    else:
                        description = f'✓ {description}'
                    choices.append(description)
                choices.append('Back')
                feed_pr_back = False
                while not feed_pr_back:
                    pr_index = simple_term_menu.TerminalMenu(choices).show()
                    if choices[pr_index] == 'Back':
                        feed_pr_back = True
                        continue
                    p = open_prs[pr_index]
                    webbrowser.open(p.html_url)
