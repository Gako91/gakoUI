from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import (
    ListProperty, StringProperty, NumericProperty, 
    BooleanProperty, ObjectProperty, DictProperty
)
from kivy.metrics import dp
from kivy.clock import Clock


KV = """
#:import rgba kivy.utils.rgba

<UDataTable>:
    orientation: 'vertical'
    spacing: dp(1)
    
    # Header
    BoxLayout:
        id: header_container
        size_hint_y: None
        height: dp(48)
        canvas.before:
            Color:
                rgba: rgba('#1e293b')
            Rectangle:
                size: self.size
                pos: self.pos

    # Content with scroll
    ScrollView:
        id: scroll_view
        do_scroll_x: True
        do_scroll_y: True
        bar_width: dp(8)
        scroll_type: ['bars']
        
        GridLayout:
            id: content_grid
            cols: 1
            size_hint_y: None
            height: self.minimum_height
            spacing: dp(1)

<DataTableHeader>:
    size_hint_y: None
    height: dp(48)
    spacing: dp(1)

<DataTableRow>:
    size_hint_y: None
    height: dp(44)
    spacing: dp(1)
    canvas.before:
        Color:
            rgba: rgba('#0f172a') if not root.selected else rgba('#1e40af')
        Rectangle:
            size: self.size
            pos: self.pos

<DataTableCell>:
    text_size: self.size
    halign: root.align
    valign: 'center'
    color: rgba('#f1f5f9')
    font_size: dp(14)
    padding: [dp(12), dp(8)]
    canvas.before:
        Color:
            rgba: rgba('#334155') if root.is_header else rgba('#1e293b')
        Rectangle:
            size: self.size
            pos: self.pos
"""


class DataTableCell(Label):
    """Cellule individuelle du tableau"""
    align = StringProperty('left')
    is_header = BooleanProperty(False)
    column_width = NumericProperty(dp(120))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = None
        self.width = self.column_width
        self.bind(column_width=self._update_width)
    
    def _update_width(self, *args):
        self.width = self.column_width


class DataTableRow(BoxLayout):
    """Ligne du tableau"""
    selected = BooleanProperty(False)
    row_data = ListProperty([])
    table = ObjectProperty(None)
    row_index = NumericProperty(-1)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_touch_down=self._on_touch_down)
    
    def _on_touch_down(self, instance, touch):
        if self.collide_point(*touch.pos) and self.table:
            if self.table.selectable:
                self.table._select_row(self.row_index)
            return True
        return False


class DataTableHeader(BoxLayout):
    """En-tête du tableau"""
    pass


class UDataTable(BoxLayout):
    """
    Widget DataTable moderne pour Kivy
    
    Propriétés:
    - columns: Liste des colonnes [{'key': 'name', 'title': 'Nom', 'width': 150}]
    - data: Liste des données [{'name': 'John', 'age': 30}]
    - selectable: Permet la sélection de lignes
    - sortable: Permet le tri des colonnes
    - striped: Lignes alternées
    """
    
    columns = ListProperty([])
    data = ListProperty([])
    selectable = BooleanProperty(True)
    sortable = BooleanProperty(True)
    striped = BooleanProperty(True)
    selected_row = NumericProperty(-1)
    
    # Événements
    __events__ = ('on_row_select', 'on_column_sort')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._build_table, 0)
        self.bind(columns=self._rebuild_table)
        self.bind(data=self._rebuild_table)
    
    def _build_table(self, *args):
        """Construit le tableau"""
        self._build_header()
        self._build_content()
    
    def _rebuild_table(self, *args):
        """Reconstruit le tableau quand les données changent"""
        Clock.schedule_once(self._build_table, 0)
    
    def _build_header(self):
        """Construit l'en-tête"""
        header_container = self.ids.header_container
        header_container.clear_widgets()
        
        if not self.columns:
            return
        
        header = DataTableHeader()
        
        for col in self.columns:
            cell = DataTableCell(
                text=col.get('title', col.get('key', '')),
                is_header=True,
                align=col.get('align', 'left'),
                column_width=dp(col.get('width', 120)),
                bold=True
            )
            
            # Ajouter indicateur de tri si activé
            if self.sortable:
                cell.bind(on_touch_down=lambda x, touch, key=col['key']: 
                         self._on_header_click(key, touch))
            
            header.add_widget(cell)
        
        header_container.add_widget(header)
    
    def _build_content(self):
        """Construit le contenu du tableau"""
        content_grid = self.ids.content_grid
        content_grid.clear_widgets()
        
        if not self.data or not self.columns:
            return
        
        for i, row_data in enumerate(self.data):
            row = DataTableRow(
                row_data=row_data,
                table=self,
                row_index=i
            )
            
            # Couleur alternée si striped
            if self.striped and i % 2 == 1:
                row.canvas.before.clear()
                with row.canvas.before:
                    from kivy.graphics import Color, Rectangle
                    Color(rgba=(0.1, 0.1, 0.1, 0.3))
                    Rectangle(size=row.size, pos=row.pos)
            
            for col in self.columns:
                key = col['key']
                value = str(row_data.get(key, ''))
                
                cell = DataTableCell(
                    text=value,
                    align=col.get('align', 'left'),
                    column_width=dp(col.get('width', 120))
                )
                
                row.add_widget(cell)
            
            content_grid.add_widget(row)
    
    def _on_header_click(self, column_key, touch):
        """Gère le clic sur l'en-tête pour le tri"""
        if self.sortable:
            self.dispatch('on_column_sort', column_key)
    
    def _select_row(self, row_index):
        """Sélectionne une ligne"""
        if not self.selectable:
            return
        
        # Désélectionner la ligne précédente
        if self.selected_row >= 0:
            old_row = self.ids.content_grid.children[-(self.selected_row + 1)]
            old_row.selected = False
        
        # Sélectionner la nouvelle ligne
        self.selected_row = row_index
        new_row = self.ids.content_grid.children[-(row_index + 1)]
        new_row.selected = True
        
        self.dispatch('on_row_select', row_index, self.data[row_index])
    
    def sort_by_column(self, column_key, reverse=False):
        """Trie les données par colonne"""
        if not self.data:
            return
        
        try:
            self.data = sorted(
                self.data, 
                key=lambda x: x.get(column_key, ''),
                reverse=reverse
            )
        except (TypeError, KeyError):
            pass  # Ignore les erreurs de tri
    
    def add_row(self, row_data):
        """Ajoute une ligne"""
        data_copy = list(self.data)
        data_copy.append(row_data)
        self.data = data_copy
    
    def remove_row(self, index):
        """Supprime une ligne"""
        if 0 <= index < len(self.data):
            data_copy = list(self.data)
            data_copy.pop(index)
            self.data = data_copy
    
    def update_row(self, index, row_data):
        """Met à jour une ligne"""
        if 0 <= index < len(self.data):
            data_copy = list(self.data)
            data_copy[index] = row_data
            self.data = data_copy
    
    def get_selected_data(self):
        """Retourne les données de la ligne sélectionnée"""
        if 0 <= self.selected_row < len(self.data):
            return self.data[self.selected_row]
        return None
    
    def clear_selection(self):
        """Efface la sélection"""
        if self.selected_row >= 0:
            row = self.ids.content_grid.children[-(self.selected_row + 1)]
            row.selected = False
            self.selected_row = -1
    
    # Événements
    def on_row_select(self, row_index, row_data):
        """Événement déclenché lors de la sélection d'une ligne"""
        pass
    
    def on_column_sort(self, column_key):
        """Événement déclenché lors du clic sur un en-tête"""
        pass


Builder.load_string(KV)