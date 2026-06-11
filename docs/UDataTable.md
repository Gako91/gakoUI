# UDataTable

Widget de tableau de données moderne et interactif pour Kivy.

## Fonctionnalités

- **Affichage tabulaire** : Présentation claire des données en lignes et colonnes
- **Sélection de lignes** : Clic pour sélectionner une ligne
- **Tri par colonnes** : Clic sur l'en-tête pour trier (croissant/décroissant)
- **Défilement** : Scroll horizontal et vertical automatique
- **Lignes alternées** : Option pour des lignes avec couleurs alternées
- **Colonnes configurables** : Largeur, alignement et titre personnalisables
- **Événements** : Callbacks pour sélection et tri

## Utilisation de base

```python
from gakoui.widgets import UDataTable

# Configuration des colonnes
columns = [
    {'key': 'id', 'title': 'ID', 'width': 80, 'align': 'center'},
    {'key': 'name', 'title': 'Nom', 'width': 150},
    {'key': 'email', 'title': 'Email', 'width': 200},
    {'key': 'age', 'title': 'Âge', 'width': 80, 'align': 'center'}
]

# Données
data = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'age': 28},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'age': 34},
    {'id': 3, 'name': 'Claire', 'email': 'claire@example.com', 'age': 25}
]

# Création du tableau
table = UDataTable(
    columns=columns,
    data=data,
    selectable=True,
    sortable=True,
    striped=True
)
```

## Propriétés

### `columns` (ListProperty)

Configuration des colonnes du tableau.

**Format :**

```python
columns = [
    {
        'key': 'nom_champ',      # Clé dans les données (obligatoire)
        'title': 'Titre',       # Titre affiché (optionnel)
        'width': 120,           # Largeur en pixels (optionnel, défaut: 120)
        'align': 'left'         # Alignement: 'left', 'center', 'right' (optionnel, défaut: 'left')
    }
]
```

### `data` (ListProperty)

Données à afficher dans le tableau.

**Format :**

```python
data = [
    {'key1': 'valeur1', 'key2': 'valeur2'},
    {'key1': 'valeur3', 'key2': 'valeur4'}
]
```

### `selectable` (BooleanProperty)

Active/désactive la sélection de lignes (défaut: `True`).

### `sortable` (BooleanProperty)

Active/désactive le tri par colonnes (défaut: `True`).

### `striped` (BooleanProperty)

Active/désactive les lignes alternées (défaut: `True`).

### `selected_row` (NumericProperty)

Index de la ligne actuellement sélectionnée (-1 si aucune).

## Méthodes

### `add_row(row_data)`

Ajoute une nouvelle ligne au tableau.

```python
table.add_row({'id': 4, 'name': 'David', 'email': 'david@example.com', 'age': 42})
```

### `remove_row(index)`

Supprime une ligne par son index.

```python
table.remove_row(0)  # Supprime la première ligne
```

### `update_row(index, row_data)`

Met à jour une ligne existante.

```python
table.update_row(0, {'id': 1, 'name': 'Alice Martin', 'email': 'alice.martin@example.com', 'age': 29})
```

### `sort_by_column(column_key, reverse=False)`

Trie les données par une colonne spécifique.

```python
table.sort_by_column('name')          # Tri croissant par nom
table.sort_by_column('age', True)     # Tri décroissant par âge
```

### `get_selected_data()`

Retourne les données de la ligne sélectionnée.

```python
selected = table.get_selected_data()
if selected:
    print(f"Ligne sélectionnée: {selected}")
```

### `clear_selection()`

Efface la sélection actuelle.

```python
table.clear_selection()
```

## Événements

### `on_row_select(table, row_index, row_data)`

Déclenché lors de la sélection d'une ligne.

```python
def on_row_select(table, row_index, row_data):
    print(f"Ligne {row_index} sélectionnée: {row_data}")

table.bind(on_row_select=on_row_select)
```

### `on_column_sort(table, column_key)`

Déclenché lors du clic sur un en-tête de colonne.

```python
def on_column_sort(table, column_key):
    print(f"Tri demandé pour la colonne: {column_key}")
    # Implémentation du tri personnalisé
    table.sort_by_column(column_key)

table.bind(on_column_sort=on_column_sort)
```

## Exemple complet

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from gakoui.widgets import UDataTable

class DataTableApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Configuration du tableau
        columns = [
            {'key': 'id', 'title': 'ID', 'width': 60, 'align': 'center'},
            {'key': 'name', 'title': 'Nom', 'width': 140},
            {'key': 'email', 'title': 'Email', 'width': 180},
            {'key': 'age', 'title': 'Âge', 'width': 60, 'align': 'center'},
            {'key': 'city', 'title': 'Ville', 'width': 100},
            {'key': 'status', 'title': 'Statut', 'width': 80, 'align': 'center'}
        ]

        data = [
            {'id': 1, 'name': 'Alice Martin', 'email': 'alice@example.com', 'age': 28, 'city': 'Paris', 'status': 'Actif'},
            {'id': 2, 'name': 'Bob Dupont', 'email': 'bob@example.com', 'age': 34, 'city': 'Lyon', 'status': 'Inactif'},
            {'id': 3, 'name': 'Claire Bernard', 'email': 'claire@example.com', 'age': 25, 'city': 'Marseille', 'status': 'Actif'}
        ]

        table = UDataTable(
            columns=columns,
            data=data,
            selectable=True,
            sortable=True,
            striped=True,
            size_hint_y=None,
            height=300
        )

        # Événements
        table.bind(on_row_select=self.on_row_select)
        table.bind(on_column_sort=self.on_column_sort)

        layout.add_widget(table)
        return layout

    def on_row_select(self, table, row_index, row_data):
        print(f"Ligne sélectionnée: {row_data['name']}")

    def on_column_sort(self, table, column_key):
        # Tri avec alternance croissant/décroissant
        if not hasattr(table, '_sort_reverse'):
            table._sort_reverse = {}

        reverse = table._sort_reverse.get(column_key, False)
        table.sort_by_column(column_key, reverse)
        table._sort_reverse[column_key] = not reverse

DataTableApp().run()
```

## Personnalisation

### Couleurs

Les couleurs sont définies dans le KV et peuvent être personnalisées :

- **En-tête** : `#1e293b` (fond), `#334155` (cellules)
- **Lignes** : `#0f172a` (fond normal), `#1e40af` (sélectionnée)
- **Texte** : `#f1f5f9`
- **Lignes alternées** : Transparence de 30%

### Tailles

- **Hauteur en-tête** : 48dp
- **Hauteur ligne** : 44dp
- **Largeur colonne par défaut** : 120dp
- **Espacement** : 1dp
- **Padding cellules** : 12dp horizontal, 8dp vertical

## Bonnes pratiques

1. **Performance** : Limitez le nombre de lignes affichées pour de gros datasets
2. **Largeurs** : Définissez des largeurs appropriées selon le contenu
3. **Alignement** : Utilisez 'center' pour les nombres, 'left' pour le texte
4. **Tri** : Implémentez une logique de tri personnalisée si nécessaire
5. **Sélection** : Gérez les événements de sélection pour les actions utilisateur

## Limitations

- Pas de tri multi-colonnes natif
- Pas de filtrage intégré
- Pas d'édition inline des cellules
- Pas de redimensionnement dynamique des colonnes
- Performance limitée avec de très gros datasets (>1000 lignes)
