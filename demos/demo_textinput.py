"""Demo: UTextInput — search-style input with leading icon.

Run: uv run python demos/demo_textinput.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import UTextInput

Window.size = (520, 420)


class TextInputDemoApp(App):
    title = "GakoUI · UTextInput"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=14)

        for color, hint in (
            ("green", "Search products..."),
            ("blue", "Search users..."),
            ("orange", "Filter tags..."),
            ("red", "Error-style input"),
        ):
            ti = UTextInput(color=color, hint_text=hint, size_hint_y=None, height=64)
            ti.bind(text=self._on_text)
            root.add_widget(ti)

        self.echo = Label(
            text="", size_hint_y=None, height=24,
            color=(0.8, 0.8, 0.8, 1), halign="left", valign="middle",
        )
        self.echo.bind(size=lambda *_: setattr(self.echo, "text_size", self.echo.size))
        root.add_widget(self.echo)
        return root

    def _on_text(self, instance, value):
        self.echo.text = f"Last text: {value!r}"


if __name__ == "__main__":
    TextInputDemoApp().run()
