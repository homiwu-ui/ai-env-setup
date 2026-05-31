import json
import os
from datetime import datetime

HISTORY_DIR = os.path.join(os.path.dirname(__file__), "_history")
os.makedirs(HISTORY_DIR, exist_ok=True)


def _session_file() -> str:
    today = datetime.now().strftime("%Y%m%d")
    return os.path.join(HISTORY_DIR, f"session_{today}.jsonl")


def save_turn(user: str, assistant: str) -> None:
    entry = {
        "time": datetime.now().isoformat(),
        "user": user,
        "assistant": assistant,
    }
    with open(_session_file(), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def get_recent(limit: int = 5) -> list[dict]:
    path = _session_file()
    if not os.path.exists(path):
        return []
    turns = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                turns.append(json.loads(line))
    return turns[-limit:]
