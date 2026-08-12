from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from screens.home_screen import HomeScreen
from screens.run_screen import RunScreen
from screens.result_screen import ResultScreen
from models.player import Player


class JogRApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player = Player()

    def build(self):

        manager = ScreenManager()

        home_screen = Screen(name="home")
        run_screen = Screen(name="run")
        result_screen = Screen(name="result")

        home_screen.add_widget(
            HomeScreen(
                player=self.player,
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

        run_screen = manager.get_screen("run")
        run_screen.children[0].start_timer()

    def go_to_result(self, manager):

        run_screen = manager.get_screen("run")
        result_screen = manager.get_screen("result")

        run_screen.children[0].stop_timer()

        time, distance, pace, xp = (
            run_screen.children[0].get_results()
        )

        self.player.add_run(
            distance,
            xp
        )

        result_screen.children[0].show_results(
            time,
            distance,
            pace,
            xp
        )

        manager.current = "result"

    def go_to_home(self, manager):

        home_screen = manager.get_screen("home")

        home_screen.children[0].update_stats()

        manager.current = "home"


if __name__ == "__main__":
    JogRApp().run()