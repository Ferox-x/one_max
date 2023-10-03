from pathlib import Path
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent
FRAMES_DIR = BASE_DIR / 'frames'
PLOTS_DIR = BASE_DIR / 'plots'
RESULTS_DIR = BASE_DIR / 'results'

ENV_CONSTANTS = dotenv_values(BASE_DIR / ".env")
