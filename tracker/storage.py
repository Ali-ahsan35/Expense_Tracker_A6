import json
import os
from json import JSONDecodeError


def ensure_data_file(path: str) -> None:
    """
    Create the JSON file if it doesn't exist.
    """
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"version": 1, "expenses": []}, f, indent=2)


def load_expenses(path: str) -> list[dict]:
    """
    Load expenses from JSON. Returns a list of dicts.
    """
    ensure_data_file(path)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("expenses", [])
    except JSONDecodeError:
        raise ValueError("data file is corrupted (invalid JSON)")


def save_expenses(path: str, expenses: list[dict]) -> None:
    """
    Save expenses to JSON.
    """
    ensure_data_file(path)

    with open(path, "w", encoding="utf-8") as f:
        json.dump({"version": 1, "expenses": expenses}, f, indent=2)
