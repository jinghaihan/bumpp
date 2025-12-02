from pathlib import Path

import tomlkit


def read_toml_file(path: str):
  with open(path, 'r') as file:
    content = file.read()
    return tomlkit.loads(content)


def update_toml_file(path: str, content: dict):
  target_file = Path(path)
  temp_file = target_file.with_suffix(target_file.suffix + '.tmp')

  try:
    with open(temp_file, 'w') as file:
      file.write(tomlkit.dumps(content))
      temp_file.replace(target_file)
  except Exception:
    if temp_file.exists():
      temp_file.unlink()
    raise
