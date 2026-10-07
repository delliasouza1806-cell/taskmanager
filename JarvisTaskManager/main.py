from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from core.manager import TaskManager
from ui.screens import SplashScreen, HomeScreen, LoginScreen, TaskScreen

STORAGE_FILE = "tasks.json"


class JarvisApp(App):
    def build(self):
        manager = TaskManager(storage_filepath=STORAGE_FILE)

        screen_manager = ScreenManager()
        screen_manager.add_widget(SplashScreen(name="splash"))
        screen_manager.add_widget(HomeScreen(name="home"))
        screen_manager.add_widget(LoginScreen(name="login"))
        screen_manager.add_widget(TaskScreen(name="tasks"))

        screen_manager.get_screen("tasks").task_manager = manager
        screen_manager.current = "splash"
        return screen_manager


if __name__ == "__main__":
    JarvisApp().run()
