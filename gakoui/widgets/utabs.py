from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty, AliasProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from gakoui.data import icon_path
from gakoui.data.colors import colors
from gakoui.behaviors import HoverBehavior

KV = """
<UTabs>:
    orientation: 'vertical'
    spacing: 0
    size_hint_y: None
    height: self.minimum_height

<UTabsHeader>:
    orientation: 'horizontal'
    spacing: 0
    size_hint_y: None
    height: root.tab_height
    canvas.before:
        Color:
            rgba: root.header_bg_color
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: root.border_color
        Line:
            points: self.x, self.y, self.x + self.width, self.y
            width: 1

<UTab>:
    size_hint_x: None
    width: self.minimum_width
    padding: [16, 8, 16, 8]
    spacing: 8
    canvas.before:
        Color:
            rgba: root.tab_bg_color
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: root.tab_border_color
        Line:
            points: self.x, self.y + self.height, self.x + self.width, self.y + self.height
            width: root.border_width
    
    Widget:
        size_hint_x: None
        width: 20 if root.icon else 0
        canvas:
            Color:
                rgba: root.icon_color if root.icon else [0,0,0,0]
            Rectangle:
                pos: self.center_x - 8, self.center_y - 8
                size: 16, 16
                source: root.icon_source if root.icon else ''
    
    Label:
        text: root.text
        color: root.text_color
        font_size: root.font_size
        size_hint_x: None
        width: self.texture_size[0]
        halign: 'center'
        valign: 'middle'
    
    Widget:
        size_hint_x: None
        width: 20 if root.badge_text else 0
        canvas:
            Color:
                rgba: root.badge_bg_color if root.badge_text else [0,0,0,0]
            Ellipse:
                size: 16, 16
                pos: self.center_x - 8, self.center_y - 8
        Label:
            text: root.badge_text
            color: root.badge_text_color
            font_size: '10sp'
            size_hint: None, None
            size: 16, 16
            halign: 'center'
            valign: 'middle'

<UTabContent>:
    orientation: 'vertical'
    padding: root.content_padding
    canvas.before:
        Color:
            rgba: root.content_bg_color
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: root.content_border_color
        Line:
            rectangle: (self.x, self.y, self.width, self.height)
            width: 1

<UTabPanel>:
    orientation: 'vertical'
"""


class UTabPanel(BoxLayout):
    """Panneau de contenu d'un tab"""
    pass


class UTabContent(BoxLayout):
    """Conteneur pour le contenu des tabs"""
    content_padding = ListProperty([16, 16, 16, 16])
    content_bg_color = ListProperty([0.05, 0.05, 0.05, 1])
    content_border_color = ListProperty([0.3, 0.3, 0.3, 1])


class UTab(HoverBehavior, ButtonBehavior, BoxLayout):
    """Un tab individuel dans la barre de tabs"""
    text = StringProperty('')
    icon = StringProperty('')
    badge_text = StringProperty('')
    active = BooleanProperty(False)
    disabled = BooleanProperty(False)
    tab_id = StringProperty('')
    tabs_widget = ObjectProperty(None)
    
    # Propriétés de style
    font_size = NumericProperty(14)
    border_width = NumericProperty(2)
    
    # Propriétés de couleur
    tab_bg_color = ListProperty([0, 0, 0, 0])
    tab_border_color = ListProperty([0, 0, 0, 0])
    text_color = ListProperty([0.7, 0.7, 0.7, 1])
    icon_color = ListProperty([0.7, 0.7, 0.7, 1])
    badge_bg_color = ListProperty([1, 0, 0, 1])
    badge_text_color = ListProperty([1, 1, 1, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(active=self._update_colors)
        self.bind(hovered=self._update_colors, disabled=self._update_colors)
        self._update_colors()
    
    def _update_colors(self, *args):
        """Met à jour les couleurs selon l'état"""
        if self.tabs_widget:
            color_data = colors.get(self.tabs_widget.color, colors['blue'])
        else:
            color_data = colors.get('blue', colors['blue'])
        
        if self.disabled:
            # État désactivé
            self.tab_bg_color = [0, 0, 0, 0]
            self.tab_border_color = [0, 0, 0, 0]
            self.text_color = [0.4, 0.4, 0.4, 1]
            self.icon_color = [0.4, 0.4, 0.4, 1]
        elif self.active:
            # Tab actif
            self.tab_bg_color = [0.1, 0.1, 0.1, 1]
            active_color = color_data.get('fill', [0.3, 0.6, 1, 1])
            self.tab_border_color = active_color
            self.text_color = [1, 1, 1, 1]
            self.icon_color = active_color
        elif self.hovered:
            # État hover
            self.tab_bg_color = [0.05, 0.05, 0.05, 1]
            self.tab_border_color = [0, 0, 0, 0]
            self.text_color = [0.9, 0.9, 0.9, 1]
            self.icon_color = [0.9, 0.9, 0.9, 1]
        else:
            # État normal
            self.tab_bg_color = [0, 0, 0, 0]
            self.tab_border_color = [0, 0, 0, 0]
            self.text_color = [0.7, 0.7, 0.7, 1]
            self.icon_color = [0.7, 0.7, 0.7, 1]
    
    def _get_icon_source(self):
        """Retourne la source de l'icône"""
        return icon_path(self.icon)
    
    icon_source = AliasProperty(_get_icon_source, None, bind=['icon'])
    
    def on_release(self):
        """Active ce tab"""
        if not self.disabled and self.tabs_widget:
            self.tabs_widget.set_active_tab(self.tab_id)
    
    def on_enter(self, *args):
        """Effet hover"""
        from kivy.core.window import Window
        if not self.disabled:
            Window.set_system_cursor('hand')
    
    def on_leave(self, *args):
        """Fin effet hover"""
        from kivy.core.window import Window
        Window.set_system_cursor('arrow')


class UTabsHeader(BoxLayout):
    """Barre de navigation des tabs"""
    tab_height = NumericProperty(44)
    header_bg_color = ListProperty([0.02, 0.02, 0.02, 1])
    border_color = ListProperty([0.3, 0.3, 0.3, 1])


class UTabs(BoxLayout):
    """Widget principal des tabs"""
    color = StringProperty('blue')
    active_tab = StringProperty('')
    variant = StringProperty('line')  # 'line', 'pill', 'card'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Créer les composants
        self.header = UTabsHeader()
        self.content = UTabContent()
        
        self.add_widget(self.header)
        self.add_widget(self.content)
        
        # Stockage des tabs et panels
        self.tabs = {}
        self.panels = {}
        
        self.bind(color=self._update_tab_colors)
    
    def add_tab(self, tab_id, text, content_widget=None, icon='', badge_text='', disabled=False):
        """Ajoute un nouveau tab"""
        # Créer le tab
        tab = UTab(
            text=text,
            icon=icon,
            badge_text=badge_text,
            tab_id=tab_id,
            tabs_widget=self,
            disabled=disabled
        )
        
        # Créer le panel de contenu
        panel = UTabPanel()
        if content_widget:
            panel.add_widget(content_widget)
        
        # Stocker et ajouter
        self.tabs[tab_id] = tab
        self.panels[tab_id] = panel
        
        self.header.add_widget(tab)
        
        # Si c'est le premier tab, l'activer
        if not self.active_tab:
            self.set_active_tab(tab_id)
        
        return tab, panel
    
    def remove_tab(self, tab_id):
        """Supprime un tab"""
        if tab_id in self.tabs:
            # Retirer de l'interface
            self.header.remove_widget(self.tabs[tab_id])
            if self.panels[tab_id].parent:
                self.content.remove_widget(self.panels[tab_id])
            
            # Supprimer des dictionnaires
            del self.tabs[tab_id]
            del self.panels[tab_id]
            
            # Si c'était le tab actif, activer le premier disponible
            if self.active_tab == tab_id:
                if self.tabs:
                    first_tab_id = list(self.tabs.keys())[0]
                    self.set_active_tab(first_tab_id)
                else:
                    self.active_tab = ''
    
    def set_active_tab(self, tab_id):
        """Active un tab spécifique"""
        if tab_id not in self.tabs:
            return
        
        # Désactiver tous les tabs
        for tid, tab in self.tabs.items():
            tab.active = (tid == tab_id)
        
        # Changer le contenu
        self.content.clear_widgets()
        if tab_id in self.panels:
            self.content.add_widget(self.panels[tab_id])
        
        self.active_tab = tab_id
    
    def get_active_tab(self):
        """Retourne l'ID du tab actif"""
        return self.active_tab
    
    def get_tab_content(self, tab_id):
        """Retourne le panel de contenu d'un tab"""
        return self.panels.get(tab_id)
    
    def set_tab_badge(self, tab_id, badge_text):
        """Définit le badge d'un tab"""
        if tab_id in self.tabs:
            self.tabs[tab_id].badge_text = badge_text
    
    def set_tab_disabled(self, tab_id, disabled):
        """Active/désactive un tab"""
        if tab_id in self.tabs:
            self.tabs[tab_id].disabled = disabled
    
    def _update_tab_colors(self, *args):
        """Met à jour les couleurs de tous les tabs"""
        for tab in self.tabs.values():
            tab._update_colors()


def create_simple_tabs(tabs_data, **kwargs):
    """Fonction utilitaire pour créer des tabs simples"""
    tabs_widget = UTabs(**kwargs)
    
    for tab_data in tabs_data:
        if isinstance(tab_data, dict):
            tab_id = tab_data.get('id', tab_data.get('text', '').lower().replace(' ', '_'))
            text = tab_data.get('text', '')
            content = tab_data.get('content')
            icon = tab_data.get('icon', '')
            badge = tab_data.get('badge', '')
            disabled = tab_data.get('disabled', False)
        else:
            # Format simple: juste le texte
            tab_id = str(tab_data).lower().replace(' ', '_')
            text = str(tab_data)
            content = None
            icon = ''
            badge = ''
            disabled = False
        
        # Créer le contenu si c'est du texte
        if isinstance(content, str):
            content_widget = Label(
                text=content,
                color=(1, 1, 1, 1),
                text_size=(None, None),
                halign='left',
                valign='top'
            )
        else:
            content_widget = content
        
        tabs_widget.add_tab(tab_id, text, content_widget, icon, badge, disabled)
    
    return tabs_widget


Builder.load_string(KV)