class Achievement:

    DEFINITIONS = [
        {
            "id": "first_run",
            "title": "FIRST RUN",
            "description": "Complete your first run.",
        },
        {
            "id": "getting_started",
            "title": "GETTING STARTED",
            "description": "Reach 5 km total distance.",
        },
        {
            "id": "road_runner",
            "title": "ROAD RUNNER",
            "description": "Reach 10 km total distance.",
        },
        {
            "id": "xp_hunter",
            "title": "XP HUNTER",
            "description": "Earn 500 total XP.",
        },
        {
            "id": "on_fire",
            "title": "ON FIRE",
            "description": "Reach a 3-day running streak.",
        },
    ]

    @classmethod
    def check_unlocked(
        cls,
        player,
        current_streak
    ):
        unlocked = []

        for achievement in cls.DEFINITIONS:

            achievement_id = achievement["id"]

            if achievement_id == "first_run":
                is_unlocked = (
                    player.total_runs >= 1
                )

            elif achievement_id == "getting_started":
                is_unlocked = (
                    player.total_distance >= 5
                )

            elif achievement_id == "road_runner":
                is_unlocked = (
                    player.total_distance >= 10
                )

            elif achievement_id == "xp_hunter":
                is_unlocked = (
                    player.total_xp >= 500
                )

            elif achievement_id == "on_fire":
                is_unlocked = (
                    current_streak >= 3
                )

            else:
                is_unlocked = False

            if is_unlocked:
                unlocked.append(achievement)

        return unlocked
