from math import radians, sin, cos, sqrt, atan2


class LocationService:

    def __init__(self):
        self.running = False
        self.last_location = None
        self.total_distance = 0.0

    def start(self):
        self.running = True
        self.last_location = None
        self.total_distance = 0.0

    def stop(self):
        self.running = False
        self.last_location = None

    def update_location(self, latitude, longitude):
        if not self.running:
            return

        current_location = (latitude, longitude)

        if self.last_location is not None:
            distance = self._calculate_distance(
                self.last_location,
                current_location
            )

            self.total_distance += distance

        self.last_location = current_location

    def get_distance(self):
        return self.total_distance

    @staticmethod
    def _calculate_distance(location1, location2):
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

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return earth_radius * c