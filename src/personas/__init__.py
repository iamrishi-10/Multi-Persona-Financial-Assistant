from src.personas import beginner, trader, insurance
from src.personas.base import build_messages, stream_response

PERSONAS: dict[str, str] = {
    "beginner": beginner.SYSTEM_PROMPT,
    "trader": trader.SYSTEM_PROMPT,
    "insurance": insurance.SYSTEM_PROMPT,
}

__all__ = ["PERSONAS", "build_messages", "stream_response"]
