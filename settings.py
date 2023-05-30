import os

from dotenv import load_dotenv

load_dotenv(".env")

DB_URL = os.getenv("DB_URL", "")
