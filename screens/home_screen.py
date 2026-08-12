from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class HomeScreen(BoxLayout):

    def __init__(self, player, go_to_run_screen, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=50,
            spacing=20,
            **kwargs
        )

        self.player = player

        self.title = Label(
            text="JogR",
            font_size=50
        )

        self.level_label = Label(
            font_size=25
        )

        self.xp_label = Label(
            font_size=22
        )

        self.runs_label = Label(
            font_size=20
        )

        self.distance_label = Label(
            font_size=20
        )

        start_button = Button(
            text="START RUN",
            font_size=25
        )

        start_button.bind(
            on_press=go_to_run_screen
        )

        self.add_widget(self.title)
        self.add_widget(self.level_label)
        self.add_widget(self.xp_label)
        self.add_widget(start_button)
        self.add_widget(self.runs_label)
        self.add_widget(self.distance_label)

        self.update_stats()

    def update_stats(self):

        self.level_label.text = (
            f"LEVEL {self.player.level}"
        )

        self.xp_label.text = (
            f"{self.player.xp} / "
            f"{self.player.xp_required()} XP"
        )

        self.runs_label.text = (
            f"RUNS: {self.player.total_runs}"
        )

        self.distance_label.text = (
            f"DISTANCE: "
            f"{self.player.total_distance:.2f} km"
        )