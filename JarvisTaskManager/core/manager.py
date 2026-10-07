from typing import List, Dict, Any, Optional
from data.storage import load_tasks, save_tasks


class TaskManager:
    """Business logic for creating, listing, completing and deleting tasks."""

    def __init__(self, storage_filepath: str):
        self._filepath = storage_filepath
        self._tasks: List[Dict[str, Any]] = load_tasks(self._filepath)

        for task in self._tasks:
            task.setdefault("completed", False)

    def _save(self) -> None:
        save_tasks(self._filepath, self._tasks)

    def _generate_next_id(self) -> int:
        if not self._tasks:
            return 1
        return max((task.get("id", 0) for task in self._tasks), default=0) + 1

    def add_task(self, description: str) -> Dict[str, Any]:
        description = description.strip()
        if not description:
            raise ValueError("Task description cannot be empty.")

        task = {
            "id": self._generate_next_id(),
            "description": description,
            "completed": False,
        }
        self._tasks.append(task)
        self._save()
        return task

    def get_tasks(self, include_completed: bool = True) -> List[Dict[str, Any]]:
        if include_completed:
            return list(self._tasks)
        return [task for task in self._tasks if not task.get("completed", False)]

    def complete_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        for task in self._tasks:
            if task.get("id") == task_id:
                task["completed"] = True
                self._save()
                return task
        return None

    def delete_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        for task in self._tasks:
            if task.get("id") == task_id:
                self._tasks.remove(task)
                self._save()
                return task
        return None
