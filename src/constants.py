import os
from os.path import abspath

USER_DATA_DIR = abspath(os.environ.get("REWARDS_DATA_DIR", "./data-dir"))
PROFILE_NAME = os.environ.get("REWARDS_PROFILE", "Default")