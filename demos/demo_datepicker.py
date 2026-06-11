"""Demo: DatePicker — calendar dropdown.

Run: uv run python demos/demo_datepicker.py
"""
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import DatePicker

Window.size = (520, 420)


class DatePickerDemoApp(App):
    title = "GakoUI · DatePicker"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=14)

        self.status = Label(
            text="Pick a date in the calendar.",
            color=(0.85, 0.85, 0.85, 1),
            size_hint_y=None, height=30,
        )
        root.add_widget(self.status)

        picker = DatePicker(size_hint=(None, None), size=(220, 44))
        picker.bind(selected_date=self._on_date)
        wrap = BoxLayout(size_hint_y=None, height=60)
        wrap.add_widget(picker)
        root.add_widget(wrap)

        root.add_widget(Label())  # spacer
        return root

    def _on_date(self, instance, value):
        if isinstance(value, datetime):
            self.status.text = f"Selected: {value.strftime('%Y-%m-%d')}"
        else:
            self.status.text = f"Selected: {value}"


if __name__ == "__main__":
    DatePickerDemoApp().run()
