from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from services.storage import load_runs, get_streaks


class StatsScreen(BoxLayout):

    def __init__(self, go_to_home_screen, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=40,
            spacing=20,
            **kwargs
        )

        title = Label(
            text="STATISTICS",
            font_size=40,
            size_hint_y=None,
            height=60
        )

        self.runs_label = Label(
            font_size=24
        )

        self.distance_label = Label(
            font_size=24
        )

        self.time_label = Label(
            font_size=24
        )

        self.average_pace_label = Label(
            font_size=24
        )

        self.best_pace_label = Label(
            font_size=24
        )

        self.longest_run_label = Label(
            font_size=24
        )

        self.xp_label = Label(
            font_size=24
        )

        self.current_streak_label = Label(
            font_size=24
        )

        self.best_streak_label = Label(
            font_size=24
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
        self.add_widget(self.runs_label)
        self.add_widget(self.distance_label)
        self.add_widget(self.time_label)
        self.add_widget(self.average_pace_label)
        self.add_widget(self.best_pace_label)
        self.add_widget(self.longest_run_label)
        self.add_widget(self.xp_label)
        self.add_widget(home_button)
        self.add_widget(self.current_streak_label)
        self.add_widget(self.best_streak_label)


        self.refresh()

    def refresh(self):

        runs = load_runs()
        current_streak, best_streak = get_streaks()

        current_unit = (
            "DAY"
            if current_streak == 1
            else "DAYS"
        )

        best_unit = (
            "DAY"
            if best_streak == 1
            else "DAYS"
        )

        self.current_streak_label.text = (
            f"CURRENT STREAK: "
            f"{current_streak} {current_unit}"
        )

        self.best_streak_label.text = (
            f"BEST STREAK: "
            f"{best_streak} {best_unit}"
        )


        if not runs:

            self.runs_label.text = "RUNS: 0"
            self.distance_label.text = "DISTANCE: 0.00 km"
            self.time_label.text = "TOTAL TIME: 00:00"
            self.average_pace_label.text = (
                "AVERAGE PACE: --:-- /km"
            )
            self.best_pace_label.text = (
                "BEST PACE: --:-- /km"
            )
            self.longest_run_label.text = (
                "LONGEST RUN: 0.00 km"
            )
            self.xp_label.text = "TOTAL XP: 0"

            return

        total_runs = len(runs)

        total_distance = 0.0
        total_seconds = 0
        total_xp = 0

        valid_paces = []
        longest_distance = 0.0

        for run in runs:

            distance = float(
                run.get(
                    "distance_km",
                    0.0
                )
            )

            duration = int(
                run.get(
                    "duration_seconds",
                    0
                )
            )

            xp = int(
                run.get(
                    "xp",
                    0
                )
            )

            pace = run.get(
                "pace_seconds_per_km"
            )

            total_distance += distance
            total_seconds += duration
            total_xp += xp

            if distance > longest_distance:
                longest_distance = distance

            if pace is not None and distance > 0:
                valid_paces.append(
                    float(pace)
                )

        total_minutes = total_seconds // 60
        remaining_seconds = total_seconds % 60

        if valid_paces:

            if total_distance > 0:

                average_pace = (
                    total_seconds
                    / total_distance
                )

            else:

                average_pace = None

            best_pace = min(
                valid_paces
            )

            average_pace_text = (
                self._format_pace(
                    average_pace
                )
                if average_pace is not None
                else "--:-- /km"
            )

            best_pace_text = (
                self._format_pace(
                    best_pace
                )
            )

        else:

            average_pace_text = "--:-- /km"
            best_pace_text = "--:-- /km"

        self.runs_label.text = (
            f"RUNS: {total_runs}"
        )

        self.distance_label.text = (
            f"DISTANCE: "
            f"{total_distance:.2f} km"
        )

        self.time_label.text = (
            f"TOTAL TIME: "
            f"{total_minutes:02d}:"
            f"{remaining_seconds:02d}"
        )

        self.average_pace_label.text = (
            f"AVERAGE PACE: "
            f"{average_pace_text}"
        )

        self.best_pace_label.text = (
            f"BEST PACE: "
            f"{best_pace_text}"
        )

        self.longest_run_label.text = (
            f"LONGEST RUN: "
            f"{longest_distance:.2f} km"
        )

        self.xp_label.text = (
            f"TOTAL XP: {total_xp}"
        )

    @staticmethod
    def _format_pace(
        pace_seconds
    ):

        pace_minutes = int(
            pace_seconds // 60
        )

        remaining_seconds = int(
            pace_seconds % 60
        )

        return (
            f"{pace_minutes:02d}:"
            f"{remaining_seconds:02d} /km"
        )
