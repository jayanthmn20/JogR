import json
import os


SAVE_FILE = "player_data.json"


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