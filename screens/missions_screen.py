from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar

from models.missions import Mission
from services.storage import load_runs


class MissionsScreen(BoxLayout):

    def __init__(
        self,
        player,
        claim_mission,
        go_to_home_screen,
        **kwargs
    ):
        super().__init__(
            orientation="vertical",
            padding=20,
            spacing=15,
            **kwargs
        )

        self.player = player
        self.claim_mission = claim_mission

        title = Label(
            text="DAILY MISSIONS",
            font_size=38,
            size_hint_y=None,
            height=60
        )

        self.mission_layout = BoxLayout(
            orientation="vertical",
            spacing=15,
            size_hint_y=None
        )

        self.mission_layout.bind(
            minimum_height=self.mission_layout.setter(
                "height"
            )
        )

        scroll = ScrollView()

        scroll.add_widget(
            self.mission_layout
        )

        home_button = Button(
            text="BACK TO HOME",
            font_size=22,
            size_hint_y=None,
            height=60
        )

        home_button.bind(
            on_press=go_to_home_screen
        )

        self.add_widget(title)
        self.add_widget(scroll)
        self.add_widget(home_button)

        self.refresh()

    def refresh(self):

        self.mission_layout.clear_widgets()

        runs = load_runs()
        today = Mission.today()

        for mission in Mission.DEFINITIONS:

            progress = Mission.calculate_progress(
                mission["id"],
                runs
            )

            target = mission["target"]

            if mission["type"] == "distance":

                display_progress = min(
                    progress,
                    target
                )

                progress_text = (
                    f"{display_progress:.2f}"
                    f" / {target:.2f} km"
                )

            elif mission["type"] == "duration":

                progress_minutes = int(
                    progress // 60
                )

                target_minutes = int(
                    target // 60
                )

                display_progress = min(
                    progress_minutes,
                    target_minutes
                )

                progress_text = (
                    f"{display_progress}"
                    f" / {target_minutes} minutes"
                )

            else:

                display_progress = min(
                    progress,
                    target
                )

                progress_text = (
                    f"{display_progress:.0f}"
                    f" / {target:.0f} runs"
                )

            completed = (
                progress >= target
            )

            claimed = self.player.is_mission_claimed(
                today,
                mission["id"]
            )

            card = BoxLayout(
                orientation="vertical",
                spacing=5,
                padding=10,
                size_hint_y=None,
                height=250
            )

            if claimed:

                status = "REWARD CLAIMED"

            elif completed:

                status = "REWARD AVAILABLE"

            else:

                status = "IN PROGRESS"

            status_label = Label(
                text=status,
                font_size=16,
                size_hint_y=None,
                height=25
            )

            title_label = Label(
                text=mission["title"],
                font_size=24,
                size_hint_y=None,
                height=32
            )

            description_label = Label(
                text=mission["description"],
                font_size=17,
                size_hint_y=None,
                height=28
            )

            progress_label = Label(
                text=progress_text,
                font_size=18,
                size_hint_y=None,
                height=28
            )

            progress_bar = ProgressBar(
                max=target,
                value=min(progress, target),
                size_hint_y=None,
                height=12
            )

            reward_text = (
                f"REWARD: +{mission['reward']} XP"
            )

            reward_label = Label(
                text=reward_text,
                font_size=16,
                size_hint_y=None,
                height=25
            )

            claim_button = Button(
                font_size=17,
                size_hint_y=None,
                height=40
            )

            if claimed:

                claim_button.text = "CLAIMED"
                claim_button.disabled = True

            elif completed:

                claim_button.text = (
                    f"CLAIM +{mission['reward']} XP"
                )

                claim_button.bind(
                    on_press=lambda instance,
                    mission_id=mission["id"]:
                    self._claim(mission_id)
                )

            else:

                claim_button.text = "NOT COMPLETED"
                claim_button.disabled = True

            card.add_widget(status_label)
            card.add_widget(title_label)
            card.add_widget(description_label)
            card.add_widget(progress_label)
            card.add_widget(progress_bar)
            card.add_widget(reward_label)
            card.add_widget(claim_button)

            self.mission_layout.add_widget(
                card
            )

    def _claim(self, mission_id):

        success = self.claim_mission(
            mission_id
        )

        if success:
            self.refresh()
