from core.manager import TaskManager
from cli.interface import CLI

if __name__ == "__main__":
    manager = TaskManager("tasks.json")
    CLI(manager).run()
