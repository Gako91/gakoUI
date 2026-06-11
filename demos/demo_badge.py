"""Demo: UBadge / UBadgeDot / UBadgeNumber.

Run: uv run python demos/demo_badge.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import (
    UBadge,
    UBadgeDot,
    UBadgeNumber,
    create_notification_badge,
    create_status_badge,
)

Window.size = (640, 420)


def section(title):
    lbl = Label(
        text=title, size_hint_y=None, height=26, color=(1, 1, 1, 1),
        font_size="15sp", bold=True, halign="left", valign="middle",
    )
    lbl.bind(size=lambda *_: setattr(lbl, "text_size", lbl.size))
    return lbl


class BadgeDemoApp(App):
    title = "GakoUI · UBadge"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=12)

        root.add_widget(section("Variants"))
        row = BoxLayout(size_hint_y=None, height=36, spacing=10)
        row.add_widget(UBadge(text="solid", color_theme="blue"))
        row.add_widget(UBadge(text="outline", color_theme="green", variant="outline"))
        row.add_widget(UBadge(text="soft", color_theme="red", variant="soft"))
        row.add_widget(UBadge(text="rounded", color_theme="purple", rounded=True))
        root.add_widget(row)

        root.add_widget(section("Sizes"))
        row2 = BoxLayout(size_hint_y=None, height=40, spacing=10)
        for size_variant in ("small", "medium", "large"):
            row2.add_widget(UBadge(text=size_variant, color_theme="amber",
                                   size_variant=size_variant))
        root.add_widget(row2)

        root.add_widget(section("Status helpers"))
        row3 = BoxLayout(size_hint_y=None, height=36, spacing=10)
        for status in ("success", "warning", "error", "info"):
            row3.add_widget(create_status_badge(status))
        root.add_widget(row3)

        root.add_widget(section("Dots & numbers"))
        row4 = BoxLayout(size_hint_y=None, height=40, spacing=18)
        row4.add_widget(UBadgeDot(color_theme="red"))
        row4.add_widget(UBadgeDot(color_theme="green"))
        row4.add_widget(UBadgeNumber(count=3, color_theme="blue"))
        row4.add_widget(UBadgeNumber(count=42, color_theme="red"))
        row4.add_widget(create_notification_badge(count=128))
        root.add_widget(row4)

        return root


if __name__ == "__main__":
    BadgeDemoApp().run()
