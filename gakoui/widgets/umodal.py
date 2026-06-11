from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle
from gakoui.data.colors import colors

KV = """
<UModal>:
    size_hint: None, None
    size: root.modal_width, root.modal_height
    auto_dismiss: root.auto_dismiss
    background_color: 0, 0, 0, 0
    
<UModalContent>:
    orientation: 'vertical'
    spacing: 0
    canvas.before:
        Color:
            rgba: root.background_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [root.radius_value]

<UModalHeader>:
    size_hint_y: None
    height: self.minimum_height if self.children else 0
    orientation: 'horizontal'
    padding: [20, 16, 20, 16]
    spacing: 10

<UModalTitle>:
    size_hint_y: None
    height: self.texture_size[1]
    text_size: self.width, None
    font_size: '20sp'
    bold: True
    color: 1, 1, 1, 1

<UModalBody>:
    orientation: 'vertical'
    padding: [20, 0, 20, 20]

<UModalFooter>:
    size_hint_y: None
    height: self.minimum_height if self.children else 0
    orientation: 'horizontal'
    padding: [20, 16, 20, 20]
    spacing: 10
"""


class UModalTitle(Label):
    pass


class UModalCloseButton(BoxLayout):
    def __init__(self, modal=None, **kwargs):
        super().__init__(**kwargs)
        self.modal = modal
        # Import local pour éviter les imports circulaires
        from gakoui.widgets.ubutton import UButton
        self.close_btn = UButton(
            size_hint_x=None,
            width=32,
            color='stone',
            variant='ghost',
            text='×',
            font_size='24sp'
        )
        self.close_btn.bind(on_release=self._close_modal)
        self.add_widget(self.close_btn)
    
    def _close_modal(self, *args):
        if self.modal:
            self.modal.dismiss()


class UModalHeader(BoxLayout):
    def __init__(self, modal=None, **kwargs):
        super().__init__(**kwargs)
        self.modal = modal


class UModalBody(BoxLayout):
    pass


class UModalFooter(BoxLayout):
    pass


class UModalContent(BoxLayout):
    color = StringProperty('stone')
    radius = NumericProperty(12)
    
    def _get_radius_value(self):
        return self.radius
    
    radius_value = AliasProperty(_get_radius_value, None, bind=['radius'])
    
    def _get_background_color(self):
        return [0.1, 0.1, 0.1, 1]  # Dark background
    
    background_color = AliasProperty(_get_background_color, None, bind=['color'])


class UModal(ModalView):
    color = StringProperty('stone')
    modal_width = NumericProperty(400)
    modal_height = NumericProperty(300)
    title = StringProperty('')
    closable = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        # Configurer l'overlay avant l'initialisation
        if 'overlay_color' not in kwargs:
            kwargs['overlay_color'] = [0, 0, 0, 0.5]
        
        super().__init__(**kwargs)
        self.content_widget = UModalContent()
        self.add_widget(self.content_widget)
        
        # Header
        self.header = UModalHeader(modal=self)
        if self.title:
            self.title_label = UModalTitle(text=self.title)
            self.header.add_widget(self.title_label)
        
        if self.closable:
            self.close_button = UModalCloseButton(modal=self)
            self.header.add_widget(self.close_button)
        
        self.content_widget.add_widget(self.header)
        
        # Body
        self.body = UModalBody()
        self.content_widget.add_widget(self.body)
        
        # Footer
        self.footer = UModalFooter()
        self.content_widget.add_widget(self.footer)
        
        self.bind(title=self._update_title)
    
    def _update_title(self, *args):
        if hasattr(self, 'title_label'):
            self.title_label.text = self.title
    
    def add_content(self, widget):
        """Ajouter du contenu au corps du modal"""
        self.body.add_widget(widget)
    
    def add_footer_button(self, button):
        """Ajouter un bouton au pied du modal"""
        self.footer.add_widget(button)


Builder.load_string(KV)