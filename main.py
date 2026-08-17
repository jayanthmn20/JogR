__version__ = "0.1.0"

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from screens.home_screen import HomeScreen
from screens.run_screen import RunScreen
from screens.result_screen import ResultScreen
from screens.history_screen import HistoryScreen

from models.player import Player
from services.storage import save_player, load_player, save_run


class JogRApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        saved_data = load_player()

        if saved_data:
            self.player = Player(
                name=saved_data["name"]
            )

            self.player.level = saved_data["level"]
            self.player.xp = saved_data["xp"]
            self.player.total_distance = saved_data["total_distance"]
            self.player.total_runs = saved_data["total_runs"]

        else:
            self.player = Player()

        self.home_widget = None
        self.run_widget = None
        self.result_widget = None
        self.history_widget = None

    def build(self):

        manager = ScreenManager()

        home_screen = Screen(name="home")
        run_screen = Screen(name="run")
        result_screen = Screen(name="result")
        history_screen = Screen(name="history")

        self.home_widget = HomeScreen(
            player=self.player,
            go_to_run_screen=lambda instance: self.go_to_run(manager),
            go_to_history_screen=lambda instance: self.go_to_history(manager)
        )

        self.run_widget = RunScreen(
            go_to_result_screen=lambda instance: self.go_to_result(manager)
        )

        self.result_widget = ResultScreen(
            go_to_home_screen=lambda instance: self.go_to_home(manager)
        )

        self.history_widget = HistoryScreen(
            go_to_home_screen=lambda instance: self.go_to_home(manager)
        )

        home_screen.add_widget(self.home_widget)
        run_screen.add_widget(self.run_widget)
        result_screen.add_widget(self.result_widget)
        history_screen.add_widget(self.history_widget)

        manager.add_widget(home_screen)
        manager.add_widget(run_screen)
        manager.add_widget(result_screen)
        manager.add_widget(history_screen)

        return manager

    def go_to_run(self, manager):

        manager.current = "run"

        self.run_widget.start_timer()

    def go_to_result(self, manager):

        self.run_widget.stop_timer()

        (
            time,
            duration_seconds,
            distance,
            pace,
            pace_seconds_per_km,
            xp
        ) = self.run_widget.get_results()

        self.player.add_run(
            distance,
            xp
        )

        save_player(self.player)

        save_run(
            duration_seconds,
            distance,
            pace_seconds_per_km,
            xp
        )

        self.result_widget.show_results(
            time,
            distance,
            pace,
            xp
        )

        manager.current = "result"

    def go_to_home(self, manager):

        self.home_widget.update_stats()

        manager.current = "home"

    def go_to_history(self, manager):

        self.history_widget.refresh()

        manager.current = "history"


if __name__ == "__main__":
    JogRApp().run()