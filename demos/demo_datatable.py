"""Demo: UDataTable — sortable, selectable, striped.

Run: uv run python demos/demo_datatable.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from gakoui.widgets import UDataTable

Window.size = (760, 460)


class DataTableDemoApp(App):
    title = "GakoUI · UDataTable"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=10)

        columns = [
            {"key": "id", "title": "ID", "width": 60, "align": "center"},
            {"key": "name", "title": "Name", "width": 160},
            {"key": "email", "title": "Email", "width": 220},
            {"key": "age", "title": "Age", "width": 80, "align": "center"},
            {"key": "status", "title": "Status", "width": 100, "align": "center"},
        ]
        data = [
            {"id": 1, "name": "Alice Martin", "email": "alice@example.com",
             "age": 29, "status": "active"},
            {"id": 2, "name": "Bob Durand", "email": "bob@example.com",
             "age": 34, "status": "active"},
            {"id": 3, "name": "Carla Diaz", "email": "carla@example.com",
             "age": 41, "status": "inactive"},
            {"id": 4, "name": "Daniel Kim", "email": "dan@example.com",
             "age": 25, "status": "active"},
            {"id": 5, "name": "Émilie Petit", "email": "emilie@example.com",
             "age": 37, "status": "inactive"},
        ]

        table = UDataTable(columns=columns, data=data,
                           selectable=True, sortable=True, striped=True)
        table.bind(on_row_select=self._on_select)
        table.bind(on_column_sort=self._on_sort)
        root.add_widget(table)
        return root

    def _on_select(self, table, row_index, row_data):
        print(f"Selected row {row_index}: {row_data}")

    def _on_sort(self, table, column_key):
        print(f"Sorted by {column_key}")


if __name__ == "__main__":
    DataTableDemoApp().run()
