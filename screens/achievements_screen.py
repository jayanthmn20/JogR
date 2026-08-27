from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from models.achievements import Achievement
from services.storage import get_streaks


class AchievementsScreen(BoxLayout):

    def __init__(
        self,
        player,
        go_to_home_screen,
        **kwargs
    ):
        super().__init__(
            orientation="vertical",
            padding=30,
            spacing=15,
            **kwargs
        )

        self.player = player

        title = Label(
            text="ACHIEVEMENTS",
            font_size=40,
            size_hint_y=None,
            height=60
        )

        self.achievement_layout = BoxLayout(
            orientation="vertical",
            spacing=15,
            size_hint_y=None
        )

        self.achievement_layout.bind(
            minimum_height=self.achievement_layout.setter(
                "height"
            )
        )

        scroll = ScrollView()

        scroll.add_widget(
            self.achievement_layout
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

        self.refresh()

    def refresh(self):

        self.achievement_layout.clear_widgets()

        unlocked_ids = set(
            self.player.achievements
        )

        current_streak, _ = get_streaks()

        for achievement in Achievement.DEFINITIONS:

            achievement_id = achievement["id"]

            if achievement_id in unlocked_ids:

                status = "UNLOCKED"
                progress = ""

            else:

                status = "LOCKED"
                progress = self._get_progress(
                    achievement_id,
                    current_streak
                )

            text = (
                f"{status}\n"
                f"{achievement['title']}\n"
                f"{achievement['description']}"
            )

            if progress:
                text += f"\n{progress}"

            label = Label(
                text=text,
                font_size=20,
                halign="left",
                valign="middle",
                size_hint_y=None,
                height=120 if progress else 100
            )

            label.bind(
                size=lambda instance, value: setattr(
                    instance,
                    "text_size",
                    (value[0], None)
                )
            )

            self.achievement_layout.add_widget(
                label
            )

    def _get_progress(
        self,
        achievement_id,
        current_streak
    ):

        if achievement_id == "first_run":

            return (
                f"Progress: "
                f"{self.player.total_runs} / 1 run"
            )

        if achievement_id == "getting_started":

            return (
                f"Progress: "
                f"{self.player.total_distance:.2f} / 5.00 km"
            )

        if achievement_id == "road_runner":

            return (
                f"Progress: "
                f"{self.player.total_distance:.2f} / 10.00 km"
            )

        if achievement_id == "xp_hunter":

            return (
                f"Progress: "
                f"{self.player.total_xp} / 500 XP"
            )

        if achievement_id == "on_fire":

            return (
                f"Progress: "
                f"{min(current_streak, 3)} / 3 days"
            )

        return ""
