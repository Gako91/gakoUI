from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle, Line
from gakoui.data.colors import colors

KV = """
<UCard>:
    orientation: 'vertical'
    spacing: 10
    canvas.before:
        Color:
            rgba: root.background_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [root.radius_value]

<UCardHeader>:
    size_hint_y: None
    height: self.minimum_height if self.children else 0
    orientation: 'vertical'
    spacing: 5

<UCardTitle>:
    size_hint_y: None
    height: self.texture_size[1] + 5
    text_size: self.width, None
    font_size: '18sp'
    bold: True
    color: 1, 1, 1, 1

<UCardDescription>:
    size_hint_y: None
    height: self.texture_size[1] + 5
    text_size: self.width, None
    font_size: '14sp'
    color: 0.7, 0.7, 0.7, 1

<UCardContent>:
    orientation: 'vertical'

<UCardFooter>:
    size_hint_y: None
    height: self.minimum_height if self.children else 0
    orientation: 'horizontal'
    spacing: 10
"""


class UCardTitle(Label):
    pass


class UCardDescription(Label):
    pass


class UCardHeader(BoxLayout):
    pass


class UCardContent(BoxLayout):
    pass


class UCardFooter(BoxLayout):
    pass


class UCard(BoxLayout):
    color = StringProperty('stone')
    variant = StringProperty('elevated')  # 'elevated', 'outlined', 'filled'
    radius = NumericProperty(10)
    card_padding = StringProperty('medium')  # 'small', 'medium', 'large'
    border_width = NumericProperty(1)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(card_padding=self._update_padding)
        self.bind(pos=self._update_graphics, size=self._update_graphics)
        self.bind(variant=self._update_graphics, color=self._update_graphics)
        self._update_padding()
        self._update_graphics()
    
    def _update_padding(self, *args):
        padding_map = {
            'small': [10, 10, 10, 10],
            'medium': [16, 16, 16, 16], 
            'large': [24, 24, 24, 24]
        }
        self.padding = padding_map.get(self.card_padding, [16, 16, 16, 16])
    
    def _update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Background
            Color(*self.background_color)
            RoundedRectangle(size=self.size, pos=self.pos, radius=[self.radius_value])
            
            # Border only if needed
            if self.variant in ['outlined', 'elevated']:
                Color(*self.border_color)
                Line(
                    rounded_rectangle=(self.x, self.y, self.width, self.height, 
                                     self.radius_value, self.radius_value, 
                                     self.radius_value, self.radius_value, 100),
                    width=self.border_width
                )
    
    def _get_radius_value(self):
        return self.radius
    
    radius_value = AliasProperty(_get_radius_value, None, bind=['radius'])
    

    
    def _get_background_color(self):
        if self.variant == 'filled':
            color_data = colors.get(self.color, colors['stone'])
            fill_color = color_data.get('fill', [0.1, 0.1, 0.1, 1])
            # Rendre la couleur plus transparente pour le fond
            return [fill_color[0], fill_color[1], fill_color[2], 0.2]
        elif self.variant == 'outlined':
            return [0, 0, 0, 0]  # Transparent
        else:  # elevated
            return [0.1, 0.1, 0.1, 0.8]  # Dark background with transparency
    
    background_color = AliasProperty(_get_background_color, None, bind=['color', 'variant'])
    
    def _get_border_color(self):
        if self.variant == 'outlined':
            color_data = colors.get(self.color, colors['stone'])
            return color_data.get('fill', [0.3, 0.3, 0.3, 1])
        elif self.variant == 'elevated':
            return [0.3, 0.3, 0.3, 0.5]  # Subtle border for elevation effect
        else:  # filled
            color_data = colors.get(self.color, colors['stone'])
            return color_data.get('fill', [0.3, 0.3, 0.3, 1])
    
    border_color = AliasProperty(_get_border_color, None, bind=['color', 'variant'])


Builder.load_string(KV)