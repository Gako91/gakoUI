"""Demo: UCheckbox — standalone, with label, and a group.

Run: uv run python demos/demo_checkbox.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import (
    UCheckbox,
    create_checkbox_group,
    create_checkbox_with_label,
)

Window.size = (520, 480)


class CheckboxDemoApp(App):
    title = "GakoUI · UCheckbox"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=14)

        sizes = BoxLayout(size_hint_y=None, height=40, spacing=20)
        for variant, color in (("small", "blue"), ("medium", "green"), ("large", "purple")):
            cb = UCheckbox(size_variant=variant, color=color, checked=variant == "medium")
            sizes.add_widget(cb)
        root.add_widget(sizes)

        labelled, _ = create_checkbox_with_label(text="I accept the terms", color="emerald")
        root.add_widget(labelled)

        group, _ = self._build_group()
        root.add_widget(group)
        return root

    def _build_group(self):
        items = ["Python", "TypeScript", "Rust", "Go"]
        group, checkboxes = create_checkbox_group(items, color="sky")

        self.status = Label(text="Pick languages…", color=(0.85, 0.85, 0.85, 1))
        for cb in checkboxes:
            cb.bind(checked=lambda *_: self._refresh())
        self._group = group
        self._checkboxes = checkboxes

        wrapper = BoxLayout(orientation="vertical", spacing=8)
        wrapper.add_widget(group)
        wrapper.add_widget(self.status)
        return wrapper, checkboxes

    def _refresh(self):
        picked = [cb.value for cb in self._checkboxes if cb.checked]
        self.status.text = "Selected: " + (", ".join(picked) if picked else "—")


if __name__ == "__main__":
    CheckboxDemoApp().run()
