"""Demo: UToggle — three sizes, three colors, with label helper.

Run: uv run python demos/demo_toggle.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import UToggle, create_toggle_with_label

Window.size = (520, 420)


class ToggleDemoApp(App):
    title = "GakoUI · UToggle"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=14)

        self.status = Label(text="Toggle a switch…", color=(0.85, 0.85, 0.85, 1),
                            size_hint_y=None, height=24)
        root.add_widget(self.status)

        for size_variant, color in (
            ("small", "blue"),
            ("medium", "green"),
            ("large", "purple"),
        ):
            container, toggle = create_toggle_with_label(
                text=f"{size_variant.capitalize()} · {color}",
                size_variant=size_variant,
                color=color,
                active=size_variant == "medium",
            )
            toggle.bind(active=lambda inst, val, name=size_variant: self._on(name, val))
            root.add_widget(container)

        root.add_widget(Label())  # spacer
        return root

    def _on(self, name, value):
        self.status.text = f"{name} → {value}"


if __name__ == "__main__":
    ToggleDemoApp().run()
