import click
from config import resolve_config
from git import check_git_status, git_commit, git_push, git_tag
from schemas import ReleaseOptions
from uvbump import __version__
from version_bump import version_bump
from version_upgrade import version_collect, version_replace, sync_lock


def common_options(func):
  """Decorator to add common options to commands"""
  func = click.option('--cwd', default='.', help='The path to the `pyproject.toml` file')(func)
  func = click.option('-y', '--yes', is_flag=True, help='Skip confirmation')(func)
  return func


@click.group()
@click.version_option(__version__, '-v', '--version', help='Show version')
def cli():
  """Bumpp - A Python version bumping tool"""
  pass


@cli.command()
@common_options
@click.option('--no-git-check', default=True, is_flag=True, help='Skip git check')
@click.option('--commit', default=True, is_flag=True, help='Commit the changes')
@click.option('--all', default=False, is_flag=True, help='Include all files in the git commit')
@click.option('--no-verify', default=False, is_flag=True, help='Skip git verification')
@click.option('--tag', default=True, is_flag=True, help='Tag the git commit')
@click.option('--push', default=False, is_flag=True, help='Push the git commit and tag')
def release(**kwargs: ReleaseOptions):
  """Release a new version (bump version, commit, tag, and push)"""
  config = resolve_config(kwargs)

  if not config['no_git_check']:
    check_git_status()

  result = version_bump(config)

  git_commit(result, config)
  git_tag(result, config)

  git_push(result, config)


@cli.command()
@common_options
def upgrade(**kwargs):
  """Sync `uv.lock` dependencies, meanwhile update `pyproject.toml`"""
  config = resolve_config(kwargs)

  sync_lock(config)
  versions = version_collect(config)

  version_replace(versions, config)


if __name__ == '__main__':
  cli()
