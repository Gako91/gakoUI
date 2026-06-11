"""Demo: USelect — single-value select with options + country helper.

Run: uv run python demos/demo_select.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import create_country_select, create_select_with_label

Window.size = (520, 420)


class SelectDemoApp(App):
    title = "GakoUI · USelect"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=14)

        languages = [
            {"text": "Python", "value": "py"},
            {"text": "JavaScript", "value": "js"},
            {"text": "Rust", "value": "rs"},
            {"text": "Go", "value": "go"},
        ]
        lang_container, self.lang_select = create_select_with_label(
            text="Favourite language", options=languages, placeholder="Pick one…"
        )
        self.lang_select.bind(selected_value=lambda i, v: self._on_pick("lang", v))
        root.add_widget(lang_container)

        self.country_select = create_country_select()
        self.country_select.bind(selected_value=lambda i, v: self._on_pick("country", v))
        root.add_widget(self.country_select)

        self.status = Label(text="", color=(0.85, 0.85, 0.85, 1))
        root.add_widget(self.status)
        return root

    def _on_pick(self, name, value):
        self.status.text = f"{name} = {value}"


if __name__ == "__main__":
    SelectDemoApp().run()
