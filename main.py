from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class JogRApp(App):

    def build(self):

        layout = BoxLayout(
            orientation="vertical",
            padding=50,
            spacing=30
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

        layout.add_widget(title)
        layout.add_widget(tagline)
        layout.add_widget(start_button)

        return layout


if __name__ == "__main__":
    JogRApp().run()