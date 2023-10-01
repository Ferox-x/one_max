from pathlib import Path
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_CONSTANTS = dotenv_values(BASE_DIR / ".env")
