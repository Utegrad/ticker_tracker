import os

from dotenv import load_dotenv

load_dotenv()

DB_STRING = os.getenv("DB_STRING")
