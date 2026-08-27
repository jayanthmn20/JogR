class Player:

    def __init__(self, name="Jayanth"):
        self.name = name
        self.level = 1
        self.xp = 0
        self.total_xp = 0
        self.total_distance = 0.0
        self.total_runs = 0
        self.achievements = []
        self.mission_claims = {}
        self.streak_rewards = []

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

    def is_mission_claimed(
        self,
        date_text,
        mission_id
    ):

        claimed = self.mission_claims.get(
            date_text,
            []
        )

        return mission_id in claimed

    def claim_mission(
        self,
        date_text,
        mission_id
    ):

        if self.is_mission_claimed(
            date_text,
            mission_id
        ):
            return False

        if date_text not in self.mission_claims:
            self.mission_claims[date_text] = []

        self.mission_claims[date_text].append(
            mission_id
        )

        return True

    def is_streak_reward_claimed(
            self,
            milestone
    ):
        return milestone in self.streak_rewards

    def claim_streak_reward(
            self,
            milestone
    ):

        if self.is_streak_reward_claimed(
            milestone
        ):
            return False

        self.streak_rewards.append(
            milestone
        )

        return True
