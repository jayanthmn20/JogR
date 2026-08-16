import json
import os
import time

from jnius import autoclass, PythonJavaClass, java_method

from services.location_service import LocationService


class GPSRunnable(PythonJavaClass):

    __javainterfaces__ = [
        "java/lang/Runnable"
    ]

    def __init__(self, service):
        super().__init__()
        self.service = service

    @java_method("()V")
    def run(self):
        self.service.location_received()


class GPSForegroundService:

    def __init__(self):
        self.location_manager = None
        self.listener = None
        self.callback = None

        self.location_service = LocationService()

        PythonService = autoclass(
            "org.kivy.android.PythonService"
        )

        self.android_service = PythonService.mService

        self.state_file = os.path.join(
            self.android_service
            .getFilesDir()
            .getAbsolutePath(),
            "jogr_run_state.json"
        )

    def start(self):

        print("JogR GPS FOREGROUND SERVICE STARTING")

        self.location_service.start()

        self._write_state(
            running=True,
            distance=0.0
        )

        try:
            Context = autoclass(
                "android.content.Context"
            )

            LocationManager = autoclass(
                "android.location.LocationManager"
            )

            GPSListener = autoclass(
                "org.jogr.GPSListener"
            )

            Looper = autoclass(
                "android.os.Looper"
            )

            self.location_manager = (
                self.android_service.getSystemService(
                    Context.LOCATION_SERVICE
                )
            )

            self.callback = GPSRunnable(
                self
            )

            self.listener = GPSListener(
                self.callback
            )

            self.location_manager.requestLocationUpdates(
                LocationManager.GPS_PROVIDER,
                1000,
                1.0,
                self.listener,
                Looper.getMainLooper()
            )

            print("JogR GPS FOREGROUND SERVICE STARTED")

        except Exception as e:

            print(
                "GPS FOREGROUND SERVICE ERROR:",
                repr(e)
            )

            self._write_state(
                running=False,
                distance=0.0,
                error=str(e)
            )

            raise

    def location_received(self):

        if not self.listener:
            return

        latitude = self.listener.getLatitude()
        longitude = self.listener.getLongitude()

        speed = self.listener.getSpeed()
        bearing = self.listener.getBearing()
        altitude = self.listener.getAltitude()
        accuracy = self.listener.getAccuracy()

        self.location_service.update_location(
            latitude,
            longitude
        )

        distance = (
            self.location_service.get_distance()
        )

        print(
            f"JogR SERVICE LOCATION: "
            f"lat={latitude}, "
            f"lon={longitude}, "
            f"distance={distance:.5f} km, "
            f"accuracy={accuracy}"
        )

        self._write_state(
            running=True,
            latitude=latitude,
            longitude=longitude,
            speed=speed,
            bearing=bearing,
            altitude=altitude,
            accuracy=accuracy,
            distance=distance
        )

    def _write_state(self, running, distance, **kwargs):

        state = {
            "running": running,
            "distance_km": distance,
            "timestamp": time.time()
        }

        state.update(kwargs)

        temp_file = self.state_file + ".tmp"

        try:

            with open(
                temp_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    state,
                    file
                )

            os.replace(
                temp_file,
                self.state_file
            )

        except Exception as e:

            print(
                "GPS STATE WRITE ERROR:",
                repr(e)
            )

    def stop(self):

        print(
            "JogR GPS FOREGROUND SERVICE STOPPING"
        )

        try:

            if (
                self.location_manager
                and self.listener
            ):

                self.location_manager.removeUpdates(
                    self.listener
                )

        except Exception as e:

            print(
                "GPS REMOVE ERROR:",
                repr(e)
            )

        self.location_service.stop()

        self._write_state(
            running=False,
            distance=self.location_service.get_distance()
        )

        self.listener = None
        self.callback = None

        print(
            "JogR GPS FOREGROUND SERVICE STOPPED"
        )


service = GPSForegroundService()

service.start()

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    service.stop()
