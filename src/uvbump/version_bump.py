import sys
from pathlib import Path

import coloredstrings as c
import questionary
import semver
from fs import read_toml_file, update_toml_file
from questionary import Choice
from schemas import ReleaseOptions, ReleaseResult


def version_bump(options: ReleaseOptions) -> ReleaseResult:
  path = Path(options['cwd']).joinpath('pyproject.toml')
  content = read_toml_file(path)

  if 'project' not in content:
    print(c.red('Project table not found in pyproject.toml'))
    sys.exit(1)

  version: str | None = content['project'].get('version')
  if version and not semver.Version.is_valid(version):
    print(c.red('Invalid version: {version}'))
    sys.exit(1)

  dynamic: list[str] | None = content['project'].get('dynamic', [])
  is_dynamic_version = dynamic and any(i == 'version' for i in dynamic)
  if is_dynamic_version:
    print(c.red('Dynamic version is not supported'))
    sys.exit(1)

  newVersion = _get_new_version(version, options)
  if not options['yes']:
    confirm = questionary.confirm('Bump?', default=True).ask()
    if not confirm:
      print(c.red('Aborting...'))
      sys.exit(1)

  content['project']['version'] = str(newVersion)
  update_toml_file(path, content)

  return {
    'version': str(newVersion),
    'updatedFiles': [path],
  }


def _get_new_version(version: str, options: ReleaseOptions):
  PADDING = 13

  next_versions = _get_next_versions(version)

  choices = [
    Choice(
      title=f'{"major".ljust(PADDING)} {next_versions["major"]}',
      value='major',
    ),
    Choice(
      title=f'{"minor".ljust(PADDING)} {next_versions["minor"]}',
      value='minor',
    ),
    Choice(
      title=f'{"patch".ljust(PADDING)} {next_versions["patch"]}',
      value='patch',
    ),
    Choice(
      title=f'{"next".ljust(PADDING)} {next_versions["next"]}',
      value='next',
    ),
    Choice(
      title=f'{"pre-patch".ljust(PADDING)} {next_versions["prepatch"]}',
      value='prepatch',
    ),
    Choice(
      title=f'{"pre-minor".ljust(PADDING)} {next_versions["preminor"]}',
      value='preminor',
    ),
    Choice(
      title=f'{"pre-major".ljust(PADDING)} {next_versions["premajor"]}',
      value='premajor',
    ),
    Choice(
      title=f'{"as-is".ljust(PADDING)} {version}',
      value='none',
    ),
    Choice(
      title='custom ...'.ljust(PADDING + 4),
      value='custom',
    ),
  ]

  release = questionary.select(
    f'Current version {version}',
    default='next',
    choices=choices,
  ).ask()

  if release is None:
    print(c.red('Aborting...'))
    sys.exit(1)

  if release == 'none':
    return version

  if release == 'custom':
    custom_version = questionary.text(
      'Enter the new version number:',
      validate=semver.Version.is_valid,
    ).ask()
    return custom_version

  return next_versions[release]


def _get_next_versions(version: str):
  current_version = semver.VersionInfo.parse(version)
  return {
    'major': current_version.bump_major(),
    'minor': current_version.bump_minor(),
    'patch': current_version.bump_patch(),
    'next': current_version.bump_patch(),
    'prepatch': current_version.bump_patch().bump_prerelease()
    if not current_version.prerelease
    else current_version.bump_prerelease(),
    'preminor': current_version.bump_minor().bump_prerelease(),
    'premajor': current_version.bump_major().bump_prerelease(),
  }
