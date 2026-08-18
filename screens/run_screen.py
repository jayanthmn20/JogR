from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from jnius import autoclass

from services.gps_service import GPSService


class RunScreen(BoxLayout):

    def __init__(
        self,
        go_to_result_screen,
        **kwargs
    ):

        super().__init__(
            orientation="vertical",
            padding=50,
            spacing=20,
            **kwargs
        )

        self.seconds = 0
        self.distance = 0.0

        self.start_time_ms = None
        self.pause_start_ms = None
        self.paused_total_ms = 0

        self.is_paused = False

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

        self.pause_button = Button(
            text="PAUSE RUN",
            font_size=25
        )

        self.pause_button.bind(
            on_press=self.toggle_pause
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
        self.add_widget(self.pause_button)
        self.add_widget(stop_button)

    def start_timer(self):

        self.seconds = 0
        self.distance = 0.0

        self.start_time_ms = None
        self.pause_start_ms = None
        self.paused_total_ms = 0

        self.is_paused = False

        self.pause_button.text = (
            "PAUSE RUN"
        )

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

    def toggle_pause(self, instance):

        if self.is_paused:

            self.resume_run()

        else:

            self.pause_run()

    def pause_run(self):

        if self.is_paused:
            return

        SystemClock = autoclass(
            "android.os.SystemClock"
        )

        self.pause_start_ms = (
            SystemClock.elapsedRealtime()
        )

        self.is_paused = True

        self.gps_service.pause()

        Clock.unschedule(
            self.update_time
        )

        self.pause_button.text = (
            "RESUME RUN"
        )

        print(
            "JogR RUN PAUSED"
        )

    def resume_run(self):

        if not self.is_paused:
            return

        SystemClock = autoclass(
            "android.os.SystemClock"
        )

        current_time_ms = (
            SystemClock.elapsedRealtime()
        )

        if self.pause_start_ms is not None:

            self.paused_total_ms += (
                current_time_ms
                - self.pause_start_ms
            )

        self.pause_start_ms = None

        self.is_paused = False

        self.gps_service.resume()

        self.pause_button.text = (
            "PAUSE RUN"
        )

        self.update_time(0)

        Clock.unschedule(
            self.update_time
        )

        Clock.schedule_interval(
            self.update_time,
            1
        )

        print(
            "JogR RUN RESUMED"
        )

    def stop_timer(self):

        if self.is_paused:

            SystemClock = autoclass(
                "android.os.SystemClock"
            )

            current_time_ms = (
                SystemClock.elapsedRealtime()
            )

            if self.pause_start_ms is not None:

                self.paused_total_ms += (
                    current_time_ms
                    - self.pause_start_ms
                )

            self.pause_start_ms = None
            self.is_paused = False

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

        if self.is_paused:
            return

        SystemClock = autoclass(
            "android.os.SystemClock"
        )

        current_time_ms = (
            SystemClock.elapsedRealtime()
        )

        active_time_ms = (
            current_time_ms
            - self.start_time_ms
            - self.paused_total_ms
        )

        self.seconds = max(
            0,
            int(active_time_ms / 1000)
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
            f"Distance: "
            f"{self.distance:.2f} km"
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
                f"Pace: "
                f"{pace_minutes:02d}:"
                f"{pace_seconds:02d} /km"
            )

        else:

            self.pace_label.text = (
                "Pace: --:-- /km"
            )

    def get_results(self):

        minutes = self.seconds // 60
        seconds = self.seconds % 60

        time = (
            f"{minutes:02d}:{seconds:02d}"
        )

        pace_seconds_per_km = None

        if self.distance > 0:

            pace_seconds_per_km = (
                self.seconds
                / self.distance
            )

            pace_minutes = int(
                pace_seconds_per_km // 60
            )

            pace_seconds = int(
                pace_seconds_per_km % 60
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
            self.seconds,
            self.distance,
            pace_text,
            pace_seconds_per_km,
            xp
        )
