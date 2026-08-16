from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass

from services.gps_service import GPSService


class RunScreen(BoxLayout):

    def __init__(self, go_to_result_screen, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=50,
            spacing=30,
            **kwargs
        )

        self.seconds = 0
        self.distance = 0.0
        self.start_time_ms = None

        self.gps_service = GPSService(
            on_location=self.on_location
        )

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
        self.distance = 0.0

        SystemClock = autoclass(
            "android.os.SystemClock"
        )

        self.start_time_ms = (
            SystemClock.elapsedRealtime()
        )

        self.gps_service.start()

        self.update_time(0)

        Clock.unschedule(
            self.update_time
        )

        Clock.schedule_interval(
            self.update_time,
            1
        )

    def stop_timer(self):

        self.update_time(0)

        Clock.unschedule(
            self.update_time
        )

        self.gps_service.stop()

        self.distance = (
            self.gps_service.get_distance()
        )

    def on_location(self, **kwargs):

        print(
            "GPS LOCATION:",
            kwargs
        )

        self.distance = (
            self.gps_service.get_distance()
        )

    def update_time(self, dt):

        if self.start_time_ms is None:
            return

        SystemClock = autoclass(
            "android.os.SystemClock"
        )

        current_time_ms = (
            SystemClock.elapsedRealtime()
        )

        self.seconds = int(
            (
                current_time_ms
                - self.start_time_ms
            ) / 1000
        )

        minutes = self.seconds // 60
        seconds = self.seconds % 60

        self.time_label.text = (
            f"{minutes:02d}:{seconds:02d}"
        )

        self.distance = (
            self.gps_service.get_distance()
        )

        self.distance_label.text = (
            f"Distance: {self.distance:.2f} km"
        )

        if self.distance > 0:

            pace = (
                self.seconds
                / self.distance
            )

            pace_minutes = int(
                pace // 60
            )

            pace_seconds = int(
                pace % 60
            )

            self.pace_label.text = (
                f"Pace: {pace_minutes:02d}:"
                f"{pace_seconds:02d} /km"
            )

    def get_results(self):

        minutes = self.seconds // 60
        seconds = self.seconds % 60

        time = (
            f"{minutes:02d}:{seconds:02d}"
        )

        if self.distance > 0:

            pace = (
                self.seconds
                / self.distance
            )

            pace_minutes = int(
                pace // 60
            )

            pace_seconds = int(
                pace % 60
            )

            pace_text = (
                f"{pace_minutes:02d}:"
                f"{pace_seconds:02d} /km"
            )

        else:

            pace_text = "--:-- /km"

        xp = int(
            self.distance * 100
        )

        return (
            time,
            self.distance,
            pace_text,
            xp
        )