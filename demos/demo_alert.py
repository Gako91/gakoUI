"""Demo: UAlert — success / error / warning / info.

Run: uv run python demos/demo_alert.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from gakoui.widgets import (
    create_error_alert,
    create_info_alert,
    create_success_alert,
    create_warning_alert,
)

Window.size = (640, 420)


class AlertDemoApp(App):
    title = "GakoUI · UAlert"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=12)
        root.add_widget(create_success_alert(
            title="Saved", description="Your changes were saved successfully."))
        root.add_widget(create_error_alert(
            title="Error", description="Something went wrong, please retry."))
        root.add_widget(create_warning_alert(
            title="Warning", description="This action cannot be undone."))
        root.add_widget(create_info_alert(
            title="Heads up", description="A new version of GakoUI is available."))
        return root


if __name__ == "__main__":
    AlertDemoApp().run()
