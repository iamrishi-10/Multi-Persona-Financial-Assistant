import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
ROOT_DIR = Path(__file__).parent
DATA_DIR = ROOT_DIR / "data"
LOG_FILE = DATA_DIR / "conversation_log.json"

# Model
MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))

# OpenAI pricing per 1K tokens (USD) — gpt-4o-mini defaults
INPUT_COST_PER_1K: float = 0.000150
OUTPUT_COST_PER_1K: float = 0.000600

# INR conversion rate
USD_TO_INR: float = 83.0
