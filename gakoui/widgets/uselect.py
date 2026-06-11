from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty, AliasProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.graphics import Color, RoundedRectangle, Line
from gakoui.data import icon_path
from gakoui.data.colors import colors
from gakoui.behaviors import HoverBehavior

KV = """
<USelect>:
    orientation: 'horizontal'
    spacing: 8
    padding: [12, 8, 8, 8]
    size_hint_y: None
    height: root.select_height
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
        text: root.display_text
        color: root.text_color
        font_size: root.font_size
        text_size: self.width, None
        halign: 'left'
        valign: 'middle'
    
    Widget:
        size_hint_x: None
        width: 20
        canvas:
            Color:
                rgba: root.icon_color
            Rectangle:
                pos: self.center_x - 8, self.center_y - 8
                size: 16, 16
                source: root.icon_source

<USelectDropDown>:
    canvas.before:
        Color:
            rgba: root.dropdown_bg_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [8]
        Color:
            rgba: root.dropdown_border_color
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 8, 8, 8, 8, 100)
            width: 1
    size_hint_x: None
    width: root.parent_width if root.parent_width > 0 else 200
    auto_width: False

<USelectOption>:
    size_hint_y: None
    height: 40
    padding: [12, 8, 12, 8]
    canvas.before:
        Color:
            rgba: root.option_bg_color
        Rectangle:
            size: self.size
            pos: self.pos
    
    Label:
        text: root.option_text
        color: root.option_text_color
        font_size: '14sp'
        text_size: self.width, None
        halign: 'left'
        valign: 'middle'

<USelectContainer>:
    orientation: 'vertical'
    spacing: 4
    size_hint_y: None
    height: self.minimum_height

<USelectLabel>:
    size_hint_y: None
    height: self.texture_size[1] if self.text else 0
    text_size: self.width, None
    color: 1, 1, 1, 1
    font_size: '14sp'
    bold: True

<USelectError>:
    size_hint_y: None
    height: self.texture_size[1] if self.text else 0
    text_size: self.width, None
    color: 0.9, 0.3, 0.3, 1
    font_size: '12sp'
"""


class USelectLabel(Label):
    pass


class USelectError(Label):
    pass


class USelectContainer(BoxLayout):
    pass


class USelectOption(HoverBehavior, ButtonBehavior, BoxLayout):
    option_text = StringProperty('')
    option_value = ObjectProperty(None)
    select_widget = ObjectProperty(None)
    option_bg_color = ListProperty([0, 0, 0, 0])
    option_text_color = ListProperty([0.9, 0.9, 0.9, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(hovered=self._update_colors)
        self._update_colors()
    
    def _update_colors(self, *args):
        """Met à jour les couleurs selon l'état hover"""
        if self.hovered:
            self.option_bg_color = [0.2, 0.2, 0.2, 1]
            self.option_text_color = [1, 1, 1, 1]
        else:
            self.option_bg_color = [0, 0, 0, 0]
            self.option_text_color = [0.9, 0.9, 0.9, 1]
    
    def on_release(self):
        if self.select_widget:
            self.select_widget.select_option(self.option_value, self.option_text)


class USelectDropDown(DropDown):
    dropdown_bg_color = ListProperty([0.1, 0.1, 0.1, 1])
    dropdown_border_color = ListProperty([0.3, 0.3, 0.3, 1])
    parent_width = NumericProperty(0)


class USelect(HoverBehavior, ButtonBehavior, BoxLayout):
    # Propriétés principales
    selected_value = ObjectProperty(None, allownone=True)
    placeholder = StringProperty('Sélectionner une option')
    options = ListProperty([])
    color = StringProperty('blue')
    size_variant = StringProperty('medium')  # 'small', 'medium', 'large'
    disabled = BooleanProperty(False)
    searchable = BooleanProperty(False)  # Pour une future implémentation
    multiple = BooleanProperty(False)  # Pour une future implémentation
    
    # Propriétés de style
    select_height = NumericProperty(40)
    radius_value = NumericProperty(6)
    border_width = NumericProperty(1)
    font_size = NumericProperty(14)
    
    # Propriétés de couleur
    background_color = ListProperty([0, 0, 0, 0])
    border_color = ListProperty([0.5, 0.5, 0.5, 1])
    text_color = ListProperty([1, 1, 1, 1])
    icon_color = ListProperty([0.7, 0.7, 0.7, 1])
    
    # Validation
    required = BooleanProperty(False)
    error_message = StringProperty('')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size_variant=self._update_sizes)
        self.bind(color=self._update_colors, hovered=self._update_colors)
        self.bind(disabled=self._update_colors, selected_value=self._update_colors)
        self.bind(options=self._update_dropdown)
        
        # Créer le dropdown
        self.dropdown = USelectDropDown()
        self.dropdown.bind(on_select=self._on_dropdown_select)
        
        self._update_sizes()
        self._update_colors()
        self._update_dropdown()
    
    def _update_sizes(self, *args):
        """Met à jour les tailles selon le variant"""
        size_map = {
            'small': {'height': 32, 'font': 12, 'radius': 4},
            'medium': {'height': 40, 'font': 14, 'radius': 6},
            'large': {'height': 48, 'font': 16, 'radius': 8}
        }
        
        sizes = size_map.get(self.size_variant, size_map['medium'])
        self.select_height = sizes['height']
        self.font_size = sizes['font']
        self.radius_value = sizes['radius']
    
    def _update_colors(self, *args):
        """Met à jour les couleurs selon l'état"""
        color_data = colors.get(self.color, colors['blue'])
        
        if self.disabled:
            # État désactivé
            self.background_color = [0.1, 0.1, 0.1, 1]
            self.border_color = [0.3, 0.3, 0.3, 1]
            self.text_color = [0.5, 0.5, 0.5, 1]
            self.icon_color = [0.4, 0.4, 0.4, 1]
        elif self.hovered:
            # État hover
            self.background_color = [0.05, 0.05, 0.05, 1]
            hover_color = color_data.get('fill', [0.3, 0.6, 1, 1])
            self.border_color = hover_color
            self.text_color = [1, 1, 1, 1]
            self.icon_color = hover_color
        else:
            # État normal
            self.background_color = [0, 0, 0, 0]
            self.border_color = [0.5, 0.5, 0.5, 1]
            if self.selected_value is not None:
                self.text_color = [1, 1, 1, 1]
            else:
                self.text_color = [0.7, 0.7, 0.7, 1]  # Placeholder plus sombre
            self.icon_color = [0.7, 0.7, 0.7, 1]
    
    def _update_dropdown(self, *args):
        """Met à jour les options du dropdown"""
        self.dropdown.clear_widgets()
        
        for option in self.options:
            if isinstance(option, dict):
                text = option.get('text', str(option.get('value', '')))
                value = option.get('value', text)
            elif isinstance(option, (list, tuple)) and len(option) >= 2:
                text, value = option[0], option[1]
            else:
                text = str(option)
                value = option
            
            option_widget = USelectOption(
                option_text=text,
                option_value=value,
                select_widget=self
            )
            self.dropdown.add_widget(option_widget)
    
    def _on_dropdown_select(self, dropdown, option_widget):
        """Callback quand une option est sélectionnée"""
        # Cette méthode est appelée par le dropdown de Kivy, pas notre logique
        pass
    
    def select_option(self, value, text):
        """Sélectionne une option"""
        self.selected_value = value
        self.dropdown.dismiss()
        self.validate()
    
    def _get_display_text(self):
        """Retourne le texte à afficher"""
        if self.selected_value is not None:
            # Trouver le texte correspondant à la valeur
            for option in self.options:
                if isinstance(option, dict):
                    if option.get('value') == self.selected_value:
                        return option.get('text', str(self.selected_value))
                elif isinstance(option, (list, tuple)) and len(option) >= 2:
                    if option[1] == self.selected_value:
                        return option[0]
                else:
                    if option == self.selected_value:
                        return str(option)
            return str(self.selected_value)
        return self.placeholder
    
    display_text = AliasProperty(_get_display_text, None, bind=['selected_value', 'placeholder', 'options'])
    
    def _get_icon_source(self):
        """Retourne la source de l'icône"""
        return icon_path('material-symbols--keyboard-arrow-down.png')
    
    icon_source = AliasProperty(_get_icon_source, None, bind=[])
    
    def on_release(self):
        """Ouvre le dropdown"""
        if not self.disabled:
            self.dropdown.parent_width = self.width
            self.dropdown.open(self)
    
    def validate(self):
        """Valide la sélection"""
        if self.required and self.selected_value is None:
            self.error_message = 'Ce champ est requis'
            return False
        else:
            self.error_message = ''
            return True
    
    def clear_selection(self):
        """Efface la sélection"""
        self.selected_value = None
        self.error_message = ''
    
    def set_options(self, options):
        """Définit les options du select"""
        self.options = options
    
    def get_selected_text(self):
        """Retourne le texte de l'option sélectionnée"""
        return self.display_text if self.selected_value is not None else None
    
    def on_enter(self, *args):
        """Effet hover"""
        from kivy.core.window import Window
        if not self.disabled:
            Window.set_system_cursor('hand')
    
    def on_leave(self, *args):
        """Fin effet hover"""
        from kivy.core.window import Window
        Window.set_system_cursor('arrow')


def create_select_with_label(text="", options=None, **select_kwargs):
    """Fonction utilitaire pour créer un select avec label"""
    container = USelectContainer()
    
    if text:
        label = USelectLabel(text=text)
        container.add_widget(label)
    
    select_widget = USelect(options=options or [], **select_kwargs)
    container.add_widget(select_widget)
    
    # Ajouter le message d'erreur
    error_label = USelectError()
    select_widget.bind(error_message=error_label.setter('text'))
    container.add_widget(error_label)
    
    return container, select_widget


def create_country_select(**kwargs):
    """Fonction utilitaire pour créer un select de pays"""
    countries = [
        {'text': 'France', 'value': 'FR'},
        {'text': 'Allemagne', 'value': 'DE'},
        {'text': 'Espagne', 'value': 'ES'},
        {'text': 'Italie', 'value': 'IT'},
        {'text': 'Royaume-Uni', 'value': 'GB'},
        {'text': 'États-Unis', 'value': 'US'},
        {'text': 'Canada', 'value': 'CA'},
        {'text': 'Japon', 'value': 'JP'},
        {'text': 'Australie', 'value': 'AU'},
        {'text': 'Brésil', 'value': 'BR'}
    ]
    
    return USelect(
        options=countries,
        placeholder='Sélectionner un pays',
        **kwargs
    )


Builder.load_string(KV)