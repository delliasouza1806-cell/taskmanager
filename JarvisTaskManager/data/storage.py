import json
import os
from typing import List, Dict, Any


def load_tasks(filepath: str) -> List[Dict[str, Any]]:
    """Load tasks from a JSON file. Return [] when the file is missing/invalid."""
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            tasks = json.load(file)
            return tasks if isinstance(tasks, list) else []
    except (json.JSONDecodeError, OSError) as error:
        print(f"Error loading {filepath}: {error}")
        return []


def save_tasks(filepath: str, tasks: List[Dict[str, Any]]) -> None:
    """Save tasks to JSON, creating the parent directory when needed."""
    try:
        directory = os.path.dirname(os.path.abspath(filepath))
        os.makedirs(directory, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except OSError as error:
        print(f"Error saving {filepath}: {error}")
