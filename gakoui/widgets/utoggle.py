from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty, AliasProperty, NumericProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.animation import Animation
from gakoui.data.colors import colors
from gakoui.behaviors import HoverBehavior

KV = """
<UToggle>:
    size_hint: None, None
    size: root.toggle_width, root.toggle_height

<UToggleLabel>:
    size_hint_y: None
    height: self.texture_size[1]
    text_size: self.width, None
    color: 1, 1, 1, 1
    font_size: '14sp'

<UToggleContainer>:
    orientation: 'horizontal'
    spacing: 10
    size_hint: None, None
    size: self.minimum_width, self.minimum_height
"""


class UToggleLabel(BoxLayout):
    pass


class UToggleContainer(BoxLayout):
    pass


class UToggle(HoverBehavior, ButtonBehavior, BoxLayout):
    # Propriétés principales
    active = BooleanProperty(False)
    color = StringProperty('green')
    size_variant = StringProperty('medium')  # 'small', 'medium', 'large'
    disabled = BooleanProperty(False)
    
    # Propriétés de taille
    toggle_width = NumericProperty(50)
    toggle_height = NumericProperty(24)
    thumb_size = NumericProperty(20)
    thumb_padding = NumericProperty(2)
    
    # Propriétés de couleur
    track_color = ListProperty([0.3, 0.3, 0.3, 1])
    thumb_color = ListProperty([0.95, 0.95, 0.95, 1])
    
    def __init__(self, **kwargs):
        # Initialiser les attributs avant super().__init__
        self._thumb_anim = None
        self._thumb_x_pos = 0
        
        super().__init__(**kwargs)
        
        self.bind(active=self._update_thumb_position)
        self.bind(size_variant=self._update_sizes)
        self.bind(pos=self._update_graphics, size=self._update_graphics)
        self.bind(active=self._update_colors, color=self._update_colors)
        self.bind(hovered=self._update_colors, disabled=self._update_colors)
        
        self._update_sizes()
        self._update_colors()
        self._update_thumb_position()
        self._update_graphics()
    
    def _update_sizes(self, *args):
        """Met à jour les tailles selon le variant"""
        size_map = {
            'small': {'width': 40, 'height': 20, 'thumb': 16, 'padding': 2},
            'medium': {'width': 50, 'height': 24, 'thumb': 20, 'padding': 2},
            'large': {'width': 60, 'height': 28, 'thumb': 24, 'padding': 2}
        }
        
        sizes = size_map.get(self.size_variant, size_map['medium'])
        self.toggle_width = sizes['width']
        self.toggle_height = sizes['height']
        self.thumb_size = sizes['thumb']
        self.thumb_padding = sizes['padding']
    
    def _update_thumb_position(self, *args):
        """Met à jour la position du thumb avec animation"""
        if self.active:
            target_x = self.x + self.toggle_width - self.thumb_size - self.thumb_padding
        else:
            target_x = self.x + self.thumb_padding
        
        # Animation fluide du thumb
        if self._thumb_anim:
            self._thumb_anim.cancel(self)
        
        self._thumb_anim = Animation(
            _thumb_x_pos=target_x,
            duration=0.2,
            transition='out_cubic'
        )
        self._thumb_anim.start(self)
    
    def _update_colors(self, *args):
        """Met à jour les couleurs selon l'état"""
        # Couleur du track
        if self.disabled:
            self.track_color = [0.3, 0.3, 0.3, 1]
        elif self.active:
            color_data = colors.get(self.color, colors['green'])
            base_color = color_data.get('fill', [0.3, 0.8, 0.3, 1])
            if self.hovered:
                self.track_color = [min(1, base_color[0] * 1.1), 
                                   min(1, base_color[1] * 1.1), 
                                   min(1, base_color[2] * 1.1), 
                                   base_color[3]]
            else:
                self.track_color = base_color
        else:
            if self.hovered:
                self.track_color = [0.4, 0.4, 0.4, 1]
            else:
                self.track_color = [0.3, 0.3, 0.3, 1]
        
        # Couleur du thumb
        if self.disabled:
            self.thumb_color = [0.6, 0.6, 0.6, 1]
        elif self.hovered:
            self.thumb_color = [1, 1, 1, 1]
        else:
            self.thumb_color = [0.95, 0.95, 0.95, 1]
    
    def _update_graphics(self, *args):
        """Met à jour les graphiques du toggle"""
        self.canvas.before.clear()
        with self.canvas.before:
            # Track (fond)
            Color(*self.track_color)
            RoundedRectangle(
                size=(self.toggle_width, self.toggle_height),
                pos=self.pos,
                radius=[self.toggle_height/2]
            )
            
            # Thumb (bouton)
            Color(*self.thumb_color)
            thumb_x = getattr(self, '_thumb_x_pos', self.x + self.thumb_padding)
            thumb_y = self.y + (self.toggle_height - self.thumb_size) / 2
            Ellipse(
                size=(self.thumb_size, self.thumb_size),
                pos=(thumb_x, thumb_y)
            )
    
    def on_release(self):
        """Bascule l'état du toggle"""
        if not self.disabled:
            self.active = not self.active
    
    def on_enter(self, *args):
        """Effet hover"""
        from kivy.core.window import Window
        if not self.disabled:
            Window.set_system_cursor('hand')
    
    def on_leave(self, *args):
        """Fin effet hover"""
        from kivy.core.window import Window
        Window.set_system_cursor('arrow')


def create_toggle_with_label(text="", **toggle_kwargs):
    """Fonction utilitaire pour créer un toggle avec label"""
    container = UToggleContainer()
    
    toggle = UToggle(**toggle_kwargs)
    container.add_widget(toggle)
    
    if text:
        from kivy.uix.label import Label
        label = Label(
            text=text,
            size_hint_y=None,
            height=toggle.toggle_height,
            color=(1, 1, 1, 1),
            font_size='14sp'
        )
        container.add_widget(label)
    
    return container, toggle


Builder.load_string(KV)