"""Demo: DatePicker / UCalendar / DateRangePicker / MultiDatePicker.

Run: uv run python demos/demo_datepicker.py
"""
from datetime import date, datetime, timedelta

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import (
    DatePicker,
    DateRangePicker,
    MultiDatePicker,
    UCalendar,
)

Window.size = (860, 560)


def _section_label(text):
    lbl = Label(
        text=text, size_hint_y=None, height=26,
        color=(1, 1, 1, 1), bold=True, font_size='14sp',
        halign='left', valign='middle',
    )
    lbl.bind(size=lambda *_: setattr(lbl, 'text_size', lbl.size))
    return lbl


class DatePickerDemoApp(App):
    title = "GakoUI \u00b7 DatePicker / UCalendar"

    def build(self):
        root = BoxLayout(orientation='horizontal', padding=16, spacing=16)

        # -- Left column: pickers --------------------------------------
        left = BoxLayout(orientation='vertical', spacing=10)

        left.add_widget(_section_label("DatePicker (single)"))
        self.picker = DatePicker(color='sky')
        self.picker.bind(selected_date=self._on_single)
        left.add_widget(self.picker)

        left.add_widget(_section_label("DateRangePicker"))
        self.range_picker = DateRangePicker(color='emerald')
        self.range_picker.bind(selected_range=self._on_range)
        left.add_widget(self.range_picker)

        left.add_widget(_section_label("MultiDatePicker"))
        self.multi_picker = MultiDatePicker(color='purple')
        self.multi_picker.bind(selected_dates=self._on_multi)
        left.add_widget(self.multi_picker)

        self.status = Label(
            text="Pick dates to see callbacks here.",
            color=(0.8, 0.8, 0.85, 1), halign='left', valign='top',
        )
        self.status.bind(
            size=lambda *_: setattr(self.status, 'text_size', self.status.size)
        )
        left.add_widget(self.status)

        # -- Right column: a standalone UCalendar ----------------------
        right = BoxLayout(orientation='vertical', spacing=10,
                          size_hint_x=None, width=320)
        right.add_widget(_section_label(
            "Standalone UCalendar  (range, \u00b145 days, weekends disabled)"
        ))

        today = date.today()
        right.add_widget(UCalendar(
            mode='range',
            color='amber',
            min_value=today - timedelta(days=45),
            max_value=today + timedelta(days=45),
            is_date_disabled=lambda d: d.weekday() >= 5,  # disable Sat/Sun
        ))

        root.add_widget(left)
        root.add_widget(right)
        return root

    def _on_single(self, _picker, value):
        self.status.text = f"DatePicker \u2192 {value}"

    def _on_range(self, _picker, value):
        if value:
            s, e = value
            self.status.text = (
                f"DateRangePicker \u2192 {s:%Y-%m-%d} to {e:%Y-%m-%d}"
            )
        else:
            self.status.text = "DateRangePicker \u2192 (cleared)"

    def _on_multi(self, _picker, value):
        nice = [d.strftime('%Y-%m-%d') if isinstance(d, datetime) else str(d)
                for d in value]
        self.status.text = f"MultiDatePicker \u2192 {nice}"


if __name__ == "__main__":
    DatePickerDemoApp().run()
