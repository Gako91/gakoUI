"""Demo: USlider — value slider + range slider helper.

Run: uv run python demos/demo_slider.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import create_range_slider, create_slider_with_label

Window.size = (560, 420)


class SliderDemoApp(App):
    title = "GakoUI · USlider"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=18)

        volume_container, self.volume = create_slider_with_label(
            text="Volume", color="blue", min_value=0, max_value=100, value=42,
        )
        self.volume.bind(value=lambda i, v: self._echo("Volume", v))
        root.add_widget(volume_container)

        price_container, (self.price_low, self.price_high) = create_range_slider(
            color="emerald",
            min_val=0, max_val=1000,
            low_value=200, high_value=750,
        )
        root.add_widget(price_container)

        self.status = Label(text="Move a slider…", color=(0.85, 0.85, 0.85, 1))
        root.add_widget(self.status)
        return root

    def _echo(self, name, value):
        self.status.text = f"{name} = {value:.1f}"


if __name__ == "__main__":
    SliderDemoApp().run()
