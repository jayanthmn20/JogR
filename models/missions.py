from datetime import datetime


class Mission:

    DEFINITIONS = [
        {
            "id": "first_step",
            "title": "FIRST STEP",
            "description": "Run 1 km today.",
            "type": "distance",
            "target": 1.0,
            "reward": 50,
        },
        {
            "id": "keep_moving",
            "title": "KEEP MOVING",
            "description": "Run for 10 minutes today.",
            "type": "duration",
            "target": 600,
            "reward": 75,
        },
        {
            "id": "daily_runner",
            "title": "DAILY RUNNER",
            "description": "Complete 1 run today.",
            "type": "runs",
            "target": 1,
            "reward": 100,
        },
    ]

    @classmethod
    def today(cls):
        return datetime.now().strftime("%Y-%m-%d")

    @classmethod
    def calculate_progress(cls, mission_id, runs):

        today = cls.today()

        today_runs = []

        for run in runs:

            date_text = run.get("date", "")

            if date_text.startswith(today):
                today_runs.append(run)

        for mission in cls.DEFINITIONS:

            if mission["id"] != mission_id:
                continue

            if mission["type"] == "distance":

                return sum(
                    run.get("distance_km", 0)
                    for run in today_runs
                )

            if mission["type"] == "duration":

                return sum(
                    run.get("duration_seconds", 0)
                    for run in today_runs
                )

            if mission["type"] == "runs":

                return len(today_runs)

        return 0

    @classmethod
    def is_complete(cls, mission_id, runs):

        for mission in cls.DEFINITIONS:

            if mission["id"] != mission_id:
                continue

            progress = cls.calculate_progress(
                mission_id,
                runs
            )

            return progress >= mission["target"]

        return False
