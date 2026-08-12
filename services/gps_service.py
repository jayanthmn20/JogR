from plyer import gps
from android.permissions import request_permissions, Permission


class GPSService:

    def __init__(self, on_location):
        self.on_location = on_location

    def start(self):
        request_permissions([
            Permission.ACCESS_FINE_LOCATION,
            Permission.ACCESS_COARSE_LOCATION
        ])

        gps.configure(
            on_location=self.on_location
        )

        gps.start(
            minTime=1000,
            minDistance=1
        )

    def stop(self):
        gps.stop()