from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty, BooleanProperty, AliasProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle
from gakoui.data.colors import colors

KV = """
<UBadge>:
    size_hint: None, None
    size: self.texture_size[0] + root.padding_x, root.badge_height
    text_size: None, None
    halign: 'center'
    valign: 'middle'
    color: root.text_color
    font_size: root.font_size
    canvas.before:
        Color:
            rgba: root.background_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [root.radius_value]

<UBadgeDot>:
    size_hint: None, None
    size: root.dot_size, root.dot_size
    canvas.before:
        Color:
            rgba: root.dot_color
        Ellipse:
            size: self.size
            pos: self.pos

<UBadgeNumber>:
    size_hint: None, None
    size: max(root.min_size, self.texture_size[0] + root.padding_x), root.badge_height
    text_size: None, None
    halign: 'center'
    valign: 'middle'
    color: root.text_color
    font_size: root.font_size
    canvas.before:
        Color:
            rgba: root.background_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [root.radius_value]
"""


class UBadgeDot(Label):
    """Badge point simple pour les notifications"""
    color_theme = StringProperty('red')
    dot_size = NumericProperty(8)
    
    def _get_dot_color(self):
        """Couleur du point"""
        color_data = colors.get(self.color_theme, colors['red'])
        return color_data.get('fill', [1, 0, 0, 1])
    
    dot_color = AliasProperty(_get_dot_color, None, bind=['color_theme'])


class UBadgeNumber(Label):
    """Badge numérique pour compter les notifications"""
    color_theme = StringProperty('red')
    variant = StringProperty('solid')  # 'solid', 'outline'
    size_variant = StringProperty('small')  # 'small', 'medium'
    max_count = NumericProperty(99)  # Affiche 99+ au-delà
    count = NumericProperty(0)
    
    # Propriétés de taille
    badge_height = NumericProperty(20)
    min_size = NumericProperty(20)
    padding_x = NumericProperty(8)
    font_size = NumericProperty(11)
    radius_value = NumericProperty(10)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(count=self._update_text)
        self.bind(size_variant=self._update_sizes)
        self._update_sizes()
        self._update_text()
    
    def _update_sizes(self, *args):
        """Met à jour les tailles selon le variant"""
        if self.size_variant == 'small':
            self.badge_height = 18
            self.min_size = 18
            self.padding_x = 6
            self.font_size = 10
            self.radius_value = 9
        else:  # medium
            self.badge_height = 22
            self.min_size = 22
            self.padding_x = 8
            self.font_size = 12
            self.radius_value = 11
    
    def _update_text(self, *args):
        """Met à jour le texte selon le count"""
        if self.count > self.max_count:
            self.text = f"{self.max_count}+"
        else:
            self.text = str(self.count)
    
    def _get_background_color(self):
        """Couleur de fond selon le variant"""
        color_data = colors.get(self.color_theme, colors['red'])
        if self.variant == 'solid':
            return color_data.get('fill', [1, 0, 0, 1])
        else:  # outline
            return [0, 0, 0, 0]  # Transparent
    
    background_color = AliasProperty(_get_background_color, None, bind=['color_theme', 'variant'])
    
    def _get_text_color(self):
        """Couleur du texte selon le variant"""
        color_data = colors.get(self.color_theme, colors['red'])
        if self.variant == 'solid':
            return color_data.get('font', [1, 1, 1, 1])
        else:  # outline
            return color_data.get('fill', [1, 0, 0, 1])
    
    text_color = AliasProperty(_get_text_color, None, bind=['color_theme', 'variant'])


class UBadge(Label):
    """Badge texte général"""
    color_theme = StringProperty('gray')
    variant = StringProperty('solid')  # 'solid', 'outline', 'soft'
    size_variant = StringProperty('small')  # 'small', 'medium', 'large'
    rounded = BooleanProperty(False)  # Badge complètement arrondi
    
    # Propriétés de taille
    badge_height = NumericProperty(24)
    padding_x = NumericProperty(12)
    font_size = NumericProperty(12)
    radius_value = NumericProperty(6)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size_variant=self._update_sizes)
        self.bind(rounded=self._update_radius)
        self._update_sizes()
    
    def _update_sizes(self, *args):
        """Met à jour les tailles selon le variant"""
        size_map = {
            'small': {'height': 20, 'padding': 8, 'font': 10, 'radius': 4},
            'medium': {'height': 24, 'padding': 12, 'font': 12, 'radius': 6},
            'large': {'height': 28, 'padding': 16, 'font': 14, 'radius': 8}
        }
        
        sizes = size_map.get(self.size_variant, size_map['small'])
        self.badge_height = sizes['height']
        self.padding_x = sizes['padding']
        self.font_size = sizes['font']
        if not self.rounded:
            self.radius_value = sizes['radius']
        self._update_radius()
    
    def _update_radius(self, *args):
        """Met à jour le radius selon l'option rounded"""
        if self.rounded:
            self.radius_value = self.badge_height / 2
    
    def _get_background_color(self):
        """Couleur de fond selon le variant"""
        color_data = colors.get(self.color_theme, colors['stone'])
        
        if self.variant == 'solid':
            return color_data.get('fill', [0.5, 0.5, 0.5, 1])
        elif self.variant == 'outline':
            return [0, 0, 0, 0]  # Transparent
        else:  # soft
            base_color = color_data.get('fill', [0.5, 0.5, 0.5, 1])
            # Version plus transparente pour l'effet "soft"
            return [base_color[0], base_color[1], base_color[2], 0.2]
    
    background_color = AliasProperty(_get_background_color, None, bind=['color_theme', 'variant'])
    
    def _get_text_color(self):
        """Couleur du texte selon le variant"""
        color_data = colors.get(self.color_theme, colors['stone'])
        
        if self.variant == 'solid':
            return color_data.get('font', [1, 1, 1, 1])
        else:  # outline ou soft
            return color_data.get('fill', [0.5, 0.5, 0.5, 1])
    
    text_color = AliasProperty(_get_text_color, None, bind=['color_theme', 'variant'])


def create_status_badge(status='success', text=''):
    """Fonction utilitaire pour créer des badges de statut prédéfinis"""
    status_map = {
        'success': {'color': 'green', 'text': text or 'Succès'},
        'error': {'color': 'red', 'text': text or 'Erreur'},
        'warning': {'color': 'orange', 'text': text or 'Attention'},
        'info': {'color': 'blue', 'text': text or 'Info'},
        'pending': {'color': 'yellow', 'text': text or 'En attente'},
        'new': {'color': 'purple', 'text': text or 'Nouveau'}
    }
    
    config = status_map.get(status, status_map['info'])
    return UBadge(
        text=config['text'],
        color_theme=config['color'],
        variant='solid',
        size_variant='small'
    )


def create_notification_badge(count=0, color='red', size='small'):
    """Fonction utilitaire pour créer des badges de notification"""
    if count == 0:
        return UBadgeDot(color_theme=color, dot_size=8 if size == 'small' else 10)
    else:
        return UBadgeNumber(
            count=count,
            color_theme=color,
            size_variant=size
        )


Builder.load_string(KV)