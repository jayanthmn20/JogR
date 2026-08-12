from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class HomeScreen(BoxLayout):

    def __init__(self, go_to_run_screen, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=50,
            spacing=30,
            **kwargs
        )

        title = Label(
            text="JogR",
            font_size=50
        )

        tagline = Label(
            text="Run. Level Up. Become Better.",
            font_size=20
        )

        start_button = Button(
            text="START RUN",
            font_size=25
        )

        start_button.bind(
            on_press=go_to_run_screen
        )

        self.add_widget(title)
        self.add_widget(tagline)
        self.add_widget(start_button)