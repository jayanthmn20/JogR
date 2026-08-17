import json
import os
import shutil
from datetime import datetime

from jnius import autoclass


def _get_app_data_dir():

    try:

        PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
        )

        activity = PythonActivity.mActivity

        files_dir = (
            activity
            .getFilesDir()
            .getAbsolutePath()
        )

        data_dir = os.path.join(
            files_dir,
            "jogr_data"
        )

    except Exception:

        data_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

    os.makedirs(
        data_dir,
        exist_ok=True
    )

    return data_dir


APP_DATA_DIR = _get_app_data_dir()

SAVE_FILE = os.path.join(
    APP_DATA_DIR,
    "player_data.json"
)

RUNS_FILE = os.path.join(
    APP_DATA_DIR,
    "runs.json"
)


def _migrate_old_data():

    old_dir = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    old_player_file = os.path.join(
        old_dir,
        "player_data.json"
    )

    old_runs_file = os.path.join(
        old_dir,
        "runs.json"
    )

    if (
        not os.path.exists(SAVE_FILE)
        and os.path.exists(old_player_file)
    ):

        try:

            shutil.copy2(
                old_player_file,
                SAVE_FILE
            )

            print(
                "JogR STORAGE: migrated player_data.json"
            )

        except OSError as e:

            print(
                "JogR STORAGE PLAYER MIGRATION ERROR:",
                repr(e)
            )

    if (
        not os.path.exists(RUNS_FILE)
        and os.path.exists(old_runs_file)
    ):

        try:

            shutil.copy2(
                old_runs_file,
                RUNS_FILE
            )

            print(
                "JogR STORAGE: migrated runs.json"
            )

        except OSError as e:

            print(
                "JogR STORAGE RUN MIGRATION ERROR:",
                repr(e)
            )


_migrate_old_data()


def save_player(player):

    data = {
        "name": player.name,
        "level": player.level,
        "xp": player.xp,
        "total_distance": player.total_distance,
        "total_runs": player.total_runs
    }

    with open(
        SAVE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


def load_player():

    if not os.path.exists(SAVE_FILE):
        return None

    try:

        with open(
            SAVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return None


def save_run(
    duration_seconds,
    distance_km,
    pace_seconds_per_km,
    xp
):

    runs = load_runs()

    run = {
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "duration_seconds": duration_seconds,
        "distance_km": round(
            distance_km,
            4
        ),
        "pace_seconds_per_km": (
            round(
                pace_seconds_per_km,
                2
            )
            if pace_seconds_per_km is not None
            else None
        ),
        "xp": xp
    }

    runs.append(run)

    with open(
        RUNS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            runs,
            file,
            indent=4
        )


def load_runs():

    if not os.path.exists(RUNS_FILE):
        return []

    try:

        with open(
            RUNS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

    except (
        json.JSONDecodeError,
        OSError
    ):

        pass

    return []