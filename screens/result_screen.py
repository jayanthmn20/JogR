from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class ResultScreen(BoxLayout):

    def __init__(self, go_to_home_screen, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=50,
            spacing=20,
            **kwargs
        )

        title = Label(
            text="RUN COMPLETE!",
            font_size=40
        )

        self.time_label = Label(
            text="Time: 00:00",
            font_size=25
        )

        self.distance_label = Label(
            text="Distance: 0.00 km",
            font_size=25
        )

        self.pace_label = Label(
            text="Pace: --:-- /km",
            font_size=25
        )

        self.xp_label = Label(
            text="XP Earned: 0",
            font_size=25
        )

        self.level_up_label = Label(
            text="",
            font_size=28
        )

        self.level_label = Label(
            text="",
            font_size=25
        )

        self.xp_progress_label = Label(
            text="",
            font_size=22
        )

        self.xp_remaining_label = Label(
            text="",
            font_size=20
        )

        self.achievement_label = Label(
            text="",
            font_size=22
        )

        home_button = Button(
            text="BACK TO HOME",
            font_size=25
        )

        home_button.bind(
            on_press=go_to_home_screen
        )

        self.add_widget(title)
        self.add_widget(self.time_label)
        self.add_widget(self.distance_label)
        self.add_widget(self.pace_label)
        self.add_widget(self.xp_label)
        self.add_widget(self.level_up_label)
        self.add_widget(self.level_label)
        self.add_widget(self.xp_progress_label)
        self.add_widget(self.xp_remaining_label)
        self.add_widget(self.achievement_label)
        self.add_widget(home_button)

    def show_results(
            self,
            time,
            distance,
            pace,
            xp,
            level_result,
            level,
            current_xp,
            xp_required,
            new_achievements
    ):

        self.time_label.text = (
            f"Time: {time}"
        )

        self.distance_label.text = (
            f"Distance: {distance:.2f} km"
        )

        self.pace_label.text = (
            f"Pace: {pace}"
        )

        self.xp_label.text = (
            f"XP Earned: +{xp}"
        )

        if level_result["level_up"]:
            self.level_up_label.text = (
                f"LEVEL UP! "
                f"{level_result['old_level']} "
                f"→ "
                f"{level_result['new_level']}"
            )

        else:

            self.level_up_label.text = ""

        self.level_label.text = (
            f"LEVEL {level}"
        )

        self.xp_progress_label.text = (
            f"{current_xp} / {xp_required} XP"
        )

        remaining_xp = (
            xp_required - current_xp
        )

        self.xp_remaining_label.text = (
            f"{remaining_xp} XP TO LEVEL "
            f"{level + 1}"
        )

        if new_achievements:

            achievement = new_achievements[0]

            self.achievement_label.text = (
                f"ACHIEVEMENT UNLOCKED!\n"
                f"{achievement['title']}\n"
                f"{achievement['description']}"
            )

        else:

            self.achievement_label.text = ""
