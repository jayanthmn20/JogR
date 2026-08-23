from math import radians, sin, cos, sqrt, atan2


class LocationService:

    MIN_MOVEMENT_METERS = 5.0
    MAX_ACCURACY_METERS = 25.0

    def __init__(self):
        self.running = False
        self.last_location = None
        self.total_distance = 0.0

    def start(self):
        self.running = True
        self.last_location = None
        self.total_distance = 0.0

    def pause(self):
        self.running = False
        self.last_location = None

    def resume(self):
        self.running = True
        self.last_location = None

    def stop(self):
        self.running = False
        self.last_location = None

    def update_location(
        self,
        latitude,
        longitude,
        accuracy
    ):
        if not self.running:
            return

        if accuracy > self.MAX_ACCURACY_METERS:
            return

        current_location = (
            latitude,
            longitude
        )

        if self.last_location is None:
            self.last_location = current_location
            return

        distance = self._calculate_distance(
            self.last_location,
            current_location
        )

        self.last_location = current_location

        if distance * 1000 < self.MIN_MOVEMENT_METERS:
            return

        self.total_distance += distance

    def get_distance(self):
        return self.total_distance

    @staticmethod
    def _calculate_distance(
        location1,
        location2
    ):
        earth_radius = 6371.0

        lat1, lon1 = location1
        lat2, lon2 = location2

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        delta_lat = lat2 - lat1
        delta_lon = lon2 - lon1

        a = (
            sin(delta_lat / 2) ** 2
            + cos(lat1)
            * cos(lat2)
            * sin(delta_lon / 2) ** 2
        )

        c = 2 * atan2(
            sqrt(a),
            sqrt(1 - a)
        )

        return earth_radius * c
