class Player:

    def __init__(self, name="Jayanth"):
        self.name = name
        self.level = 1
        self.xp = 0
        self.total_distance = 0.0
        self.total_runs = 0

    def add_run(self, distance, xp):

        self.total_distance += distance
        self.total_runs += 1

        self.add_xp(xp)

    def add_xp(self, xp):

        self.xp += xp

        while self.xp >= self.xp_required():

            self.xp -= self.xp_required()
            self.level += 1

    def xp_required(self):

        return self.level * 100