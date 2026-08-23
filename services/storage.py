import json
import os
import shutil
from datetime import datetime, timedelta

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


def _atomic_write_json(
    file_path,
    data
):

    temp_file = (
        file_path
        + ".tmp"
    )

    try:

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

            file.flush()

            os.fsync(
                file.fileno()
            )

        os.replace(
            temp_file,
            file_path
        )

    except Exception:

        if os.path.exists(
            temp_file
        ):

            try:

                os.remove(
                    temp_file
                )

            except OSError:

                pass

        raise


def _load_json(
    file_path,
    default=None
):

    if not os.path.exists(
        file_path
    ):

        return default

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return default


def save_player(player):

    data = {
        "name": player.name,
        "level": player.level,
        "xp": player.xp,
        "total_xp": player.total_xp,
        "total_distance": player.total_distance,
        "total_runs": player.total_runs,
        "achievements": player.achievements
    }

    _atomic_write_json(
        SAVE_FILE,
        data
    )


def load_player():

    return _load_json(
        SAVE_FILE,
        None
    )


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

    runs.append(
        run
    )

    _atomic_write_json(
        RUNS_FILE,
        runs
    )


def load_runs():

    data = _load_json(
        RUNS_FILE,
        []
    )

    if isinstance(
        data,
        list
    ):

        return data

    return []


def get_streaks():

    runs = load_runs()

    if not runs:
        return 0, 0

    dates = set()

    for run in runs:

        date_text = run.get("date")

        if not date_text:
            continue

        try:

            run_date = datetime.strptime(
                date_text,
                "%Y-%m-%d %H:%M:%S"
            ).date()

            dates.add(run_date)

        except ValueError:

            continue

    if not dates:
        return 0, 0


    today = datetime.now().date()

    current_streak = 0
    check_date = today
    while check_date in dates:

        current_streak += 1


        check_date -= timedelta(days=1)

    best_streak = 1
    streak = 1

    ascending_dates = sorted(dates)

    for index in range(
        1,
        len(ascending_dates)
    ):

        difference = (
            ascending_dates[index]
            - ascending_dates[index - 1]
        ).days

        if difference == 1:

            streak += 1

        else:

            streak = 1

        if streak > best_streak:
            best_streak = streak

    return current_streak, best_streak
