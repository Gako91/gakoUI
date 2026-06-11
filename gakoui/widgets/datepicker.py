from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty, NumericProperty, AliasProperty, ObjectProperty
from kivy.clock import Clock
from calendar import Calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from functools import partial


KV = """
#:import rgba kivy.utils.rgba


<WeekDayNames>:
    padding: [10,0,10,0]
    size_hint_y: None
    height: 44
    
<DatePicker>:
    left_icon: 'material-symbols--calendar-month-rounded.png'

<Month>:
    spacing: 10
    orientation: 'vertical'
    size_hint_y: None
    height: 44*6
    padding: [10,0,10,10]
    
<Week>:
    size_hint_y: None
    height: 36




<DatePickerDropDown>:
    canvas.before:
        Color:
            rgba: rgba('#0f172a')
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [10]
        Color:
            rgba: .5,.5,.5,1
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 10, 10, 10, 10, 100)
    size_hint_x: None
    width: self.height/8*7
    auto_width: True
"""


class NavBar(BoxLayout):
    month_object = ObjectProperty(None)
    _date_string = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 44
        self.spacing = 30
        self.padding = [10, 10, 10, 10]
        
        # Import local pour éviter l'import circulaire
        from gakoui.widgets.ubutton import UButton
        
        self.prev_button = UButton(
            color='sky',
            variant='ghost',
            left_icon='material-symbols--arrow-back-ios-new-rounded.png',
            size_hint_x=None,
            width=44
        )
        self.prev_button.bind(on_release=lambda x: self.change_month(-1))
        
        self.month_label = UButton(
            color='sky',
            variant='ghost',
            text=self._date_string
        )
        
        self.next_button = UButton(
            color='sky',
            variant='ghost',
            left_icon='material-symbols--arrow-forward-ios-rounded.png',
            size_hint_x=None,
            width=44
        )
        self.next_button.bind(on_release=lambda x: self.change_month(1))
        
        self.add_widget(self.prev_button)
        self.add_widget(self.month_label)
        self.add_widget(self.next_button)
        
        self.bind(_date_string=self._update_month_label)

    def _update_month_label(self, *args):
        if hasattr(self, 'month_label'):
            self.month_label.text = self._date_string

    def change_month(self, add_month=1):
        dt = datetime.fromtimestamp(self.month_object._timestamp)
        dt = dt + relativedelta(months=add_month)
        dt = int(dt.timestamp())
        self.month_object.set_month(dt)
        self._date_string = datetime.fromtimestamp(dt).strftime("%B %Y")


class Day(BoxLayout):
    text = StringProperty("")
    year = NumericProperty(0)
    month = NumericProperty(0)
    month_object = ObjectProperty(None)
    selected = NumericProperty(0)  # 0 = False, 1 = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Import local pour éviter l'import circulaire
        from gakoui.widgets.ubutton import UButton
        
        self.add_widget(Widget())  # Spacer gauche
        
        self.button = UButton(
            color='sky',
            rounded=True,
            text=self.text,
            size_hint_x=None,
            width=36
        )
        self.button.bind(on_release=self._on_button_release)
        self.add_widget(self.button)
        
        self.add_widget(Widget())  # Spacer droite
        
        self.bind(text=self._update_button_text)
        self.bind(selected=self._update_button_color)

    def _update_button_text(self, *args):
        if hasattr(self, 'button'):
            self.button.text = self.text

    def _update_button_color(self, *args):
        if hasattr(self, 'button'):
            self.button.color = 'green' if self.selected else 'sky'

    def _on_button_release(self, *args):
        self.select_date(self)
        self.selected = 1

    def select_date(self, day_button):
        self.month_object.select_date(day_button)


class EmptyDay(Widget):
    pass


class Week(BoxLayout):
    pass


class Month(BoxLayout):
    calendar = Calendar()
    datepicker = ObjectProperty(None)
    _timestamp = 0

    def __init__(self,timestamp,**kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(partial(self.set_month,timestamp))

    def set_month(self,timestamp, dt=0):
        self._timestamp = timestamp
        date = datetime.fromtimestamp(timestamp)
        cal = self.calendar.monthdatescalendar(date.year, date.month)
        self.clear_widgets()
        for w in cal:
            bl = Week()
            for d in w:
                if d.month == date.month:
                    bl.add_widget(Day(text=f"{d.day}", year=d.year, month=d.month, month_object=self))
                else:
                    bl.add_widget(Widget())
            self.add_widget(bl)

    def select_date(self, day_button):
        for w in self.children:
            for d in w.children:
                if isinstance(d, Day):
                    d.selected = 0
        self.datepicker._set_date(day_button.year, day_button.month, int(day_button.text))


class DatePickerDropDown(DropDown):
    pass


class WeekDayNames(BoxLayout):
    def __init__(self, wn, **kwargs):
        super().__init__(**kwargs)
        for d in wn:
            self.add_widget(Label(text=d))


class DatePicker(BoxLayout):
    week_day_names = ListProperty(['M','T','W','T','F','S','S'])
    _selected_timestamp = NumericProperty(datetime.now().timestamp())
    
    # Propriétés héritées de UButton pour la compatibilité
    text = StringProperty('')
    color = StringProperty('sky')
    variant = StringProperty('outline')
    left_icon = StringProperty('material-symbols--calendar-month-rounded.png')

    def get_selected_date(self):
        return datetime.fromtimestamp(self._selected_timestamp)

    selected_date = AliasProperty(get_selected_date,None,bind=['_selected_timestamp'])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Import local pour éviter l'import circulaire
        from gakoui.widgets.ubutton import UButton
        
        # Créer le bouton principal
        self.button = UButton(
            text=self.text,
            color=self.color,
            variant=self.variant,
            left_icon=self.left_icon
        )
        self.button.bind(on_release=self._on_button_release)
        self.add_widget(self.button)
        
        # Créer le dropdown
        self.dropdown = DatePickerDropDown()
        now = datetime.now().timestamp()
        self.month = Month(now, datepicker=self)
        self.navbar = NavBar(month_object=self.month)
        self._set_text(now)
        self.dropdown.add_widget(self.navbar)
        self.dropdown.add_widget(WeekDayNames(self.week_day_names))
        self.dropdown.add_widget(self.month)
        
        # Lier les propriétés au bouton
        self.bind(text=self._update_button_text)
        self.bind(color=self._update_button_color)
        self.bind(variant=self._update_button_variant)
        self.bind(left_icon=self._update_button_icon)
    
    def _update_button_text(self, *args):
        if hasattr(self, 'button'):
            self.button.text = self.text
    
    def _update_button_color(self, *args):
        if hasattr(self, 'button'):
            self.button.color = self.color
    
    def _update_button_variant(self, *args):
        if hasattr(self, 'button'):
            self.button.variant = self.variant
    
    def _update_button_icon(self, *args):
        if hasattr(self, 'button'):
            self.button.left_icon = self.left_icon
    
    def _on_button_release(self, *args):
        """Callback quand le bouton est cliqué"""
        self.dropdown.open(self.button)

    def _set_text(self, timestamp):
        self.text = datetime.fromtimestamp(timestamp).strftime("%-d %b, %Y")
        self._selected_timestamp = timestamp
        self.navbar._date_string = datetime.fromtimestamp(timestamp).strftime("%B %Y")

    def _set_date(self, year, month, day):
        timestamp = datetime(year, month, day).timestamp()
        self._set_text(timestamp)




Builder.load_string(KV)