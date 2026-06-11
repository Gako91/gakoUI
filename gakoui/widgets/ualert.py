from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty, AliasProperty, NumericProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle
from gakoui.data.colors import colors
from gakoui.behaviors import HoverBehavior

KV = """
<UAlert>:
    orientation: 'horizontal'
    spacing: 12
    padding: root.padding_value
    size_hint_y: None
    height: self.minimum_height
    canvas.before:
        Color:
            rgba: root.background_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [root.radius_value]
        Color:
            rgba: root.border_color
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, root.radius_value, root.radius_value, root.radius_value, root.radius_value, 100)
            width: root.border_width

<UAlertIcon>:
    size_hint_x: None
    width: 24
    text: root.icon_text
    font_size: 18
    color: root.icon_color
    halign: 'center'
    valign: 'middle'

<UAlertContent>:
    orientation: 'vertical'
    spacing: 4
    size_hint_y: None
    height: self.minimum_height

<UAlertTitle>:
    size_hint_y: None
    height: self.texture_size[1] if self.text else 0
    text_size: self.width, None
    font_size: 14
    bold: True
    color: root.title_color

<UAlertDescription>:
    size_hint_y: None
    height: self.texture_size[1] if self.text else 0
    text_size: self.width, None
    font_size: 12
    color: root.description_color

<UAlertCloseButton>:
    size_hint_x: None
    width: 24
    text: '×'
    font_size: 18
    color: root.close_color if not root.hovered else root.close_hover_color
    halign: 'center'
    valign: 'middle'
"""


class UAlertIcon(Label):
    icon_text = StringProperty('ℹ')
    icon_color = ListProperty([1, 1, 1, 1])


class UAlertTitle(Label):
    title_color = ListProperty([1, 1, 1, 1])


class UAlertDescription(Label):
    description_color = ListProperty([0.8, 0.8, 0.8, 1])


class UAlertContent(BoxLayout):
    pass


class UAlertCloseButton(HoverBehavior, ButtonBehavior, Label):
    alert = None
    close_color = ListProperty([0.6, 0.6, 0.6, 1])
    close_hover_color = ListProperty([1, 1, 1, 1])
    
    def __init__(self, alert=None, **kwargs):
        super().__init__(**kwargs)
        self.alert = alert
    
    def on_release(self):
        if self.alert and hasattr(self.alert, 'dismiss'):
            self.alert.dismiss()


class UAlert(BoxLayout):
    # Propriétés principales
    alert_type = StringProperty('info')  # 'success', 'error', 'warning', 'info'
    variant = StringProperty('solid')  # 'solid', 'outline', 'soft'
    title = StringProperty('')
    description = StringProperty('')
    closable = BooleanProperty(True)
    
    # Propriétés de style
    radius_value = NumericProperty(8)
    border_width = NumericProperty(1)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(alert_type=self._update_colors)
        self.bind(variant=self._update_colors)
        
        # Créer les composants
        self._create_components()
        self._update_colors()
    
    def _create_components(self):
        """Crée les composants de l'alert"""
        # Icône
        if self.alert_type:
            self.icon = UAlertIcon()
            self.icon.icon_text = self._get_icon_text()
            self.icon.icon_color = self._get_icon_color()
            self.add_widget(self.icon)
        
        # Contenu
        self.content = UAlertContent()
        
        if self.title:
            self.title_label = UAlertTitle(text=self.title)
            self.content.add_widget(self.title_label)
        
        if self.description:
            self.description_label = UAlertDescription(text=self.description)
            self.content.add_widget(self.description_label)
        
        self.add_widget(self.content)
        
        # Bouton de fermeture
        if self.closable:
            self.close_button = UAlertCloseButton(alert=self)
            self.add_widget(self.close_button)
    
    def _get_icon_text(self):
        """Retourne le texte de l'icône selon le type"""
        icon_map = {
            'success': '✓',
            'error': '✕',
            'warning': '⚠',
            'info': 'ℹ'
        }
        return icon_map.get(self.alert_type, 'ℹ')
    
    def _get_icon_color(self):
        """Retourne la couleur de l'icône selon le type"""
        color_data = colors.get(self._get_color_name(), colors['blue'])
        return color_data.get('fill', [0.3, 0.6, 1, 1])
    
    def _update_colors(self, *args):
        """Met à jour les couleurs selon le type et variant"""
        # Pas besoin de faire quoi que ce soit ici, les AliasProperty s'en chargent
        pass
    
    def _get_padding_value(self):
        """Padding de l'alert"""
        return [16, 12, 16, 12]
    
    padding_value = AliasProperty(_get_padding_value, None, bind=[])
    
    def _get_background_color(self):
        """Couleur de fond selon le type et variant"""
        color_data = colors.get(self._get_color_name(), colors['blue'])
        
        if self.variant == 'solid':
            base_color = color_data.get('fill', [0.3, 0.6, 1, 1])
            return [base_color[0], base_color[1], base_color[2], 0.1]
        elif self.variant == 'outline':
            return [0, 0, 0, 0]  # Transparent
        else:  # soft
            base_color = color_data.get('fill', [0.3, 0.6, 1, 1])
            return [base_color[0], base_color[1], base_color[2], 0.05]
    
    background_color = AliasProperty(_get_background_color, None, bind=['alert_type', 'variant'])
    
    def _get_border_color(self):
        """Couleur de bordure selon le type et variant"""
        if self.variant == 'outline':
            color_data = colors.get(self._get_color_name(), colors['blue'])
            return color_data.get('fill', [0.3, 0.6, 1, 1])
        else:
            return [0, 0, 0, 0]  # Pas de bordure
    
    border_color = AliasProperty(_get_border_color, None, bind=['alert_type', 'variant'])
    
    def _get_color_name(self):
        """Retourne le nom de couleur selon le type d'alert"""
        color_map = {
            'success': 'green',
            'error': 'red',
            'warning': 'orange',
            'info': 'blue'
        }
        return color_map.get(self.alert_type, 'blue')
    
    def dismiss(self):
        """Ferme l'alert en la retirant de son parent"""
        if self.parent:
            self.parent.remove_widget(self)


def create_success_alert(title="Succès", description="", closable=True):
    """Crée un alert de succès"""
    return UAlert(
        alert_type='success',
        title=title,
        description=description,
        closable=closable,
        variant='soft'
    )


def create_error_alert(title="Erreur", description="", closable=True):
    """Crée un alert d'erreur"""
    return UAlert(
        alert_type='error',
        title=title,
        description=description,
        closable=closable,
        variant='soft'
    )


def create_warning_alert(title="Attention", description="", closable=True):
    """Crée un alert d'avertissement"""
    return UAlert(
        alert_type='warning',
        title=title,
        description=description,
        closable=closable,
        variant='soft'
    )


def create_info_alert(title="Information", description="", closable=True):
    """Crée un alert d'information"""
    return UAlert(
        alert_type='info',
        title=title,
        description=description,
        closable=closable,
        variant='soft'
    )


Builder.load_string(KV)