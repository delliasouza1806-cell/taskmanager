from core.manager import TaskManager


class CLI:
    """Command-line interface for the Task Manager."""

    def __init__(self, manager: TaskManager):
        self._manager = manager
        self._running = False

    def _display_help(self):
        print("""
Task Manager CLI Commands:

  add <description>   - Adds a new task.
  list                - Lists all tasks.
  complete <id>       - Marks a task as completed.
  delete <id>         - Deletes a task.
  help                - Displays this help message.
  quit / exit         - Exits the application.
""")

    def run(self):
        self._running = True
        print("Welcome to the Task Manager CLI!")
        self._display_help()

        while self._running:
            try:
                user_input = input("\n> ").strip()
                if not user_input:
                    continue

                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                argument = parts[1] if len(parts) > 1 else ""

                if command == "add":
                    if not argument.strip():
                        print("Usage: add <description>")
                        continue
                    task = self._manager.add_task(argument)
                    print(f"Task '{task['description']}' (ID: {task['id']}) added.")

                elif command == "list":
                    tasks = self._manager.get_tasks()
                    if not tasks:
                        print("No tasks found.")
                    else:
                        print("\n--- Your Tasks ---")
                        for task in tasks:
                            status = "[COMPLETED]" if task.get("completed") else "[PENDING]"
                            print(
                                f"{status} ID: {task['id']} "
                                f"Description: {task['description']}"
                            )

                elif command == "complete":
                    if not argument.isdigit():
                        print("Usage: complete <id>")
                        continue
                    task = self._manager.complete_task(int(argument))
                    print("Task completed." if task else "Task not found.")

                elif command == "delete":
                    if not argument.isdigit():
                        print("Usage: delete <id>")
                        continue
                    task = self._manager.delete_task(int(argument))
                    print("Task deleted." if task else "Task not found.")

                elif command == "help":
                    self._display_help()

                elif command in ("quit", "exit"):
                    self._running = False
                    print("Exiting Task Manager. Goodbye!")

                else:
                    print("Unknown command. Type 'help'.")

            except (EOFError, KeyboardInterrupt):
                self._running = False
                print("\nExiting Task Manager. Goodbye!")
            except Exception as error:
                print(f"Error: {error}")
