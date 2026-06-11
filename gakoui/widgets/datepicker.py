"""DatePicker / UCalendar widgets for GakoUI.

Inspired by the Nuxt UI Calendar component
(https://ui.nuxt.com/components/calendar). Provides:

- ``UCalendar``        — standalone calendar (single / range / multiple)
- ``DatePicker``       — button + popover wrapping a UCalendar (single)
- ``DateRangePicker``  — button + popover wrapping a UCalendar (range)
- ``MultiDatePicker``  — button + popover wrapping a UCalendar (multiple)
"""
from calendar import Calendar as _PyCalendar
from datetime import date as _date, datetime, timedelta
from functools import partial

from dateutil.relativedelta import relativedelta

from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import (
    AliasProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    OptionProperty,
    StringProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from gakoui.data.colors import colors


KV = """
#:import rgba kivy.utils.rgba


<_WeekDayNames>:
    padding: [6, 0, 6, 0]
    size_hint_y: None
    height: 28

<_DayCell>:
    size_hint_y: None
    height: 36
    padding: [2, 2, 2, 2]

<UCalendar>:
    orientation: 'vertical'
    size_hint_y: None
    height: self.minimum_height
    padding: [4, 4, 4, 4]
    spacing: 4

<DatePickerDropDown>:
    canvas.before:
        Color:
            rgba: rgba('#0f172a')
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [10]
        Color:
            rgba: .5, .5, .5, 1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 10, 10, 10, 10, 100)
    size_hint_x: None
    width: 300
    auto_width: False
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _to_date(value):
    """Coerce ``datetime`` / ``date`` / ``None`` to a ``date`` (or ``None``)."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, _date):
        return value
    raise TypeError(f"Expected date/datetime, got {type(value).__name__}")


def _to_datetime(value):
    """Coerce ``date`` / ``datetime`` / ``None`` to a ``datetime`` (midnight)."""
    d = _to_date(value)
    if d is None:
        return None
    return datetime(d.year, d.month, d.day)


# ---------------------------------------------------------------------------
# Internal building blocks
# ---------------------------------------------------------------------------


class _WeekDayNames(BoxLayout):
    """Top row of the calendar grid showing weekday initials."""

    def __init__(self, names, **kwargs):
        super().__init__(**kwargs)
        for n in names:
            self.add_widget(Label(
                text=n,
                color=(0.65, 0.65, 0.7, 1),
                bold=True,
                font_size='12sp',
            ))


class _DayCell(BoxLayout):
    """One grid cell. Optionally draws a faint background for range
    highlight; embeds a single ``UButton`` for the day number."""

    in_range = BooleanProperty(False)
    color = StringProperty('sky')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self._range_color = Color(0, 0, 0, 0)
            self._range_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._sync_rect, pos=self._sync_rect,
                  in_range=self._sync_color, color=self._sync_color)
        self._sync_color()

    def _sync_rect(self, *_):
        self._range_rect.size = self.size
        self._range_rect.pos = self.pos

    def _sync_color(self, *_):
        if self.in_range:
            c = colors.get(self.color).get('fill')
            self._range_color.rgba = (c[0], c[1], c[2], 0.18)
        else:
            self._range_color.rgba = (0, 0, 0, 0)


class DatePickerDropDown(DropDown):
    """Popover container styled with a dark rounded background."""
    pass


# ---------------------------------------------------------------------------
# UCalendar — standalone calendar widget
# ---------------------------------------------------------------------------


class UCalendar(BoxLayout):
    """Standalone calendar inspired by Nuxt UI's ``UCalendar``.

    Supports three selection modes (``single`` / ``range`` / ``multiple``),
    date bounds (``min_value`` / ``max_value``), per-date filtering
    (``is_date_disabled``), and the usual visual flags (``disabled``,
    ``readonly``, ``fixed_weeks``, ``show_outside_days``, ``month_controls``,
    ``year_controls``).
    """

    mode = OptionProperty('single', options=['single', 'range', 'multiple'])

    # Selection state (the active one depends on ``mode``)
    selected_date = ObjectProperty(None, allownone=True)
    selected_range = ObjectProperty(None, allownone=True)
    selected_dates = ListProperty([])

    # Bounds & filter
    min_value = ObjectProperty(None, allownone=True)
    max_value = ObjectProperty(None, allownone=True)
    is_date_disabled = ObjectProperty(None, allownone=True)

    # Behaviour
    disabled = BooleanProperty(False)
    readonly = BooleanProperty(False)
    fixed_weeks = BooleanProperty(True)
    show_outside_days = BooleanProperty(True)
    month_controls = BooleanProperty(True)
    year_controls = BooleanProperty(True)

    # Theming
    color = StringProperty('sky')
    week_day_names = ListProperty(['M', 'T', 'W', 'T', 'F', 'S', 'S'])

    # View state
    _view_year = NumericProperty(datetime.now().year)
    _view_month = NumericProperty(datetime.now().month)
    _pending_range_start = ObjectProperty(None, allownone=True)

    __events__ = ('on_date_select', 'on_range_select', 'on_dates_change')

    # -- Lifecycle ------------------------------------------------------

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        initial = self._initial_view_date()
        if initial is not None:
            self._view_year = initial.year
            self._view_month = initial.month

        self._navbar = self._build_navbar()
        self.add_widget(self._navbar)

        self._weekday_row = _WeekDayNames(self.week_day_names)
        self.add_widget(self._weekday_row)

        self._grid = GridLayout(cols=7, size_hint_y=None, spacing=2)
        self._grid.bind(minimum_height=self._grid.setter('height'))
        self.add_widget(self._grid)

        self.bind(
            mode=self._render,
            selected_date=self._render,
            selected_range=self._render,
            selected_dates=self._render,
            min_value=self._render,
            max_value=self._render,
            is_date_disabled=self._render,
            disabled=self._render,
            readonly=self._render,
            fixed_weeks=self._render,
            show_outside_days=self._render,
            month_controls=self._render,
            year_controls=self._render,
            color=self._render,
            _view_year=self._render,
            _view_month=self._render,
            week_day_names=self._on_weekdays_change,
        )

        Clock.schedule_once(self._render, 0)

    # -- Public API -----------------------------------------------------

    def goto(self, year, month):
        """Programmatically navigate the calendar to ``year`` / ``month``."""
        self._view_year, self._view_month = year, month

    def clear_selection(self):
        """Reset every selection mode to an empty state."""
        self.selected_date = None
        self.selected_range = None
        self.selected_dates = []
        self._pending_range_start = None

    # -- Default event handlers (Kivy requires them to exist) -----------

    def on_date_select(self, *_):
        pass

    def on_range_select(self, *_):
        pass

    def on_dates_change(self, *_):
        pass

    # -- Internal helpers ----------------------------------------------

    def _initial_view_date(self):
        if self.mode == 'single' and self.selected_date is not None:
            return _to_date(self.selected_date)
        if self.mode == 'range' and self.selected_range:
            start, _end = self.selected_range
            return _to_date(start)
        if self.mode == 'multiple' and self.selected_dates:
            return _to_date(self.selected_dates[0])
        return _date.today()

    def _build_navbar(self):
        from gakoui.widgets.ubutton import UButton

        bar = BoxLayout(orientation='horizontal', size_hint_y=None,
                        height=44, spacing=4, padding=[6, 4, 6, 4])

        self._prev_year_btn = UButton(
            color=self.color, variant='ghost', text='\u00ab',
            size_hint_x=None, width=36,
        )
        self._prev_year_btn.bind(on_release=lambda *_: self._shift_year(-1))

        self._prev_month_btn = UButton(
            color=self.color, variant='ghost',
            left_icon='material-symbols--arrow-back-ios-new-rounded.png',
            size_hint_x=None, width=36,
        )
        self._prev_month_btn.bind(on_release=lambda *_: self._shift_month(-1))

        self._month_label = Label(
            text='', color=(1, 1, 1, 1), bold=True, font_size='15sp',
        )

        self._next_month_btn = UButton(
            color=self.color, variant='ghost',
            left_icon='material-symbols--arrow-forward-ios-rounded.png',
            size_hint_x=None, width=36,
        )
        self._next_month_btn.bind(on_release=lambda *_: self._shift_month(1))

        self._next_year_btn = UButton(
            color=self.color, variant='ghost', text='\u00bb',
            size_hint_x=None, width=36,
        )
        self._next_year_btn.bind(on_release=lambda *_: self._shift_year(1))

        bar.add_widget(self._prev_year_btn)
        bar.add_widget(self._prev_month_btn)
        bar.add_widget(self._month_label)
        bar.add_widget(self._next_month_btn)
        bar.add_widget(self._next_year_btn)
        return bar

    def _shift_month(self, delta):
        if self.disabled or not self.month_controls:
            return
        dt = datetime(self._view_year, self._view_month, 1) + relativedelta(months=delta)
        self._view_year, self._view_month = dt.year, dt.month

    def _shift_year(self, delta):
        if self.disabled or not self.year_controls:
            return
        dt = datetime(self._view_year, self._view_month, 1) + relativedelta(years=delta)
        self._view_year, self._view_month = dt.year, dt.month

    def _on_weekdays_change(self, *_):
        # Rebuild the weekday header in-place.
        idx = self.children.index(self._weekday_row)
        self.remove_widget(self._weekday_row)
        self._weekday_row = _WeekDayNames(self.week_day_names)
        self.add_widget(self._weekday_row, index=idx)
        self._render()

    # -- Predicates -----------------------------------------------------

    def _is_disabled(self, d):
        if self.disabled:
            return True
        mn = _to_date(self.min_value)
        mx = _to_date(self.max_value)
        if mn is not None and d < mn:
            return True
        if mx is not None and d > mx:
            return True
        if callable(self.is_date_disabled) and self.is_date_disabled(d):
            return True
        return False

    def _is_selected(self, d):
        if self.mode == 'single':
            sd = _to_date(self.selected_date)
            return sd is not None and sd == d
        if self.mode == 'range':
            if self.selected_range:
                s, e = self.selected_range
                return d == _to_date(s) or d == _to_date(e)
            if self._pending_range_start is not None:
                return d == _to_date(self._pending_range_start)
            return False
        if self.mode == 'multiple':
            return any(d == _to_date(x) for x in self.selected_dates)
        return False

    def _is_in_range(self, d):
        if self.mode != 'range' or not self.selected_range:
            return False
        s, e = self.selected_range
        s, e = _to_date(s), _to_date(e)
        if s is None or e is None:
            return False
        lo, hi = (s, e) if s <= e else (e, s)
        return lo < d < hi

    def _is_today(self, d):
        return d == _date.today()

    # -- Rendering ------------------------------------------------------

    def _month_dates(self, year, month):
        """Return the list of weeks (each a list of 7 ``date`` objects).

        If ``fixed_weeks`` is True the result is padded to 6 weeks by
        appending dates from the following month.
        """
        cal = _PyCalendar(firstweekday=0)
        weeks = cal.monthdatescalendar(year, month)
        if self.fixed_weeks and len(weeks) < 6:
            last = weeks[-1][-1]
            weeks.append([last + timedelta(days=i) for i in range(1, 8)])
        return weeks

    def _render(self, *_):
        # Navbar
        self._month_label.text = datetime(
            self._view_year, self._view_month, 1
        ).strftime("%B %Y")

        for btn, visible in (
            (self._prev_year_btn, self.year_controls),
            (self._next_year_btn, self.year_controls),
            (self._prev_month_btn, self.month_controls),
            (self._next_month_btn, self.month_controls),
        ):
            btn.opacity = 1 if visible else 0
            btn.disabled = self.disabled or not visible

        # Grid
        self._grid.clear_widgets()
        from gakoui.widgets.ubutton import UButton

        weeks = self._month_dates(self._view_year, self._view_month)
        for week in weeks:
            for d in week:
                in_view = (d.month == self._view_month and d.year == self._view_year)
                cell = _DayCell(color=self.color)
                cell.in_range = self._is_in_range(d) and in_view

                if not in_view and not self.show_outside_days:
                    cell.add_widget(Widget())
                    self._grid.add_widget(cell)
                    continue

                selected = self._is_selected(d)
                disabled = self._is_disabled(d)
                today = self._is_today(d)

                if selected:
                    variant, btn_color = 'solid', self.color
                elif today and in_view:
                    variant, btn_color = 'outline', self.color
                elif in_view:
                    variant, btn_color = 'ghost', self.color
                else:
                    variant, btn_color = 'ghost', 'stone'

                btn = UButton(
                    text=str(d.day),
                    color=btn_color,
                    variant=variant,
                    rounded=True,
                    font_size='14sp',
                )
                btn.disabled = disabled
                if not (self.readonly or disabled):
                    btn.bind(on_release=partial(self._on_day_release, d))
                cell.add_widget(btn)
                self._grid.add_widget(cell)

    # -- Click handling -------------------------------------------------

    def _on_day_release(self, d, *_):
        if self.disabled or self.readonly or self._is_disabled(d):
            return

        # Clicking an outside-month day navigates to that month first.
        if d.month != self._view_month or d.year != self._view_year:
            self._view_year, self._view_month = d.year, d.month

        if self.mode == 'single':
            self.selected_date = _to_datetime(d)
            self.dispatch('on_date_select', self.selected_date)

        elif self.mode == 'range':
            if self._pending_range_start is None or self.selected_range is not None:
                # Start a new range (clears any previous one).
                self.selected_range = None
                self._pending_range_start = _to_datetime(d)
                self._render()
            else:
                start = _to_date(self._pending_range_start)
                end = d
                if end < start:
                    start, end = end, start
                self.selected_range = (_to_datetime(start), _to_datetime(end))
                self._pending_range_start = None
                self.dispatch(
                    'on_range_select',
                    self.selected_range[0], self.selected_range[1],
                )

        elif self.mode == 'multiple':
            existing = [_to_date(x) for x in self.selected_dates]
            if d in existing:
                self.selected_dates = [
                    x for x in self.selected_dates if _to_date(x) != d
                ]
            else:
                self.selected_dates = list(self.selected_dates) + [_to_datetime(d)]
            self.dispatch('on_dates_change', list(self.selected_dates))


# ---------------------------------------------------------------------------
# Picker base — trigger button + popover calendar
# ---------------------------------------------------------------------------


class _CalendarPickerBase(BoxLayout):
    """Shared base for the trigger-button + popover-calendar pickers."""

    text = StringProperty('')
    color = StringProperty('sky')
    variant = StringProperty('outline')
    left_icon = StringProperty('material-symbols--calendar-month-rounded.png')

    placeholder = StringProperty('Pick a date')
    date_format = StringProperty('%d %b %Y')

    # Passed through to the inner UCalendar
    min_value = ObjectProperty(None, allownone=True)
    max_value = ObjectProperty(None, allownone=True)
    is_date_disabled = ObjectProperty(None, allownone=True)
    fixed_weeks = BooleanProperty(True)
    show_outside_days = BooleanProperty(True)
    month_controls = BooleanProperty(True)
    year_controls = BooleanProperty(True)
    readonly = BooleanProperty(False)

    _mode = 'single'  # overridden in subclasses

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from gakoui.widgets.ubutton import UButton

        self.size_hint_y = None
        self.height = 44

        self.button = UButton(
            text=self.text or self.placeholder,
            color=self.color, variant=self.variant,
            left_icon=self.left_icon,
        )
        self.button.bind(on_release=self._open_dropdown)
        self.add_widget(self.button)

        self.calendar = UCalendar(
            mode=self._mode,
            color=self.color,
            min_value=self.min_value,
            max_value=self.max_value,
            is_date_disabled=self.is_date_disabled,
            fixed_weeks=self.fixed_weeks,
            show_outside_days=self.show_outside_days,
            month_controls=self.month_controls,
            year_controls=self.year_controls,
            readonly=self.readonly,
        )

        self.dropdown = DatePickerDropDown()
        self.dropdown.add_widget(self.calendar)

        # Wrapper ⇄ inner-widgets sync
        self.bind(
            text=self._sync_button_text,
            placeholder=self._sync_button_text,
            color=self._sync_color,
            variant=self._sync_button_variant,
            left_icon=self._sync_button_icon,
            min_value=lambda *_: setattr(self.calendar, 'min_value', self.min_value),
            max_value=lambda *_: setattr(self.calendar, 'max_value', self.max_value),
            is_date_disabled=lambda *_: setattr(self.calendar, 'is_date_disabled', self.is_date_disabled),
            fixed_weeks=lambda *_: setattr(self.calendar, 'fixed_weeks', self.fixed_weeks),
            show_outside_days=lambda *_: setattr(self.calendar, 'show_outside_days', self.show_outside_days),
            month_controls=lambda *_: setattr(self.calendar, 'month_controls', self.month_controls),
            year_controls=lambda *_: setattr(self.calendar, 'year_controls', self.year_controls),
            readonly=lambda *_: setattr(self.calendar, 'readonly', self.readonly),
        )

    def _open_dropdown(self, *_):
        self.dropdown.open(self.button)

    def _sync_button_text(self, *_):
        self.button.text = self.text or self.placeholder

    def _sync_color(self, *_):
        self.button.color = self.color
        self.calendar.color = self.color

    def _sync_button_variant(self, *_):
        self.button.variant = self.variant

    def _sync_button_icon(self, *_):
        self.button.left_icon = self.left_icon


# ---------------------------------------------------------------------------
# Concrete pickers
# ---------------------------------------------------------------------------


class DatePicker(_CalendarPickerBase):
    """Single-date picker (trigger button + popover calendar)."""

    _mode = 'single'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calendar.bind(
            on_date_select=self._on_date_select,
            selected_date=lambda *_: self._update_label(),
        )
        self._update_label()

    def _get_selected_date(self):
        return self.calendar.selected_date

    def _set_selected_date(self, value):
        self.calendar.selected_date = value
        return True

    selected_date = AliasProperty(
        _get_selected_date, _set_selected_date, bind=[],
    )

    def _on_date_select(self, _cal, _value):
        self.property('selected_date').dispatch(self)
        self.dropdown.dismiss()

    def _update_label(self, *_):
        value = self.calendar.selected_date
        if value is None:
            self.text = ''
        else:
            self.text = _to_datetime(value).strftime(self.date_format)


class DateRangePicker(_CalendarPickerBase):
    """Date-range picker (trigger button + popover calendar, range mode)."""

    _mode = 'range'

    def __init__(self, **kwargs):
        kwargs.setdefault('placeholder', 'Pick a date range')
        super().__init__(**kwargs)
        self.calendar.bind(
            on_range_select=self._on_range_select,
            selected_range=lambda *_: self._update_label(),
        )
        self._update_label()

    def _get_selected_range(self):
        return self.calendar.selected_range

    def _set_selected_range(self, value):
        self.calendar.selected_range = value
        return True

    selected_range = AliasProperty(
        _get_selected_range, _set_selected_range, bind=[],
    )

    def _on_range_select(self, _cal, _start, _end):
        self.property('selected_range').dispatch(self)
        self.dropdown.dismiss()

    def _update_label(self, *_):
        rng = self.calendar.selected_range
        if rng:
            s, e = rng
            self.text = (
                f"{_to_datetime(s).strftime(self.date_format)} "
                f"\u2013 {_to_datetime(e).strftime(self.date_format)}"
            )
        else:
            self.text = ''


class MultiDatePicker(_CalendarPickerBase):
    """Multi-date picker (trigger button + popover calendar, multiple mode)."""

    _mode = 'multiple'

    def __init__(self, **kwargs):
        kwargs.setdefault('placeholder', 'Pick dates')
        super().__init__(**kwargs)
        self.calendar.bind(
            selected_dates=lambda *_: self._update_label(),
            on_dates_change=lambda *_: self.property('selected_dates').dispatch(self),
        )
        self._update_label()

    def _get_selected_dates(self):
        return list(self.calendar.selected_dates)

    def _set_selected_dates(self, value):
        self.calendar.selected_dates = list(value or [])
        return True

    selected_dates = AliasProperty(
        _get_selected_dates, _set_selected_dates, bind=[],
    )

    def _update_label(self, *_):
        n = len(self.calendar.selected_dates)
        if n == 0:
            self.text = ''
        elif n == 1:
            self.text = _to_datetime(
                self.calendar.selected_dates[0]
            ).strftime(self.date_format)
        else:
            self.text = f"{n} dates selected"


Builder.load_string(KV)
