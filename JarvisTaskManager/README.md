# JARVIS Task Manager

A Python task-management project with:
- Kivy graphical user interface
- Command-line interface
- JSON file storage
- Add, list, complete and delete operations
- Screen navigation and simple login validation

## Project structure

```text
JarvisTaskManager/
├── main.py
├── tasks.json              # created automatically
├── core/
│   ├── __init__.py
│   └── manager.py
├── data/
│   ├── __init__.py
│   └── storage.py
├── ui/
│   ├── __init__.py
│   └── screens.py
└── cli/
    ├── __init__.py
    └── interface.py
```

## Run the GUI

Install Kivy:

```bash
pip install kivy
```

Then from the project root:

```bash
python main.py
```

## Run the CLI

Create a small runner such as:

```python
from core.manager import TaskManager
from cli.interface import CLI

manager = TaskManager("tasks.json")
CLI(manager).run()
```

Save it as `cli_main.py` and run:

```bash
python cli_main.py
```

## Main workflow

Splash → Home → Login → Task Manager

Tasks are saved in `tasks.json`, so they remain available after restarting the application.
