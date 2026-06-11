from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty, AliasProperty, NumericProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.animation import Animation
from gakoui.data.colors import colors
from gakoui.behaviors import HoverBehavior

KV = """
<USlider>:
    orientation: 'horizontal'
    size_hint_y: None
    height: root.slider_height
    canvas.before:
        # Track de fond
        Color:
            rgba: root.track_bg_color
        RoundedRectangle:
            size: self.width, root.track_thickness
            pos: self.x, self.center_y - root.track_thickness/2
            radius: [root.track_thickness/2]
        
        # Track de progression
        Color:
            rgba: root.track_fill_color
        RoundedRectangle:
            size: root.fill_width, root.track_thickness
            pos: self.x, self.center_y - root.track_thickness/2
            radius: [root.track_thickness/2]
        
        # Thumb (bouton)
        Color:
            rgba: root.thumb_color
        Ellipse:
            size: root.thumb_size, root.thumb_size
            pos: root.thumb_x - root.thumb_size/2, self.center_y - root.thumb_size/2

<USliderContainer>:
    orientation: 'vertical'
    spacing: 8
    size_hint_y: None
    height: self.minimum_height

<USliderLabel>:
    size_hint_y: None
    height: self.texture_size[1]
    text_size: self.width, None
    color: 1, 1, 1, 1
    font_size: '14sp'

<USliderValue>:
    size_hint_y: None
    height: self.texture_size[1]
    text_size: self.width, None
    color: 0.8, 0.8, 0.8, 1
    font_size: '12sp'
    halign: 'right'
"""


class USliderLabel(Label):
    pass


class USliderValue(Label):
    pass


class USliderContainer(BoxLayout):
    pass


class USlider(HoverBehavior, ButtonBehavior, BoxLayout):
    # Propriétés principales
    value = NumericProperty(0)
    min_value = NumericProperty(0)
    max_value = NumericProperty(100)
    step = NumericProperty(1)
    color = StringProperty('blue')
    disabled = BooleanProperty(False)
    
    # Propriétés de style
    slider_height = NumericProperty(40)
    track_thickness = NumericProperty(6)
    thumb_size = NumericProperty(20)
    
    # Propriétés de couleur
    track_bg_color = ListProperty([0.3, 0.3, 0.3, 1])
    track_fill_color = ListProperty([0.3, 0.6, 1, 1])
    thumb_color = ListProperty([1, 1, 1, 1])
    
    # Propriétés calculées
    fill_width = NumericProperty(0)
    thumb_x = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(value=self._update_position)
        self.bind(min_value=self._update_position, max_value=self._update_position)
        self.bind(size=self._update_position, pos=self._update_position)
        self.bind(color=self._update_colors)
        self.bind(hovered=self._update_colors, disabled=self._update_colors)
        
        # Variables pour le drag
        self._dragging = False
        
        self._update_colors()
        self._update_position()
    
    def _update_position(self, *args):
        """Met à jour la position du thumb et la largeur de remplissage"""
        if self.max_value <= self.min_value:
            return
        
        # Calculer la position relative (0-1)
        relative_value = (self.value - self.min_value) / (self.max_value - self.min_value)
        relative_value = max(0, min(1, relative_value))  # Clamp entre 0 et 1
        
        # Calculer les positions
        self.fill_width = self.width * relative_value
        self.thumb_x = self.x + self.width * relative_value
    
    def _update_colors(self, *args):
        """Met à jour les couleurs selon l'état"""
        color_data = colors.get(self.color, colors['blue'])
        
        if self.disabled:
            # État désactivé
            self.track_bg_color = [0.2, 0.2, 0.2, 1]
            self.track_fill_color = [0.4, 0.4, 0.4, 1]
            self.thumb_color = [0.6, 0.6, 0.6, 1]
        else:
            # Track de fond
            self.track_bg_color = [0.3, 0.3, 0.3, 1]
            
            # Track de progression
            base_color = color_data.get('fill', [0.3, 0.6, 1, 1])
            if self.hovered or self._dragging:
                # Plus lumineux au hover/drag
                self.track_fill_color = [min(1, base_color[0] * 1.1), 
                                       min(1, base_color[1] * 1.1), 
                                       min(1, base_color[2] * 1.1), 
                                       base_color[3]]
            else:
                self.track_fill_color = base_color
            
            # Thumb
            if self.hovered or self._dragging:
                self.thumb_color = [1, 1, 1, 1]
            else:
                self.thumb_color = [0.95, 0.95, 0.95, 1]
    
    def _get_value_from_pos(self, x):
        """Calcule la valeur selon la position X"""
        if self.width <= 0:
            return self.min_value
        
        # Position relative (0-1)
        relative_x = (x - self.x) / self.width
        relative_x = max(0, min(1, relative_x))  # Clamp entre 0 et 1
        
        # Valeur correspondante
        raw_value = self.min_value + relative_x * (self.max_value - self.min_value)
        
        # Appliquer le step
        if self.step > 0:
            steps = round((raw_value - self.min_value) / self.step)
            return self.min_value + steps * self.step
        else:
            return raw_value
    
    def on_touch_down(self, touch):
        if not self.disabled and self.collide_point(*touch.pos):
            self._dragging = True
            self.value = self._get_value_from_pos(touch.x)
            self._update_colors()
            touch.grab(self)
            return True
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if touch.grab_current is self and self._dragging:
            self.value = self._get_value_from_pos(touch.x)
            return True
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self._dragging = False
            self._update_colors()
            touch.ungrab(self)
            return True
        return super().on_touch_up(touch)
    
    def on_enter(self, *args):
        """Effet hover"""
        from kivy.core.window import Window
        if not self.disabled:
            Window.set_system_cursor('hand')
    
    def on_leave(self, *args):
        """Fin effet hover"""
        from kivy.core.window import Window
        Window.set_system_cursor('arrow')
    
    def set_value(self, value):
        """Définit la valeur avec validation"""
        self.value = max(self.min_value, min(self.max_value, value))
    
    def get_percentage(self):
        """Retourne la valeur en pourcentage (0-100)"""
        if self.max_value <= self.min_value:
            return 0
        return ((self.value - self.min_value) / (self.max_value - self.min_value)) * 100


def create_slider_with_label(text="", value=0, min_value=0, max_value=100, **slider_kwargs):
    """Fonction utilitaire pour créer un slider avec label et valeur"""
    container = USliderContainer()
    
    # Header avec label et valeur
    header = BoxLayout(orientation='horizontal', size_hint_y=None, height=20)
    
    if text:
        label = USliderLabel(text=text, size_hint_x=0.7)
        header.add_widget(label)
    
    value_label = USliderValue(text=str(value), size_hint_x=0.3)
    header.add_widget(value_label)
    
    container.add_widget(header)
    
    # Slider
    slider = USlider(
        value=value,
        min_value=min_value,
        max_value=max_value,
        **slider_kwargs
    )
    
    # Lier la valeur au label
    def update_value_label(instance, value):
        if slider_kwargs.get('step', 1) >= 1:
            value_label.text = str(int(value))
        else:
            value_label.text = f"{value:.1f}"
    
    slider.bind(value=update_value_label)
    
    container.add_widget(slider)
    
    return container, slider


def create_range_slider(min_val=0, max_val=100, low_value=25, high_value=75, **kwargs):
    """Fonction utilitaire pour créer un slider de plage (range slider)"""
    # Pour l'instant, retourne deux sliders séparés
    # Une implémentation complète nécessiterait un widget dédié
    container = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
    container.bind(minimum_height=container.setter('height'))
    
    low_container, low_slider = create_slider_with_label(
        text="Minimum",
        value=low_value,
        min_value=min_val,
        max_value=max_val,
        **kwargs
    )
    
    high_container, high_slider = create_slider_with_label(
        text="Maximum", 
        value=high_value,
        min_value=min_val,
        max_value=max_val,
        **kwargs
    )
    
    # Lier les sliders pour éviter le chevauchement
    def update_low(instance, value):
        if value >= high_slider.value:
            high_slider.value = min(max_val, value + 1)
    
    def update_high(instance, value):
        if value <= low_slider.value:
            low_slider.value = max(min_val, value - 1)
    
    low_slider.bind(value=update_low)
    high_slider.bind(value=update_high)
    
    container.add_widget(low_container)
    container.add_widget(high_container)
    
    return container, (low_slider, high_slider)


Builder.load_string(KV)