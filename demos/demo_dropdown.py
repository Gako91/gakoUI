"""Demo: UDropDown — button-styled dropdown with sectioned items.

Run: uv run python demos/demo_dropdown.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import UDropDown

Window.size = (480, 360)


class DropDownDemoApp(App):
    title = "GakoUI · UDropDown"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=14)

        self.status = Label(
            text="Pick an action…",
            size_hint_y=None, height=30,
            color=(0.85, 0.85, 0.85, 1),
        )
        root.add_widget(self.status)

        dd = UDropDown(text="Actions", size_hint=(None, None), size=(180, 44))
        dd.items = [
            [
                {"label": "Profile", "on_release": lambda *_: self._set("Profile")},
                {"label": "Settings", "on_release": lambda *_: self._set("Settings")},
            ],
            [
                {"label": "Logout", "on_release": lambda *_: self._set("Logout")},
            ],
        ]
        anchor = BoxLayout(size_hint_y=None, height=60)
        anchor.add_widget(dd)
        root.add_widget(anchor)

        root.add_widget(Label())  # spacer
        return root

    def _set(self, name):
        self.status.text = f"Selected: {name}"


if __name__ == "__main__":
    DropDownDemoApp().run()
