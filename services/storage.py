import json
import os
from datetime import datetime


SAVE_FILE = "player_data.json"
RUNS_FILE = "runs.json"


def save_player(player):

    data = {
        "name": player.name,
        "level": player.level,
        "xp": player.xp,
        "total_distance": player.total_distance,
        "total_runs": player.total_runs
    }

    with open(SAVE_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_player():

    if not os.path.exists(SAVE_FILE):
        return None

    with open(SAVE_FILE, "r") as file:
        return json.load(file)


def save_run(duration_seconds, distance_km, pace_seconds_per_km, xp):

    runs = load_runs()

    run = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration_seconds": duration_seconds,
        "distance_km": round(distance_km, 4),
        "pace_seconds_per_km": round(pace_seconds_per_km, 2)
        if pace_seconds_per_km is not None
        else None,
        "xp": xp
    }

    runs.append(run)

    with open(RUNS_FILE, "w") as file:
        json.dump(runs, file, indent=4)


def load_runs():

    if not os.path.exists(RUNS_FILE):
        return []

    try:

        with open(RUNS_FILE, "r") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

    except (json.JSONDecodeError, OSError):

        pass

    return []
