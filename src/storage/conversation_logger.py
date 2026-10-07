import json
from datetime import datetime
from pathlib import Path
import config


def _load(path: Path) -> list:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save(path: Path, log: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")


def log_exchange(
    persona: str,
    user_message: str,
    ai_response: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> None:
    """Append one conversation exchange to the JSON log file."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "persona": persona,
        "user_message": user_message,
        "ai_response": ai_response,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
    }

    log = _load(config.LOG_FILE)
    log.append(entry)
    _save(config.LOG_FILE, log)


def read_log() -> list:
    """Return all logged exchanges as a list of dicts."""
    return _load(config.LOG_FILE)


def clear_log() -> None:
    """Wipe the log file."""
    _save(config.LOG_FILE, [])
