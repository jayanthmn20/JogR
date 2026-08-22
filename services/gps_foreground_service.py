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

        self.paused = False

        PythonService = autoclass(
            "org.kivy.android.PythonService"
        )

        self.android_service = PythonService.mService

        files_dir = (
            self.android_service
            .getFilesDir()
            .getAbsolutePath()
        )

        self.state_file = os.path.join(
            files_dir,
            "jogr_run_state.json"
        )

        self.control_file = os.path.join(
            files_dir,
            "jogr_run_control.json"
        )

    def start(self):

        print(
            "JogR GPS FOREGROUND SERVICE STARTING"
        )

        self.paused = False

        self.location_service.start()

        self._write_control(
            paused=False
        )

        self._write_state(
            running=True,
            paused=False,
            distance=0.0
        )

        self._start_location_updates()

    def _start_location_updates(self):

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
                self.android_service
                .getSystemService(
                    Context.LOCATION_SERVICE
                )
            )

            if self.callback is None:

                self.callback = GPSRunnable(
                    self
                )

            if self.listener is None:

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

            print(
                "JogR GPS LOCATION UPDATES STARTED"
            )

        except Exception as e:

            print(
                "JogR GPS FOREGROUND SERVICE ERROR:",
                repr(e)
            )

            self._write_state(
                running=False,
                paused=False,
                distance=self.location_service.get_distance(),
                error=str(e)
            )

            raise

    def _stop_location_updates(self):

        try:

            if (
                self.location_manager
                and self.listener
            ):

                self.location_manager.removeUpdates(
                    self.listener
                )

                print(
                    "JogR GPS LOCATION UPDATES PAUSED"
                )

        except Exception as e:

            print(
                "JogR GPS REMOVE ERROR:",
                repr(e)
            )

    def location_received(self):

        if not self.listener:
            return

        self._check_control()

        if self.paused:
            return

        latitude = (
            self.listener.getLatitude()
        )

        longitude = (
            self.listener.getLongitude()
        )

        speed = (
            self.listener.getSpeed()
        )

        bearing = (
            self.listener.getBearing()
        )

        altitude = (
            self.listener.getAltitude()
        )

        accuracy = (
            self.listener.getAccuracy()
        )

        self.location_service.update_location(
            latitude,
            longitude,
            accuracy
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
            paused=False,
            latitude=latitude,
            longitude=longitude,
            speed=speed,
            bearing=bearing,
            altitude=altitude,
            accuracy=accuracy,
            distance=distance
        )

    def pause(self):

        if self.paused:
            return

        print(
            "JogR GPS FOREGROUND SERVICE PAUSING"
        )

        self.paused = True

        self.location_service.pause()

        self._stop_location_updates()

        self._write_control(
            paused=True
        )

        self._write_state(
            running=True,
            paused=True,
            distance=self.location_service.get_distance()
        )

        print(
            "JogR GPS FOREGROUND SERVICE PAUSED"
        )

    def resume(self):

        if not self.paused:
            return

        print(
            "JogR GPS FOREGROUND SERVICE RESUMING"
        )

        self.paused = False

        self.location_service.resume()

        self._write_control(
            paused=False
        )

        self._start_location_updates()

        self._write_state(
            running=True,
            paused=False,
            distance=self.location_service.get_distance()
        )

        print(
            "JogR GPS FOREGROUND SERVICE RESUMED"
        )

    def _check_control(self):

        try:

            if not os.path.exists(
                self.control_file
            ):
                return

            with open(
                self.control_file,
                "r",
                encoding="utf-8"
            ) as file:

                control = json.load(file)

            paused = bool(
                control.get(
                    "paused",
                    False
                )
            )

            if paused and not self.paused:
                self.pause()

            elif not paused and self.paused:
                self.resume()

        except Exception as e:

            print(
                "JogR GPS CONTROL READ ERROR:",
                repr(e)
            )

    def _write_control(self, paused):

        control = {
            "paused": paused,
            "timestamp": time.time()
        }

        temp_file = (
            self.control_file
            + ".tmp"
        )

        try:

            with open(
                temp_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    control,
                    file
                )

            os.replace(
                temp_file,
                self.control_file
            )

        except Exception as e:

            print(
                "JogR GPS CONTROL WRITE ERROR:",
                repr(e)
            )

    def _write_state(
        self,
        running,
        paused,
        distance,
        **kwargs
    ):

        state = {
            "running": running,
            "paused": paused,
            "distance_km": distance,
            "timestamp": time.time()
        }

        state.update(kwargs)

        temp_file = (
            self.state_file
            + ".tmp"
        )

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
                "JogR GPS STATE WRITE ERROR:",
                repr(e)
            )

    def stop(self):

        print(
            "JogR GPS FOREGROUND SERVICE STOPPING"
        )

        self._stop_location_updates()

        self.location_service.stop()

        final_distance = (
            self.location_service.get_distance()
        )

        self._write_state(
            running=False,
            paused=False,
            distance=final_distance
        )

        self._write_control(
            paused=False
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

        service._check_control()

        time.sleep(1)

except KeyboardInterrupt:

    service.stop()
