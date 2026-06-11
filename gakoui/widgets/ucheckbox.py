from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty, AliasProperty, NumericProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle, Line
from gakoui.data.colors import colors
from gakoui.behaviors import HoverBehavior

KV = """
<UCheckbox>:
    size_hint: None, None
    size: root.checkbox_size, root.checkbox_size
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
    Label:
        text: root.check_text if root.checked else ''
        font_size: root.check_font_size
        color: root.check_color
        halign: 'center'
        valign: 'middle'

<UCheckboxLabel>:
    size_hint_y: None
    height: self.texture_size[1]
    text_size: self.width, None
    color: 1, 1, 1, 1
    font_size: '14sp'

<UCheckboxContainer>:
    orientation: 'horizontal'
    spacing: 8
    size_hint: None, None
    size: self.minimum_width, self.minimum_height

<UCheckboxGroup>:
    orientation: 'vertical'
    spacing: 8
    size_hint_y: None
    height: self.minimum_height
"""


class UCheckboxLabel(Label):
    pass


class UCheckboxContainer(BoxLayout):
    pass


class UCheckboxGroup(BoxLayout):
    """Groupe de checkboxes pour gérer les sélections multiples"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checkboxes = []
    
    def add_checkbox(self, checkbox):
        """Ajoute une checkbox au groupe"""
        self.checkboxes.append(checkbox)
        checkbox.group = self
    
    def get_checked_values(self):
        """Retourne la liste des valeurs cochées"""
        return [cb.value for cb in self.checkboxes if cb.checked]
    
    def set_checked_values(self, values):
        """Coche les checkboxes correspondant aux valeurs"""
        for cb in self.checkboxes:
            cb.checked = cb.value in values
    
    def check_all(self):
        """Coche toutes les checkboxes"""
        for cb in self.checkboxes:
            cb.checked = True
    
    def uncheck_all(self):
        """Décoche toutes les checkboxes"""
        for cb in self.checkboxes:
            cb.checked = False


class UCheckbox(HoverBehavior, ButtonBehavior, BoxLayout):
    # Propriétés principales
    checked = BooleanProperty(False)
    color = StringProperty('blue')
    size_variant = StringProperty('medium')  # 'small', 'medium', 'large'
    disabled = BooleanProperty(False)
    value = StringProperty('')  # Valeur associée à la checkbox
    
    # Propriétés de style
    checkbox_size = NumericProperty(20)
    radius_value = NumericProperty(4)
    border_width = NumericProperty(2)
    check_font_size = NumericProperty(14)
    
    # Propriétés de couleur
    background_color = ListProperty([0, 0, 0, 0])
    border_color = ListProperty([0.5, 0.5, 0.5, 1])
    check_color = ListProperty([1, 1, 1, 1])
    
    # Groupe (optionnel)
    group = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(checked=self._update_colors)
        self.bind(size_variant=self._update_sizes)
        self.bind(color=self._update_colors)
        self.bind(hovered=self._update_colors, disabled=self._update_colors)
        
        self._update_sizes()
        self._update_colors()
    
    def _update_sizes(self, *args):
        """Met à jour les tailles selon le variant"""
        size_map = {
            'small': {'size': 16, 'radius': 3, 'border': 1.5, 'font': 12},
            'medium': {'size': 20, 'radius': 4, 'border': 2, 'font': 14},
            'large': {'size': 24, 'radius': 5, 'border': 2, 'font': 16}
        }
        
        sizes = size_map.get(self.size_variant, size_map['medium'])
        self.checkbox_size = sizes['size']
        self.radius_value = sizes['radius']
        self.border_width = sizes['border']
        self.check_font_size = sizes['font']
    
    def _update_colors(self, *args):
        """Met à jour les couleurs selon l'état"""
        color_data = colors.get(self.color, colors['blue'])
        
        if self.disabled:
            # État désactivé
            self.background_color = [0.2, 0.2, 0.2, 1] if self.checked else [0, 0, 0, 0]
            self.border_color = [0.3, 0.3, 0.3, 1]
            self.check_color = [0.5, 0.5, 0.5, 1]
        elif self.checked:
            # État coché
            base_color = color_data.get('fill', [0.3, 0.6, 1, 1])
            if self.hovered:
                # Plus lumineux au hover
                self.background_color = [min(1, base_color[0] * 1.1), 
                                       min(1, base_color[1] * 1.1), 
                                       min(1, base_color[2] * 1.1), 
                                       base_color[3]]
            else:
                self.background_color = base_color
            self.border_color = self.background_color
            self.check_color = color_data.get('font', [1, 1, 1, 1])
        else:
            # État non coché
            self.background_color = [0, 0, 0, 0]  # Transparent
            if self.hovered:
                hover_color = color_data.get('fill', [0.3, 0.6, 1, 1])
                self.border_color = hover_color
            else:
                self.border_color = [0.5, 0.5, 0.5, 1]  # Gris neutre
            self.check_color = [1, 1, 1, 1]
    
    def _get_check_text(self):
        """Retourne le texte de la coche"""
        return '✓' if self.checked else ''
    
    check_text = AliasProperty(_get_check_text, None, bind=['checked'])
    
    def on_release(self):
        """Bascule l'état de la checkbox"""
        if not self.disabled:
            self.checked = not self.checked
    
    def on_enter(self, *args):
        """Effet hover"""
        from kivy.core.window import Window
        if not self.disabled:
            Window.set_system_cursor('hand')
    
    def on_leave(self, *args):
        """Fin effet hover"""
        from kivy.core.window import Window
        Window.set_system_cursor('arrow')


def create_checkbox_with_label(text="", value="", **checkbox_kwargs):
    """Fonction utilitaire pour créer une checkbox avec label"""
    container = UCheckboxContainer()
    
    checkbox = UCheckbox(value=value or text, **checkbox_kwargs)
    container.add_widget(checkbox)
    
    if text:
        label = UCheckboxLabel(text=text)
        container.add_widget(label)
    
    return container, checkbox


def create_checkbox_group(items, **checkbox_kwargs):
    """Fonction utilitaire pour créer un groupe de checkboxes"""
    group = UCheckboxGroup()
    checkboxes = []
    
    for item in items:
        if isinstance(item, str):
            text = item
            value = item
        elif isinstance(item, dict):
            text = item.get('text', '')
            value = item.get('value', text)
        else:
            text = str(item)
            value = str(item)
        
        container, checkbox = create_checkbox_with_label(
            text=text, 
            value=value, 
            **checkbox_kwargs
        )
        
        group.add_widget(container)
        group.add_checkbox(checkbox)
        checkboxes.append(checkbox)
    
    return group, checkboxes


Builder.load_string(KV)