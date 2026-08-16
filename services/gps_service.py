import json
import os

from android.permissions import request_permissions, Permission
from jnius import autoclass
from kivy.clock import Clock


class GPSService:

    def __init__(self, on_location=None):
        self.on_location = on_location
        self.running = False
        self.distance = 0.0

        self.state_file = None
        self._poll_event = None

    def start(self):

        request_permissions(
            [
                Permission.ACCESS_FINE_LOCATION,
                Permission.ACCESS_COARSE_LOCATION
            ],
            self._permission_callback
        )

    def _permission_callback(self, permissions, grants):

        if not all(grants):
            print("GPS PERMISSION DENIED")
            return

        print("GPS PERMISSION GRANTED")

        Clock.schedule_once(
            self._start_foreground_service,
            0.5
        )

    def _start_foreground_service(self, dt):

        try:

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            ServiceGPS = autoclass(
                "com.jayanth.jogr.ServiceGpsforeground"
            )

            activity = PythonActivity.mActivity

            ServiceGPS.start(
                activity,
                ""
            )

            files_dir = (
                activity.getFilesDir()
                .getAbsolutePath()
            )

            self.state_file = os.path.join(
                files_dir,
                "jogr_run_state.json"
            )

            self.running = True
            self.distance = 0.0

            print(
                "GPS FOREGROUND SERVICE STARTED"
            )

            Clock.unschedule(
                self._poll_state
            )

            self._poll_event = Clock.schedule_interval(
                self._poll_state,
                1
            )

        except Exception as e:

            print(
                "GPS FOREGROUND SERVICE START ERROR:",
                repr(e)
            )

    def _poll_state(self, dt):

        if not self.running:
            return

        if not self.state_file:
            return

        try:

            if not os.path.exists(
                self.state_file
            ):
                return

            with open(
                self.state_file,
                "r",
                encoding="utf-8"
            ) as file:

                state = json.load(file)

            self.distance = float(
                state.get(
                    "distance_km",
                    self.distance
                )
            )

            if self.on_location:

                latitude = state.get(
                    "latitude"
                )

                longitude = state.get(
                    "longitude"
                )

                if (
                    latitude is not None
                    and longitude is not None
                ):

                    self.on_location(
                        lat=latitude,
                        lon=longitude,
                        speed=state.get(
                            "speed",
                            0.0
                        ),
                        bearing=state.get(
                            "bearing",
                            0.0
                        ),
                        altitude=state.get(
                            "altitude",
                            0.0
                        ),
                        accuracy=state.get(
                            "accuracy",
                            0.0
                        )
                    )

        except Exception as e:

            print(
                "GPS STATE READ ERROR:",
                repr(e)
            )

    def get_distance(self):

        self._read_state()

        return self.distance

    def _read_state(self):

        if not self.state_file:
            return

        try:

            if not os.path.exists(
                self.state_file
            ):
                return

            with open(
                self.state_file,
                "r",
                encoding="utf-8"
            ) as file:

                state = json.load(file)

            self.distance = float(
                state.get(
                    "distance_km",
                    self.distance
                )
            )

        except Exception as e:

            print(
                "GPS DISTANCE READ ERROR:",
                repr(e)
            )

    def stop(self):

        if self._poll_event:
            self._poll_event.cancel()
            self._poll_event = None

        Clock.unschedule(
            self._poll_state
        )

        try:

            if self.running:

                PythonActivity = autoclass(
                    "org.kivy.android.PythonActivity"
                )

                Intent = autoclass(
                    "android.content.Intent"
                )

                ServiceGPS = autoclass(
                    "com.jayanth.jogr.ServiceGpsforeground"
                )

                activity = PythonActivity.mActivity

                intent = Intent(
                    activity,
                    ServiceGPS
                )

                activity.stopService(intent)

                print(
                    "GPS FOREGROUND SERVICE STOPPED"
                )

        except Exception as e:

            print(
                "GPS FOREGROUND SERVICE STOP ERROR:",
                repr(e)
            )

        self._read_state()

        self.running = False
