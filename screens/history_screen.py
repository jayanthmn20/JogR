from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from services.storage import load_runs


class HistoryScreen(BoxLayout):

    def __init__(self, go_to_home_screen, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=30,
            spacing=15,
            **kwargs
        )

        title = Label(
            text="RUN HISTORY",
            font_size=40,
            size_hint_y=None,
            height=60
        )

        self.history_layout = BoxLayout(
            orientation="vertical",
            spacing=15,
            size_hint_y=None
        )

        self.history_layout.bind(
            minimum_height=self.history_layout.setter(
                "height"
            )
        )

        scroll = ScrollView()

        scroll.add_widget(
            self.history_layout
        )

        home_button = Button(
            text="BACK TO HOME",
            font_size=22,
            size_hint_y=None,
            height=60
        )

        home_button.bind(
            on_press=go_to_home_screen
        )

        self.add_widget(title)
        self.add_widget(scroll)
        self.add_widget(home_button)

    def refresh(self):

        self.history_layout.clear_widgets()

        runs = load_runs()

        if not runs:

            self.history_layout.add_widget(
                Label(
                    text="No runs yet.",
                    font_size=24,
                    size_hint_y=None,
                    height=60
                )
            )

            return

        for run in reversed(runs):

            duration_seconds = int(
                run.get(
                    "duration_seconds",
                    0
                )
            )

            minutes = duration_seconds // 60
            seconds = duration_seconds % 60

            distance = float(
                run.get(
                    "distance_km",
                    0.0
                )
            )

            pace_seconds = run.get(
                "pace_seconds_per_km"
            )

            if pace_seconds is not None:

                pace_seconds = float(
                    pace_seconds
                )

                pace_minutes = int(
                    pace_seconds // 60
                )

                pace_remaining = int(
                    pace_seconds % 60
                )

                pace = (
                    f"{pace_minutes:02d}:"
                    f"{pace_remaining:02d} /km"
                )

            else:

                pace = "--:-- /km"

            xp = int(
                run.get(
                    "xp",
                    0
                )
            )

            date = run.get(
                "date",
                "Unknown date"
            )

            run_label = Label(
                text=(
                    f"{date}\n"
                    f"Time: {minutes:02d}:{seconds:02d}    "
                    f"Distance: {distance:.2f} km\n"
                    f"Pace: {pace}    "
                    f"XP: +{xp}"
                ),
                font_size=18,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=100
            )

            run_label.bind(
                size=lambda instance, value: setattr(
                    instance,
                    "text_size",
                    (value[0], None)
                )
            )

            self.history_layout.add_widget(
                run_label
            )
