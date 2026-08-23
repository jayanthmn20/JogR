class Player:

    def __init__(self, name="Jayanth"):
        self.name = name
        self.level = 1
        self.xp = 0
        self.total_xp = 0
        self.total_distance = 0.0
        self.total_runs = 0
        self.achievements = []

    @staticmethod
    def calculate_run_xp(distance):

        return int(
            distance * 50
        )


    def add_run(self, distance, xp):

        self.total_distance += distance
        self.total_runs += 1

        return self.add_xp(xp)

    def add_xp(self, xp):

        old_level = self.level

        self.xp += xp
        self.total_xp += xp

        while self.xp >= self.xp_required():

            self.xp -= self.xp_required()
            self.level += 1

        return {
            "old_level": old_level,
            "new_level": self.level,
            "level_up": self.level > old_level
        }

    def xp_required(self):

        return self.level * 100
