import os
from distutils.util import strtobool

from dotenv import load_dotenv

load_dotenv(".env")

DB_URL = os.getenv("DB_URL", "")
TEST_MODE = bool(strtobool(os.getenv("TEST_MODE", "False")))
