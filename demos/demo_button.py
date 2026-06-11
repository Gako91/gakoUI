"""Demo: UButton — variants, colors, icons, rounded.

Run: uv run python demos/demo_button.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import UButton

Window.size = (700, 520)


def section(title):
    lbl = Label(
        text=title, size_hint_y=None, height=28, color=(1, 1, 1, 1),
        font_size="16sp", bold=True, halign="left", valign="middle",
    )
    lbl.bind(size=lambda *_: setattr(lbl, "text_size", lbl.size))
    return lbl


class ButtonDemoApp(App):
    title = "GakoUI · UButton"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=12)

        root.add_widget(section("Solid"))
        row1 = BoxLayout(size_hint_y=None, height=44, spacing=10)
        for color in ("green", "blue", "red", "orange", "purple"):
            row1.add_widget(UButton(text=color.capitalize(), color=color))
        root.add_widget(row1)

        root.add_widget(section("Outline"))
        row2 = BoxLayout(size_hint_y=None, height=44, spacing=10)
        for color in ("green", "blue", "red", "orange", "purple"):
            row2.add_widget(UButton(text=color.capitalize(), color=color, variant="outline"))
        root.add_widget(row2)

        root.add_widget(section("Ghost"))
        row3 = BoxLayout(size_hint_y=None, height=44, spacing=10)
        for color in ("green", "blue", "red", "orange", "purple"):
            row3.add_widget(UButton(text=color.capitalize(), color=color, variant="ghost"))
        root.add_widget(row3)

        root.add_widget(section("With icons / rounded"))
        row4 = BoxLayout(size_hint_y=None, height=48, spacing=10)
        row4.add_widget(UButton(
            text="Search", color="sky",
            left_icon="material-symbols--search-rounded.png",
        ))
        row4.add_widget(UButton(
            text="Save", color="emerald",
            right_icon="material-symbols--save-as-outline-rounded.png",
        ))
        row4.add_widget(UButton(text="Pill", color="amber", rounded=True))
        root.add_widget(row4)

        return root


if __name__ == "__main__":
    ButtonDemoApp().run()
