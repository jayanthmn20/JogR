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
        self.add_widget(home_button)

    def show_results(self, time, distance, pace, xp):

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