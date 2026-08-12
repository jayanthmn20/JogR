from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class RunScreen(BoxLayout):

    def __init__(self, go_to_result_screen, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=50,
            spacing=30,
            **kwargs
        )

        self.seconds = 0

        title = Label(
            text="RUNNING",
            font_size=40
        )

        self.time_label = Label(
            text="00:00",
            font_size=40
        )

        self.distance_label = Label(
            text="Distance: 0.00 km",
            font_size=25
        )

        self.pace_label = Label(
            text="Pace: --:-- /km",
            font_size=25
        )

        stop_button = Button(
            text="STOP RUN",
            font_size=25
        )

        stop_button.bind(
            on_press=go_to_result_screen
        )

        self.add_widget(title)
        self.add_widget(self.time_label)
        self.add_widget(self.distance_label)
        self.add_widget(self.pace_label)
        self.add_widget(stop_button)

    def start_timer(self):
        self.seconds = 0

        self.update_time(0)

        Clock.unschedule(self.update_time)

        Clock.schedule_interval(
            self.update_time,
            1
        )

    def stop_timer(self):
        Clock.unschedule(self.update_time)

    def update_time(self, dt):
        self.seconds += 1

        minutes = self.seconds // 60
        seconds = self.seconds % 60

        self.time_label.text = (
            f"{minutes:02d}:{seconds:02d}"
        )