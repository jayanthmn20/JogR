__version__ = "0.1.0"

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from screens.home_screen import HomeScreen
from screens.run_screen import RunScreen
from screens.result_screen import ResultScreen
from screens.history_screen import HistoryScreen
from screens.stats_screen import StatsScreen
from screens.achievements_screen import AchievementsScreen
from screens.missions_screen import MissionsScreen

from models.player import Player
from models.achievements import Achievement
from models.missions import Mission
from services.storage import save_player, load_player, save_run, load_runs, get_streaks


class JogRApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        saved_data = load_player()

        if saved_data:
            self.player = Player(
                name=saved_data["name"]
            )

            self.player.level = saved_data["level"]
            self.player.xp = saved_data["xp"]
            self.player.total_xp = saved_data.get(
                "total_xp",
                saved_data["xp"]
            )
            self.player.total_distance = saved_data["total_distance"]
            self.player.total_runs = saved_data["total_runs"]
            self.player.achievements = saved_data.get(
                "achievements",
                []
            )
            self.player.mission_claims = saved_data.get(
                "mission_claims",
                {}
            )

            self.player.streak_rewards = saved_data.get(
                "streak_rewards",
                []
            )

        else:
            self.player = Player()

        self.home_widget = None
        self.run_widget = None
        self.result_widget = None
        self.history_widget = None
        self.stats_widget = None
        self.achievements_widget = None
        self.missions_widget = None


    def build(self):

        manager = ScreenManager()

        home_screen = Screen(name="home")
        run_screen = Screen(name="run")
        result_screen = Screen(name="result")
        history_screen = Screen(name="history")
        stats_screen = Screen(name="stats")
        achievements_screen = Screen(name="achievements")
        missions_screen = Screen(name="missions")

        self.home_widget = HomeScreen(
            player=self.player,
            go_to_run_screen=lambda instance: self.go_to_run(manager),
            go_to_history_screen=lambda instance: self.go_to_history(manager),
            go_to_stats_screen=lambda instance: self.go_to_stats(manager),
            go_to_achievements_screen=lambda instance: self.go_to_achievements(manager),
            go_to_missions_screen=lambda instance: self.go_to_missions(manager)
        )

        self.run_widget = RunScreen(
            go_to_result_screen=lambda instance: self.go_to_result(manager)
        )

        self.result_widget = ResultScreen(
            go_to_home_screen=lambda instance: self.go_to_home(manager)
        )

        self.history_widget = HistoryScreen(
            go_to_home_screen=lambda instance: self.go_to_home(manager)
        )

        self.stats_widget = StatsScreen(
            go_to_home_screen=lambda instance: self.go_to_home(manager)
        )

        self.achievements_widget = AchievementsScreen(
            player=self.player,
            go_to_home_screen=lambda instance: self.go_to_home(manager)
        )

        self.missions_widget = MissionsScreen(
            player=self.player,
            claim_mission=self.claim_mission,
            go_to_home_screen=lambda instance: self.go_to_home(manager)
        )

        home_screen.add_widget(self.home_widget)
        run_screen.add_widget(self.run_widget)
        result_screen.add_widget(self.result_widget)
        history_screen.add_widget(self.history_widget)
        stats_screen.add_widget(self.stats_widget)
        achievements_screen.add_widget(self.achievements_widget)
        missions_screen.add_widget(self.missions_widget)

        manager.add_widget(home_screen)
        manager.add_widget(run_screen)
        manager.add_widget(result_screen)
        manager.add_widget(history_screen)
        manager.add_widget(stats_screen)
        manager.add_widget(achievements_screen)
        manager.add_widget(missions_screen)

        return manager

    def go_to_run(self, manager):

        manager.current = "run"

        self.run_widget.start_timer()

    def go_to_result(self, manager):

        self.run_widget.stop_timer()

        (
            time,
            duration_seconds,
            distance,
            pace,
            pace_seconds_per_km,
            xp
        ) = self.run_widget.get_results()

        save_run(
            duration_seconds,
            distance,
            pace_seconds_per_km,
            xp
        )

        current_streak, _ = get_streaks()

        streak_reward = self.check_streak_reward(
            current_streak
        )

        total_xp = xp

        if streak_reward is not None:
            total_xp += streak_reward["reward"]

        level_result = self.player.add_run(
            distance,
            total_xp
        )

        if streak_reward is not None:
            self.player.claim_streak_reward(
                streak_reward["milestone"]
            )

        unlocked_achievements = (
            Achievement.check_unlocked(
                self.player,
                current_streak
            )
        )

        new_achievements = []

        for achievement in unlocked_achievements:

            if achievement["id"] not in self.player.achievements:

                self.player.achievements.append(
                    achievement["id"]
                )

                new_achievements.append(
                    achievement
                )

        save_player(
            self.player
        )

        self.result_widget.show_results(
            time,
            distance,
            pace,
            xp,
            level_result,
            self.player.level,
            self.player.xp,
            self.player.xp_required(),
            new_achievements,
            streak_reward
        )

        manager.current = "result"

    STREAK_REWARDS = {
        3: 50,
        7: 150,
        14: 300,
        30: 750
    }

    def check_streak_reward(
            self,
            current_streak
    ):
        reward = self.STREAK_REWARDS.get(
            current_streak
        )

        if reward is None:
            return None

        if self.player.is_streak_reward_claimed(
            current_streak
        ):
            return None

        return {
            "milestone": current_streak,
            "reward": reward
        }

    def go_to_home(self, manager):

        self.home_widget.update_stats()

        manager.current = "home"



    def claim_mission(self, mission_id):

        runs = load_runs()

        if not Mission.is_complete(
            mission_id,
            runs
        ):
            return False

        today = Mission.today()

        if self.player.is_mission_claimed(
            today,
            mission_id
        ):
            return False

        reward = 0

        for mission in Mission.DEFINITIONS:

            if mission["id"] == mission_id:
                reward = mission["reward"]
                break

        if reward <= 0:
            return False

        if not self.player.claim_mission(
            today,
            mission_id
        ):
            return False

        self.player.add_xp(
            reward
        )

        save_player(
            self.player
        )

        return True

    def go_to_history(self, manager):

        self.history_widget.refresh()

        manager.current = "history"

    def go_to_achievements(self, manager):

        self.achievements_widget.refresh()

        manager.current = "achievements"

    def go_to_stats(self, manager):

        self.stats_widget.refresh()

        manager.current = "stats"

    def go_to_missions(self, manager):
        self.missions_widget.refresh()

        manager.current = "missions"

if __name__ == "__main__":
    JogRApp().run()
