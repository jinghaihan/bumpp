import copy

from schemas import ReleaseOptions


def resolve_config(options: ReleaseOptions):
  config: ReleaseOptions = copy.deepcopy(options)
  return config
