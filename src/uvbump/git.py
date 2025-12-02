import subprocess

from constants import symbols
from schemas import ReleaseOptions, ReleaseResult


def check_git_status():
  result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)

  stdout = result.stdout.strip()
  if stdout:
    raise Exception(f'Git status is not clean: {stdout}')


def git_commit(result: ReleaseResult, options: ReleaseOptions):
  if not options['commit']:
    return

  args: list[str] = ['commit', '--allow-empty']

  if options['all']:
    args.append('--all')
  else:
    args.extend(result['updatedFiles'])

  if options['no_verify']:
    args.append('--no-verify')

  args.append('--message')
  args.append(_format_commit_str(result['version']))

  subprocess.run(['git', *args])

  print(f'{symbols["success"]} Git commit')


def git_tag(result: ReleaseResult, options: ReleaseOptions):
  if not options['tag']:
    return

  args: list[str] = [
    'tag',
    '--annotate',
    '--message',
    _format_commit_str(result['version']),
    _format_version_string(result['version']),
  ]

  subprocess.run(['git', *args])

  print(f'{symbols["success"]} Git tag')


def git_push(result: ReleaseResult, options: ReleaseOptions):
  if not options['push']:
    return

  subprocess.run(['git', 'push'])

  if options['tag']:
    subprocess.run(['git', 'push', '--tags'])

  print(f'{symbols["success"]} Git push')


def _format_version_string(version: str) -> str:
  return f'v{version}'


def _format_commit_str(version: str) -> str:
  return f'chore: release {_format_version_string(version)}'
