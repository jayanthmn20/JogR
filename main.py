from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from screens.home_screen import HomeScreen
from screens.run_screen import RunScreen
from screens.result_screen import ResultScreen


class JogRApp(App):

    def build(self):

        manager = ScreenManager()

        home_screen = Screen(name="home")
        run_screen = Screen(name="run")
        result_screen = Screen(name="result")

        home_screen.add_widget(
            HomeScreen(
                go_to_run_screen=lambda instance: self.go_to_run(manager)
            )
        )

        run_screen.add_widget(
            RunScreen(
                go_to_result_screen=lambda instance: self.go_to_result(manager)
            )
        )

        result_screen.add_widget(
            ResultScreen(
                go_to_home_screen=lambda instance: self.go_to_home(manager)
            )
        )

        manager.add_widget(home_screen)
        manager.add_widget(run_screen)
        manager.add_widget(result_screen)

        return manager

    def go_to_run(self, manager):
        manager.current = "run"

    def go_to_result(self, manager):
        manager.current = "result"

    def go_to_home(self, manager):
        manager.current = "home"


if __name__ == "__main__":
    JogRApp().run()