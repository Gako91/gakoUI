"""Demo: UTabs — three tabs built with create_simple_tabs.

Run: uv run python demos/demo_tabs.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import UButton, create_simple_tabs

Window.size = (640, 420)


def _label(text):
    lbl = Label(text=text, color=(1, 1, 1, 1))
    lbl.bind(size=lambda *_: setattr(lbl, "text_size", lbl.size))
    return lbl


class TabsDemoApp(App):
    title = "GakoUI · UTabs"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=10)

        actions = BoxLayout(orientation="vertical", spacing=10, padding=10)
        actions.add_widget(_label("Pick a button:"))
        row = BoxLayout(size_hint_y=None, height=44, spacing=10)
        row.add_widget(UButton(text="Save", color="emerald"))
        row.add_widget(UButton(text="Delete", color="red", variant="outline"))
        actions.add_widget(row)

        tabs = create_simple_tabs([
            {"id": "overview", "text": "Overview",
             "content": _label("Welcome to the GakoUI tabs demo!")},
            {"id": "actions", "text": "Actions",
             "content": actions, "badge": "2"},
            {"id": "settings", "text": "Settings",
             "content": _label("Nothing to configure yet."),
             "icon": "material-symbols--person-edit-outline.png"},
        ])
        root.add_widget(tabs)
        return root


if __name__ == "__main__":
    TabsDemoApp().run()
