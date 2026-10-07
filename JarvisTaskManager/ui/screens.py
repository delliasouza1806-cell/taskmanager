from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)

        title = Label(text="JARVIS", font_size=42)
        subtitle = Label(text="Your Personal Task Assistant", font_size=18)

        start_button = Button(
            text="GET STARTED",
            size_hint=(1, 0.2),
        )
        start_button.bind(on_press=self.go_to_home)

        layout.add_widget(title)
        layout.add_widget(subtitle)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def go_to_home(self, instance):
        self.manager.current = "home"


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=40, spacing=20)

        title = Label(text="Welcome to JARVIS", font_size=32)
        message = Label(text="Manage your tasks easily")

        login_button = Button(text="LOGIN", size_hint=(1, 0.2))
        login_button.bind(on_press=self.go_to_login)

        exit_button = Button(text="EXIT", size_hint=(1, 0.2))
        exit_button.bind(on_press=self.exit_app)

        layout.add_widget(title)
        layout.add_widget(message)
        layout.add_widget(login_button)
        layout.add_widget(exit_button)
        self.add_widget(layout)

    def go_to_login(self, instance):
        self.manager.current = "login"

    def exit_app(self, instance):
        from kivy.app import App
        App.get_running_app().stop()


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical", padding=40, spacing=15)

        title = Label(text="JARVIS LOGIN", font_size=30)

        self.username = TextInput(
            hint_text="Username",
            multiline=False,
        )
        self.password = TextInput(
            hint_text="Password",
            password=True,
            multiline=False,
        )

        login_button = Button(text="LOGIN", size_hint=(1, 0.2))
        back_button = Button(text="BACK", size_hint=(1, 0.2))

        login_button.bind(on_press=self.login)
        back_button.bind(on_press=self.go_back)

        layout.add_widget(title)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_button)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def login(self, instance):
        if not self.username.text.strip() or not self.password.text:
            self.show_message("Please enter both username and password.")
            return

        self.manager.current = "tasks"

    def go_back(self, instance):
        self.manager.current = "home"

    def show_message(self, message):
        Popup(
            title="Login",
            content=Label(text=message),
            size_hint=(0.8, 0.3),
        ).open()


class TaskScreen(Screen):
    task_manager = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10,
        )

        title = Label(
            text="MY TASKS",
            font_size=30,
            size_hint=(1, 0.12),
        )

        self.task_input = TextInput(
            hint_text="Enter a new task",
            multiline=False,
            size_hint=(1, 0.12),
        )

        add_button = Button(text="ADD TASK", size_hint=(1, 0.12))
        refresh_button = Button(text="REFRESH TASKS", size_hint=(1, 0.12))
        back_button = Button(text="BACK", size_hint=(1, 0.12))

        add_button.bind(on_press=self.add_task)
        refresh_button.bind(on_press=self.refresh_tasks)
        back_button.bind(on_press=self.go_back)

        self.task_list = BoxLayout(
            orientation="vertical",
            spacing=8,
            size_hint_y=None,
        )
        self.task_list.bind(
            minimum_height=self.task_list.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(self.task_list)

        self.layout.add_widget(title)
        self.layout.add_widget(self.task_input)
        self.layout.add_widget(add_button)
        self.layout.add_widget(refresh_button)
        self.layout.add_widget(scroll)
        self.layout.add_widget(back_button)
        self.add_widget(self.layout)

    def on_enter(self):
        self.refresh_tasks()

    def add_task(self, instance):
        description = self.task_input.text.strip()

        if not description:
            self.show_message("Please enter a task.")
            return

        if self.task_manager:
            self.task_manager.add_task(description)

        self.task_input.text = ""
        self.refresh_tasks()

    def refresh_tasks(self, instance=None):
        self.task_list.clear_widgets()

        if not self.task_manager:
            return

        tasks = self.task_manager.get_tasks()

        if not tasks:
            self.task_list.add_widget(
                Label(
                    text="No tasks found. Add your first task!",
                    size_hint_y=None,
                    height=60,
                )
            )
            return

        for task in tasks:
            completed = task.get("completed", False)
            status = "✓ COMPLETED" if completed else "PENDING"

            text = (
                f"ID: {task['id']}   {status}\n"
                f"{task['description']}"
            )

            task_layout = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=80,
                spacing=5,
            )

            label = Label(text=text)

            complete_button = Button(
                text="DONE" if not completed else "UNDONE",
                size_hint_x=0.22,
            )
            complete_button.disabled = completed
            complete_button.bind(
                on_press=lambda instance, task_id=task["id"]:
                self.complete_task(task_id)
            )

            delete_button = Button(
                text="DELETE",
                size_hint_x=0.22,
            )
            delete_button.bind(
                on_press=lambda instance, task_id=task["id"]:
                self.delete_task(task_id)
            )

            task_layout.add_widget(label)
            task_layout.add_widget(complete_button)
            task_layout.add_widget(delete_button)
            self.task_list.add_widget(task_layout)

    def complete_task(self, task_id):
        if self.task_manager:
            self.task_manager.complete_task(task_id)
        self.refresh_tasks()

    def delete_task(self, task_id):
        if self.task_manager:
            self.task_manager.delete_task(task_id)
        self.refresh_tasks()

    def go_back(self, instance):
        self.manager.current = "home"

    def show_message(self, message):
        Popup(
            title="JARVIS",
            content=Label(text=message),
            size_hint=(0.8, 0.3),
        ).open()
