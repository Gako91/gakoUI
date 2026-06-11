"""Demo: UCard — three variants side by side.

Run: uv run python demos/demo_card.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import (
    UButton,
    UCard,
    UCardContent,
    UCardDescription,
    UCardFooter,
    UCardHeader,
    UCardTitle,
)

Window.size = (820, 360)


def _build_card(variant, color):
    card = UCard(variant=variant, color=color)
    header = UCardHeader()
    header.add_widget(UCardTitle(text=f"{variant.capitalize()} card"))
    header.add_widget(UCardDescription(text=f"A `{variant}` card themed `{color}`."))
    card.add_widget(header)

    content = UCardContent()
    content.add_widget(Label(text="Some content here.", color=(1, 1, 1, 1)))
    card.add_widget(content)

    footer = UCardFooter()
    footer.add_widget(UButton(text="Action", color=color, size_hint_x=None, width=120))
    card.add_widget(footer)
    return card


class CardDemoApp(App):
    title = "GakoUI · UCard"

    def build(self):
        root = BoxLayout(orientation="horizontal", padding=20, spacing=16)
        root.add_widget(_build_card("elevated", "blue"))
        root.add_widget(_build_card("outlined", "green"))
        root.add_widget(_build_card("filled", "purple"))
        return root


if __name__ == "__main__":
    CardDemoApp().run()
