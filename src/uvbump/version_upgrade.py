import re
from pathlib import Path

import coloredstrings as c
from constants import symbols
from fs import read_toml_file
from schemas import UpgradeOptions

import subprocess


def sync_lock(options: UpgradeOptions):
  subprocess.run(['uv', 'sync', '--upgrade', '--all-extras'], cwd=options['cwd'])


def version_replace(versions: dict[str, str], options: UpgradeOptions):
  file = Path(options['cwd']).joinpath('pyproject.toml')
  content = file.read_text(encoding='utf-8')

  for package, version in versions.items():
    content = _replace_package_version(content, package, version)

  file.write_text(content, encoding='utf-8')
  print(symbols['success'], 'Versions Replaced')

  pass


def version_collect(options: UpgradeOptions):
  file = Path(options['cwd']).joinpath('uv.lock')
  content = read_toml_file(file)
  versions = {p['name']: p['version'] for p in content['package'] if 'version' in p}
  print(symbols['info'], f'Versions {c.yellow(len(versions))} Collected')
  return versions


def _replace_package_version(content: str, package: str, version: str):
  pattern = r'"(' + package + r'(?:\[[^\]]*\])?)(>|>=|~=)[^"`,;]+'
  replacement = r'"\1>=' + version

  content, _ = re.subn(pattern, replacement, content)
  return content
