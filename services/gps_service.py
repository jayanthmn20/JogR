from android.permissions import request_permissions, Permission
from jnius import autoclass, PythonJavaClass, java_method
from kivy.clock import Clock


class GPSRunnable(PythonJavaClass):

    __javainterfaces__ = [
        "java/lang/Runnable"
    ]

    def __init__(self, gps_service):
        super().__init__()
        self.gps_service = gps_service

    @java_method("()V")
    def run(self):
        self.gps_service._location_received()


class GPSService:

    def __init__(self, on_location):
        self.on_location = on_location

        self.location_manager = None
        self.listener = None
        self.callback = None

        self.running = False

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
            self._start_gps,
            0.5
        )

    def _start_gps(self, dt):

        try:
            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

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

            activity = PythonActivity.mActivity

            self.location_manager = (
                activity.getSystemService(
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

            self.running = True

            print("GPS STARTED")

        except Exception as e:

            print(
                "GPS START ERROR:",
                repr(e)
            )

    def _location_received(self):

        if not self.listener:
            return

        latitude = self.listener.getLatitude()
        longitude = self.listener.getLongitude()
        speed = self.listener.getSpeed()
        bearing = self.listener.getBearing()
        altitude = self.listener.getAltitude()
        accuracy = self.listener.getAccuracy()

        print(
            f"GPS LOCATION: "
            f"lat={latitude}, "
            f"lon={longitude}, "
            f"accuracy={accuracy}"
        )

        self.on_location(
            lat=latitude,
            lon=longitude,
            speed=speed,
            bearing=bearing,
            altitude=altitude,
            accuracy=accuracy
        )

    def stop(self):

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
                "GPS STOP ERROR:",
                repr(e)
            )

        self.running = False
        self.listener = None
        self.callback = None

        print("GPS STOPPED")
