from typing import Annotated, TypedDict


class CommonOptions(TypedDict, total=False):
  cwd: str
  yes: bool


class ReleaseOptions(CommonOptions, total=False):
  no_git_check: Annotated[
    bool,
    'Indicates whether the git working tree needs to be cleared before bumping. Defaults to `true`.',
  ]
  commit: Annotated[
    bool,
    'Indicates whether the changes should be committed. Defaults to `true`.',
  ]
  all: Annotated[
    bool,
    'Indicates whether the git commit should include ALL files (`git commit --all`), rather than just the files that were modified by `version_bump()`. Defaults to `false`.',
  ]
  noVerify: Annotated[
    bool,
    'Indicates whether to bypass git commit hooks (`git commit --no-verify`). Defaults to `false`.',
  ]
  tag: Annotated[
    bool,
    'Indicates whether to tag the git commit. Defaults to `true`.',
  ]
  push: Annotated[
    bool,
    'Indicates whether to push the git commit and tag. Defaults to `true`.',
  ]


class ReleaseResult(TypedDict):
  version: str
  updatedFiles: list[str]


class UpgradeOptions(CommonOptions, total=False):
  pass
