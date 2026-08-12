from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class ResultScreen(BoxLayout):

    def __init__(self, go_to_home_screen, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=50,
            spacing=30,
            **kwargs
        )

        title = Label(
            text="RUN COMPLETE!",
            font_size=40
        )

        result = Label(
            text="Great job!",
            font_size=25
        )

        home_button = Button(
            text="BACK TO HOME",
            font_size=25
        )

        home_button.bind(
            on_press=go_to_home_screen
        )

        self.add_widget(title)
        self.add_widget(result)
        self.add_widget(home_button)