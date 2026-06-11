from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
import gakoui.widgets
from gakoui.widgets import UDropDown, UCard, UCardHeader, UCardTitle, UCardDescription, UCardContent, UCardFooter, UModal, UModalBody, UToggle, create_toggle_with_label, UBadge, UBadgeDot, UBadgeNumber, create_status_badge, create_notification_badge, UAlert, create_success_alert, create_error_alert, create_warning_alert, create_info_alert, UCheckbox, UCheckboxGroup, create_checkbox_with_label, create_checkbox_group, USlider, create_slider_with_label, create_range_slider, USelect, create_select_with_label, create_country_select, UTabs, UTabPanel, create_simple_tabs

KV = """
ScrollView:
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        size_hint_y: None
        height: self.minimum_height
        
        # Exemples de UCard
        BoxLayout:
            size_hint_y: None
            height: 200
            spacing: 20
            
            UCard:
                variant: 'elevated'
                color: 'blue'
                UCardHeader:
                    UCardTitle:
                        text: 'Card Elevated'
                    UCardDescription:
                        text: 'Une carte avec effet d\\'élévation'
                UCardContent:
                    Label:
                        text: 'Contenu de la carte elevated'
                        color: 1,1,1,1
                UCardFooter:
                    UButton:
                        color: 'blue'
                        text: 'Action'
                        size_hint_x: None
                        width: 100
                        
            UCard:
                variant: 'outlined'
                color: 'green'
                UCardHeader:
                    UCardTitle:
                        text: 'Card Outlined'
                    UCardDescription:
                        text: 'Une carte avec bordure'
                UCardContent:
                    Label:
                        text: 'Contenu de la carte outlined'
                        color: 1,1,1,1
                UCardFooter:
                    UButton:
                        color: 'green'
                        variant: 'outline'
                        text: 'Voir plus'
                        size_hint_x: None
                        width: 120
                        
            UCard:
                variant: 'filled'
                color: 'purple'
                UCardHeader:
                    UCardTitle:
                        text: 'Card Filled'
                    UCardDescription:
                        text: 'Une carte avec fond coloré'
                UCardContent:
                    Label:
                        text: 'Contenu de la carte filled'
                        color: 1,1,1,1
                UCardFooter:
                    UButton:
                        color: 'purple'
                        text: 'Confirmer'
                        size_hint_x: None
                        width: 120
        
        # Exemple de boutons pour ouvrir des modals
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 20
            
            UButton:
                color: 'blue'
                text: 'Ouvrir Modal Simple'
                on_release: app.open_simple_modal()
                
            UButton:
                color: 'green'
                text: 'Modal avec Formulaire'
                on_release: app.open_form_modal()
                
            UButton:
                color: 'red'
                text: 'Modal de Confirmation'
                on_release: app.open_confirm_modal()
        
        # Exemples de UToggle
        BoxLayout:
            size_hint_y: None
            height: 160
            spacing: 20
            orientation: 'vertical'
            
            Label:
                text: 'Exemples de Toggle'
                size_hint_y: None
                height: 30
                color: 1, 1, 1, 1
                font_size: '16sp'
                bold: True
            
            BoxLayout:
                size_hint_y: None
                height: 30
                spacing: 30
                
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 10
                    size_hint: None, None
                    size: self.minimum_width, self.minimum_height
                    
                    UToggle:
                        id: toggle_small
                        size_variant: 'small'
                        color: 'blue'
                        active: False
                        on_active: app.on_toggle_change('Small Toggle', self.active)
                    Label:
                        text: 'Small Toggle'
                        size_hint_y: None
                        height: 20
                        color: 1, 1, 1, 1
                        font_size: '12sp'
                
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 10
                    size_hint: None, None
                    size: self.minimum_width, self.minimum_height
                    
                    UToggle:
                        id: toggle_medium
                        size_variant: 'medium'
                        color: 'green'
                        active: True
                        on_active: app.on_toggle_change('Medium Toggle', self.active)
                    Label:
                        text: 'Medium Toggle (Activé)'
                        size_hint_y: None
                        height: 24
                        color: 1, 1, 1, 1
                        font_size: '14sp'
                
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 10
                    size_hint: None, None
                    size: self.minimum_width, self.minimum_height
                    
                    UToggle:
                        id: toggle_large
                        size_variant: 'large'
                        color: 'purple'
                        active: False
                        on_active: app.on_toggle_change('Large Toggle', self.active)
                    Label:
                        text: 'Large Toggle'
                        size_hint_y: None
                        height: 28
                        color: 1, 1, 1, 1
                        font_size: '16sp'
        
        # Toggles avec différentes couleurs
        BoxLayout:
            size_hint_y: None
            height: 160
            spacing: 20
            orientation: 'vertical'
            
            Label:
                text: 'Toggles avec couleurs'
                size_hint_y: None
                height: 30
                color: 1, 1, 1, 1
                font_size: '16sp'
                bold: True
            
            BoxLayout:
                size_hint_y: None
                height: 30
                spacing: 20
                
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 10
                    size_hint: None, None
                    size: self.minimum_width, self.minimum_height
                    
                    UToggle:
                        color: 'red'
                        active: True
                        on_active: app.on_toggle_change('Rouge', self.active)
                    Label:
                        text: 'Rouge'
                        size_hint_y: None
                        height: 24
                        color: 1, 1, 1, 1
                
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 10
                    size_hint: None, None
                    size: self.minimum_width, self.minimum_height
                    
                    UToggle:
                        color: 'orange'
                        active: False
                        on_active: app.on_toggle_change('Orange', self.active)
                    Label:
                        text: 'Orange'
                        size_hint_y: None
                        height: 24
                        color: 1, 1, 1, 1
                
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 10
                    size_hint: None, None
                    size: self.minimum_width, self.minimum_height
                    
                    UToggle:
                        color: 'indigo'
                        active: True
                        disabled: True
                        on_active: app.on_toggle_change('Indigo (Désactivé)', self.active)
                    Label:
                        text: 'Indigo (Désactivé)'
                        size_hint_y: None
                        height: 24
                        color: 0.6, 0.6, 0.6, 1
        
        # Exemples de UBadge
        BoxLayout:
            size_hint_y: None
            height: 420
            spacing: 20
            orientation: 'vertical'
            
            Label:
                text: 'Exemples de Badge'
                size_hint_y: None
                height: 30
                color: 1, 1, 1, 1
                font_size: '16sp'
                bold: True
            
            # Badges de statut
            BoxLayout:
                size_hint_y: None
                height: 130
                spacing: 10
                
                Label:
                    text: 'Statuts:'
                    size_hint_x: None
                    width: 60
                    color: 1, 1, 1, 1
                    font_size: '12sp'
                
                UBadge:
                    text: 'Succès'
                    color_theme: 'green'
                    variant: 'solid'
                    size_variant: 'small'
                
                UBadge:
                    text: 'Erreur'
                    color_theme: 'red'
                    variant: 'solid'
                    size_variant: 'small'
                
                UBadge:
                    text: 'Attention'
                    color_theme: 'orange'
                    variant: 'outline'
                    size_variant: 'small'
                
                UBadge:
                    text: 'Info'
                    color_theme: 'blue'
                    variant: 'soft'
                    size_variant: 'small'
            
            # Badges de notification
            BoxLayout:
                size_hint_y: None
                height: 130
                spacing: 10
                
                Label:
                    text: 'Notifications:'
                    size_hint_x: None
                    width: 80
                    color: 1, 1, 1, 1
                    font_size: '12sp'
                
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 5
                    size_hint: None, None
                    size: self.minimum_width, self.minimum_height
                    
                    Label:
                        text: 'Messages'
                        color: 1, 1, 1, 1
                        size_hint: None, None
                        size: self.texture_size
                    
                    UBadgeNumber:
                        count: 5
                        color_theme: 'red'
                        size_variant: 'small'
                
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 5
                    size_hint: None, None
                    size: self.minimum_width, self.minimum_height
                    
                    Label:
                        text: 'Notifications'
                        color: 1, 1, 1, 1
                        size_hint: None, None
                        size: self.texture_size
                    
                    UBadgeNumber:
                        count: 127
                        color_theme: 'blue'
                        size_variant: 'small'
                
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 5
                    size_hint: None, None
                    size: self.minimum_width, self.minimum_height
                    
                    Label:
                        text: 'Nouveau'
                        color: 1, 1, 1, 1
                        size_hint: None, None
                        size: self.texture_size
                    
                    UBadgeDot:
                        color_theme: 'green'
                        dot_size: 8
            
            # Badges avec différents variants
            BoxLayout:
                size_hint_y: None
                height: 160
                spacing: 10
                
                Label:
                    text: 'Variants:'
                    size_hint_x: None
                    width: 60
                    color: 1, 1, 1, 1
                    font_size: '12sp'
                
                UBadge:
                    text: 'Solid'
                    color_theme: 'purple'
                    variant: 'solid'
                    size_variant: 'medium'
                
                UBadge:
                    text: 'Outline'
                    color_theme: 'indigo'
                    variant: 'outline'
                    size_variant: 'medium'
                
                UBadge:
                    text: 'Soft'
                    color_theme: 'cyan'
                    variant: 'soft'
                    size_variant: 'medium'
                
                UBadge:
                    text: 'Rounded'
                    color_theme: 'pink'
                    variant: 'solid'
                    size_variant: 'medium'
                    rounded: True
        
        # Exemples de UAlert
        BoxLayout:
            size_hint_y: None
            height: 400
            spacing: 20
            orientation: 'vertical'
            
            Label:
                text: 'Exemples d\\'Alert'
                size_hint_y: None
                height: 30
                color: 1, 1, 1, 1
                font_size: '16sp'
                bold: True
            
            # Alert de succès
            UAlert:
                alert_type: 'success'
                variant: 'soft'
                title: 'Opération réussie'
                description: 'Votre fichier a été sauvegardé avec succès.'
                closable: True
            
            # Alert d'erreur
            UAlert:
                alert_type: 'error'
                variant: 'outline'
                title: 'Erreur de connexion'
                description: 'Impossible de se connecter au serveur. Vérifiez votre connexion internet.'
                closable: True
            
            # Alert d'avertissement
            UAlert:
                alert_type: 'warning'
                variant: 'solid'
                title: 'Attention'
                description: 'Cette action est irréversible. Êtes-vous sûr de vouloir continuer ?'
                closable: False
            
            # Alert d'information
            UAlert:
                alert_type: 'info'
                variant: 'soft'
                title: 'Nouvelle fonctionnalité'
                description: 'Découvrez les nouveaux widgets disponibles dans cette version.'
                closable: True
        
        # Boutons pour créer des alerts dynamiques
        BoxLayout:
            size_hint_y: None
            height: 200
            spacing: 10
            
            UButton:
                color: 'green'
                text: 'Alert Succès'
                on_release: app.show_success_alert()
            
            UButton:
                color: 'red'
                text: 'Alert Erreur'
                on_release: app.show_error_alert()
            
            UButton:
                color: 'orange'
                text: 'Alert Warning'
                on_release: app.show_warning_alert()
            
            UButton:
                color: 'blue'
                text: 'Alert Info'
                on_release: app.show_info_alert()
        
        # Exemples de UCheckbox
        BoxLayout:
            size_hint_y: None
            height: 280
            spacing: 20
            orientation: 'vertical'
            
            Label:
                text: 'Exemples de Checkbox'
                size_hint_y: None
                height: 30
                color: 1, 1, 1, 1
                font_size: '16sp'
                bold: True
            
            # Checkboxes individuelles
            BoxLayout:
                size_hint_y: None
                height: 30
                spacing: 20
                
                Label:
                    text: 'Individuelles:'
                    size_hint_x: None
                    width: 80
                    color: 1, 1, 1, 1
                    font_size: '12sp'
                
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 8
                    size_hint: None, None
                    size: self.minimum_width, self.minimum_height
                    
                    UCheckbox:
                        id: checkbox_small
                        size_variant: 'small'
                        color: 'green'
                        checked: False
                        on_checked: app.on_checkbox_change('Small Checkbox', self.checked)
                    Label:
                        text: 'Small'
                        size_hint_y: None
                        height: 16
                        color: 1, 1, 1, 1
                        font_size: '12sp'
                
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 8
                    size_hint: None, None
                    size: self.minimum_width, self.minimum_height
                    
                    UCheckbox:
                        id: checkbox_medium
                        size_variant: 'medium'
                        color: 'blue'
                        checked: True
                        on_checked: app.on_checkbox_change('Medium Checkbox', self.checked)
                    Label:
                        text: 'Medium (Coché)'
                        size_hint_y: None
                        height: 20
                        color: 1, 1, 1, 1
                        font_size: '14sp'
                
                BoxLayout:
                    orientation: 'horizontal'
                    spacing: 8
                    size_hint: None, None
                    size: self.minimum_width, self.minimum_height
                    
                    UCheckbox:
                        id: checkbox_large
                        size_variant: 'large'
                        color: 'purple'
                        checked: False
                        disabled: True
                        on_checked: app.on_checkbox_change('Large Checkbox (Désactivé)', self.checked)
                    Label:
                        text: 'Large (Désactivé)'
                        size_hint_y: None
                        height: 24
                        color: 0.6, 0.6, 0.6, 1
                        font_size: '16sp'
            
            # Groupe de checkboxes
            BoxLayout:
                size_hint_y: None
                height: 240
                spacing: 20
                
                Label:
                    text: 'Groupe:'
                    size_hint_x: None
                    width: 160
                    color: 1, 1, 1, 1
                    font_size: '12sp'
                
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 8
                    size_hint_y: None
                    height: self.minimum_height
                    
                    Label:
                        text: 'Langages de programmation:'
                        size_hint_y: None
                        height: 20
                        color: 1, 1, 1, 1
                        font_size: '12sp'
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing: 8
                        size_hint: None, None
                        size: self.minimum_width, self.minimum_height
                        
                        UCheckbox:
                            id: cb_python
                            color: 'green'
                            value: 'python'
                            checked: True
                            on_checked: app.on_language_change()
                        Label:
                            text: 'Python'
                            size_hint_y: None
                            height: 20
                            color: 1, 1, 1, 1
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing: 8
                        size_hint: None, None
                        size: self.minimum_width, self.minimum_height
                        
                        UCheckbox:
                            id: cb_javascript
                            color: 'orange'
                            value: 'javascript'
                            checked: False
                            on_checked: app.on_language_change()
                        Label:
                            text: 'JavaScript'
                            size_hint_y: None
                            height: 20
                            color: 1, 1, 1, 1
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing: 8
                        size_hint: None, None
                        size: self.minimum_width, self.minimum_height
                        
                        UCheckbox:
                            id: cb_rust
                            color: 'red'
                            value: 'rust'
                            checked: False
                            on_checked: app.on_language_change()
                        Label:
                            text: 'Rust'
                            size_hint_y: None
                            height: 20
                            color: 1, 1, 1, 1
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        spacing: 8
                        size_hint: None, None
                        size: self.minimum_width, self.minimum_height
                        
                        UCheckbox:
                            id: cb_go
                            color: 'blue'
                            value: 'go'
                            checked: True
                            on_checked: app.on_language_change()
                        Label:
                            text: 'Go'
                            size_hint_y: None
                            height: 20
                            color: 1, 1, 1, 1
        
        # Exemples de USlider
        BoxLayout:
            size_hint_y: None
            height: 200
            spacing: 20
            orientation: 'vertical'
            
            Label:
                text: 'Exemples de Slider'
                size_hint_y: None
                height: 30
                color: 1, 1, 1, 1
                font_size: '16sp'
                bold: True
            
            # Sliders simples
            BoxLayout:
                size_hint_y: None
                height: 50
                spacing: 20
                
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 8
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 20
                        
                        Label:
                            text: 'Volume'
                            size_hint_x: 0.7
                            color: 1, 1, 1, 1
                            font_size: '14sp'
                        
                        Label:
                            id: volume_value
                            text: '50'
                            size_hint_x: 0.3
                            color: 0.8, 0.8, 0.8, 1
                            font_size: '12sp'
                            halign: 'right'
                    
                    USlider:
                        id: volume_slider
                        value: 50
                        min_value: 0
                        max_value: 100
                        step: 1
                        color: 'green'
                        on_value: volume_value.text = str(int(self.value))
                
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 8
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 20
                        
                        Label:
                            text: 'Luminosité'
                            size_hint_x: 0.7
                            color: 1, 1, 1, 1
                            font_size: '14sp'
                        
                        Label:
                            id: brightness_value
                            text: '75'
                            size_hint_x: 0.3
                            color: 0.8, 0.8, 0.8, 1
                            font_size: '12sp'
                            halign: 'right'
                    
                    USlider:
                        id: brightness_slider
                        value: 75
                        min_value: 0
                        max_value: 100
                        step: 5
                        color: 'orange'
                        on_value: brightness_value.text = str(int(self.value))
            
            # Slider avec plage de prix
            BoxLayout:
                size_hint_y: None
                height: 100
                spacing: 20
                
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 8
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 20
                        
                        Label:
                            text: 'Prix (€)'
                            size_hint_x: 0.7
                            color: 1, 1, 1, 1
                            font_size: '14sp'
                        
                        Label:
                            id: price_value
                            text: '250€'
                            size_hint_x: 0.3
                            color: 0.8, 0.8, 0.8, 1
                            font_size: '12sp'
                            halign: 'right'
                    
                    USlider:
                        id: price_slider
                        value: 250
                        min_value: 0
                        max_value: 1000
                        step: 10
                        color: 'blue'
                        on_value: price_value.text = str(int(self.value)) + '€'
                
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 8
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 20
                        
                        Label:
                            text: 'Température'
                            size_hint_x: 0.7
                            color: 1, 1, 1, 1
                            font_size: '14sp'
                        
                        Label:
                            id: temp_value
                            text: '20.5°C'
                            size_hint_x: 0.3
                            color: 0.8, 0.8, 0.8, 1
                            font_size: '12sp'
                            halign: 'right'
                    
                    USlider:
                        id: temp_slider
                        value: 20.5
                        min_value: -10
                        max_value: 40
                        step: 0.5
                        color: 'red'
                        on_value: temp_value.text = str(self.value) + '°C'
            
            # Slider désactivé
            BoxLayout:
                size_hint_y: None
                height: 50
                
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 8
                    
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint_y: None
                        height: 20
                        
                        Label:
                            text: 'Désactivé'
                            size_hint_x: 0.7
                            color: 0.6, 0.6, 0.6, 1
                            font_size: '14sp'
                        
                        Label:
                            text: '30'
                            size_hint_x: 0.3
                            color: 0.5, 0.5, 0.5, 1
                            font_size: '12sp'
                            halign: 'right'
                    
                    USlider:
                        value: 30
                        min_value: 0
                        max_value: 100
                        color: 'purple'
                        disabled: True
        
        # Exemples de USelect
        BoxLayout:
            size_hint_y: None
            height: 200
            spacing: 20
            orientation: 'vertical'
            
            Label:
                text: 'Exemples de Select'
                size_hint_y: None
                height: 30
                color: 1, 1, 1, 1
                font_size: '16sp'
                bold: True
            
            # Selects simples
            BoxLayout:
                size_hint_y: None
                height: 50
                spacing: 20
                
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 4
                    
                    Label:
                        text: 'Langage préféré'
                        size_hint_y: None
                        height: 20
                        color: 1, 1, 1, 1
                        font_size: '14sp'
                        bold: True
                    
                    USelect:
                        id: language_select
                        placeholder: 'Choisir un langage'
                        color: 'green'
                        size_variant: 'medium'
                        on_selected_value: app.on_language_select(self.selected_value)
                
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 4
                    
                    Label:
                        text: 'Niveau d\\'expérience'
                        size_hint_y: None
                        height: 20
                        color: 1, 1, 1, 1
                        font_size: '14sp'
                        bold: True
                    
                    USelect:
                        id: level_select
                        placeholder: 'Sélectionner le niveau'
                        color: 'blue'
                        size_variant: 'medium'
                        on_selected_value: app.on_level_select(self.selected_value)
            
            # Select avec validation
            BoxLayout:
                size_hint_y: None
                height: 70
                spacing: 20
                
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 4
                    
                    Label:
                        text: 'Pays (requis)'
                        size_hint_y: None
                        height: 20
                        color: 1, 1, 1, 1
                        font_size: '14sp'
                        bold: True
                    
                    USelect:
                        id: country_select
                        placeholder: 'Sélectionner un pays'
                        color: 'orange'
                        size_variant: 'medium'
                        required: True
                        on_selected_value: app.on_country_select(self.selected_value)
                    
                    Label:
                        id: country_error
                        text: ''
                        size_hint_y: None
                        height: self.texture_size[1] if self.text else 0
                        color: 0.9, 0.3, 0.3, 1
                        font_size: '12sp'
                
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 4
                    
                    Label:
                        text: 'Taille (désactivé)'
                        size_hint_y: None
                        height: 20
                        color: 0.6, 0.6, 0.6, 1
                        font_size: '14sp'
                        bold: True
                    
                    USelect:
                        id: size_select
                        placeholder: 'Sélectionner la taille'
                        color: 'purple'
                        size_variant: 'medium'
                        disabled: True
            
            # Boutons d'action
            BoxLayout:
                size_hint_y: None
                height: 40
                spacing: 10
                
                UButton:
                    color: 'green'
                    text: 'Valider sélections'
                    on_release: app.validate_selections()
                
                UButton:
                    color: 'red'
                    variant: 'outline'
                    text: 'Réinitialiser'
                    on_release: app.reset_selections()
        
        # Exemples de UTabs
        BoxLayout:
            size_hint_y: None
            height: 300
            spacing: 20
            orientation: 'vertical'
            
            Label:
                text: 'Exemples de Tabs'
                size_hint_y: None
                height: 30
                color: 1, 1, 1, 1
                font_size: '16sp'
                bold: True
            
            UTabs:
                id: main_tabs
                color: 'blue'
                size_hint_y: None
                height: 250
        
        # Widgets existants
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10
            MyDropDown:
                items: self.myitems
            UButton:
                color: 'stone'
                variant: 'outline'
                text: 'Save'
                right_icon: 'material-symbols--save-as-outline-rounded.png'
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10
            UButton:
                left_icon: 'material-symbols--search-rounded.png'
                variant: 'outline'
                text: 'More Button'
                on_release:
                    self.text = 'pushed'
            DatePicker:
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10
            UButton:
                color: 'purple'
                text: 'Button'
                right_icon: 'material-symbols--person-edit-outline.png'
            UButton:
                color: 'orange'
                variant: 'outline'
                text: 'Button'
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10
            UButton:
                color: 'orange'
                variant: 'outline'
                text: 'More Button'
                on_release:
                    self.text = 'pushed'
            UButton:
                color: 'orange'
                text: 'More Button'
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10
            UButton:
                color: 'stone'
                text: 'Button'
            UButton:
                color: 'stone'
                variant: 'outline'
                text: 'Button'
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10
            UButton:
                color: 'indigo'
                variant: 'solid'
                text: 'More Button'
                on_release:
                    self.text = 'pushed'
            UButton:
                color: 'stone'
                text: 'More Button'
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10
            UTextInput:
                color: 'red'
                text: 'More TextInput'
            UTextInput:
                color: 'sky'
                text: 'More textinput'
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10
            UTextInput:
                color: 'green'
                text: 'More TextInput'
            UTextInput:
                color: 'indigo'
                text: 'More textinput'
        
        # Test UDataTable
        Label:
            text: 'UDataTable - Tableau de données'
            size_hint_y: None
            height: 40
            color: 1, 1, 1, 1
        
        UDataTable:
            id: datatable
            size_hint_y: None
            height: 300
"""


class MyDropDown(UDropDown):
    def profile(self):
        print("Profile")

    def edit(self):
        print("Edit")

    myitems = [ [{'label': 'Profile', 'on_release':profile}],
                [{'label': 'Edit', 'on_press':edit}, {'label': 'Duplicate'}],
                [{'label': 'Archive'}, {'label': 'Move'}],
                [{'label': 'Delete'}]]


class MyApp(App):
    def build(self):
        root = Builder.load_string(KV)
        
        # Configurer les options des selects après la création
        try:
            # Select des langages
            language_select = root.ids.get('language_select')
            if language_select:
                language_select.options = [
                    {'text': 'Python', 'value': 'python'},
                    {'text': 'JavaScript', 'value': 'js'},
                    {'text': 'Rust', 'value': 'rust'},
                    {'text': 'Go', 'value': 'go'},
                    {'text': 'TypeScript', 'value': 'ts'}
                ]
            
            # Select des niveaux
            level_select = root.ids.get('level_select')
            if level_select:
                level_select.options = ['Débutant', 'Intermédiaire', 'Avancé', 'Expert']
            
            # Select des pays
            country_select = root.ids.get('country_select')
            if country_select:
                country_select.options = [
                    {'text': 'France', 'value': 'FR'},
                    {'text': 'Allemagne', 'value': 'DE'},
                    {'text': 'Espagne', 'value': 'ES'},
                    {'text': 'Italie', 'value': 'IT'},
                    {'text': 'États-Unis', 'value': 'US'},
                    {'text': 'Canada', 'value': 'CA'}
                ]
            
            # Select des tailles
            size_select = root.ids.get('size_select')
            if size_select:
                size_select.options = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
            
            # Configuration des tabs
            main_tabs = root.ids.get('main_tabs')
            if main_tabs:
                self._setup_tabs(main_tabs)
                
        except Exception as e:
            print(f"Erreur lors de la configuration des widgets: {e}")
        
        # Configurer le DataTable
        Clock.schedule_once(lambda dt: self.setup_datatable(), 0.1)
        
        return root
    
    def _setup_tabs(self, tabs_widget):
        """Configure les tabs avec du contenu"""
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout
        from gakoui.widgets import UButton, UBadge, UToggle
        
        # Tab 1: Vue d'ensemble
        overview_content = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20, 20, 20])
        overview_content.add_widget(Label(
            text="Vue d'ensemble de GakoUI",
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=30,
            color=(1, 1, 1, 1)
        ))
        overview_content.add_widget(Label(
            text="GakoUI est une bibliothèque de widgets modernes pour Kivy, inspirée de NuxtUI.\n\n"
                 "Widgets disponibles:\n"
                 "• UButton - Boutons avec variants et icônes\n"
                 "• UCard - Cartes avec header/footer\n"
                 "• UModal - Fenêtres modales\n"
                 "• UToggle - Interrupteurs animés\n"
                 "• UBadge - Indicateurs et badges\n"
                 "• UAlert - Messages et notifications\n"
                 "• UCheckbox - Cases à cocher\n"
                 "• USlider - Curseurs de valeurs\n"
                 "• USelect - Listes déroulantes\n"
                 "• UTabs - Navigation par onglets",
            text_size=(None, None),
            halign='left',
            valign='top',
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        # Tab 2: Composants
        components_content = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20, 20, 20])
        components_content.add_widget(Label(
            text='Composants disponibles',
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=30,
            color=(1, 1, 1, 1)
        ))
        
        # Ajouter quelques widgets de démonstration
        demo_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        demo_box.add_widget(UButton(text='Demo Button', color='green', size_hint_x=None, width=120))
        demo_box.add_widget(UBadge(text='Nouveau', color_theme='red', size_hint_x=None, width=80))
        demo_box.add_widget(UToggle(color='blue', size_hint_x=None, width=50))
        components_content.add_widget(demo_box)
        
        components_content.add_widget(Label(
            text="Tous les widgets suivent les mêmes conventions de design:\n"
                 "• Couleurs cohérentes avec le système de thème\n"
                 "• Variants multiples (solid, outline, ghost, soft)\n"
                 "• Tailles configurables (small, medium, large)\n"
                 "• États hover et disabled\n"
                 "• API simple et intuitive",
            text_size=(None, None),
            halign='left',
            valign='top',
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        # Tab 3: Configuration
        config_content = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20, 20, 20])
        config_content.add_widget(Label(
            text='Configuration et utilisation',
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height=30,
            color=(1, 1, 1, 1)
        ))
        config_content.add_widget(Label(
            text="Installation:\n"
                 "pip install gakoui\n\n"
                 "Utilisation de base:\n"
                 "from gakoui.widgets import UButton, UCard\n\n"
                 "button = UButton(\n"
                 '    text="Mon bouton",\n'
                 '    color="blue",\n'
                 '    variant="solid"\n'
                 ")\n\n"
                 "Personnalisation des couleurs:\n"
                 "Les couleurs sont définies dans gakoui/data/colors.py\n"
                 "Vous pouvez ajouter vos propres thèmes de couleurs.",
            text_size=(None, None),
            halign='left',
            valign='top',
            color=(0.9, 0.9, 0.9, 1)
        ))
        
        # Ajouter les tabs
        tabs_widget.add_tab('overview', "Vue d'ensemble", overview_content, badge_text='')
        tabs_widget.add_tab('components', 'Composants', components_content, badge_text='10')
        tabs_widget.add_tab('config', 'Configuration', config_content)
        tabs_widget.add_tab('disabled', 'Désactivé', None, disabled=True)
    
    def open_simple_modal(self):
        """Ouvre un modal simple avec du texte"""
        modal = UModal(
            title="Modal Simple",
            modal_width=350,
            modal_height=200,
            closable=True
        )
        
        # Ajouter du contenu
        from kivy.uix.label import Label
        content = Label(
            text="Ceci est un modal simple avec du texte.\nVous pouvez le fermer en cliquant sur X ou à l'extérieur.",
            text_size=(300, None),
            halign='center',
            color=(1, 1, 1, 1)
        )
        modal.add_content(content)
        
        # Ajouter un bouton de fermeture
        from gakoui.widgets import UButton
        close_btn = UButton(
            text="Fermer",
            color="stone",
            size_hint_x=None,
            width=100
        )
        close_btn.bind(on_release=lambda x: modal.dismiss())
        modal.add_footer_button(close_btn)
        
        modal.open()
    
    def open_form_modal(self):
        """Ouvre un modal avec un formulaire"""
        modal = UModal(
            title="Formulaire",
            modal_width=400,
            modal_height=350,
            closable=True
        )
        
        # Créer un formulaire
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from gakoui.widgets import UTextInput, UButton
        
        form = BoxLayout(orientation='vertical', spacing=10)
        
        # Champs du formulaire
        form.add_widget(Label(text="Nom:", size_hint_y=None, height=30, color=(1,1,1,1)))
        name_input = UTextInput(color='blue', text='', hint_text='Entrez votre nom')
        form.add_widget(name_input)
        
        form.add_widget(Label(text="Email:", size_hint_y=None, height=30, color=(1,1,1,1)))
        email_input = UTextInput(color='green', text='', hint_text='Entrez votre email')
        form.add_widget(email_input)
        
        modal.add_content(form)
        
        # Boutons du footer
        cancel_btn = UButton(
            text="Annuler",
            color="stone",
            variant="outline",
            size_hint_x=None,
            width=100
        )
        cancel_btn.bind(on_release=lambda x: modal.dismiss())
        
        save_btn = UButton(
            text="Sauvegarder",
            color="green",
            size_hint_x=None,
            width=120
        )
        save_btn.bind(on_release=lambda x: self._save_form(modal, name_input.text, email_input.text))
        
        modal.add_footer_button(cancel_btn)
        modal.add_footer_button(save_btn)
        
        modal.open()
    
    def open_confirm_modal(self):
        """Ouvre un modal de confirmation"""
        modal = UModal(
            title="Confirmation",
            modal_width=350,
            modal_height=180,
            closable=False,  # Pas de X pour forcer le choix
            auto_dismiss=False
        )
        
        # Message de confirmation
        from kivy.uix.label import Label
        message = Label(
            text="Êtes-vous sûr de vouloir supprimer cet élément ?\nCette action est irréversible.",
            text_size=(300, None),
            halign='center',
            color=(1, 1, 1, 1)
        )
        modal.add_content(message)
        
        # Boutons de confirmation
        from gakoui.widgets import UButton
        cancel_btn = UButton(
            text="Annuler",
            color="stone",
            variant="outline",
            size_hint_x=None,
            width=100
        )
        cancel_btn.bind(on_release=lambda x: modal.dismiss())
        
        confirm_btn = UButton(
            text="Supprimer",
            color="red",
            size_hint_x=None,
            width=100
        )
        confirm_btn.bind(on_release=lambda x: self._confirm_delete(modal))
        
        modal.add_footer_button(cancel_btn)
        modal.add_footer_button(confirm_btn)
        
        modal.open()
    
    def _save_form(self, modal, name, email):
        """Sauvegarde les données du formulaire"""
        print(f"Données sauvegardées: Nom={name}, Email={email}")
        modal.dismiss()
    
    def _confirm_delete(self, modal):
        """Confirme la suppression"""
        print("Élément supprimé!")
        modal.dismiss()
    
    def on_toggle_change(self, name, active):
        """Gère les changements d'état des toggles"""
        state = "activé" if active else "désactivé"
        print(f"{name} est maintenant {state}")
    
    def show_success_alert(self):
        """Affiche un alert de succès dynamique"""
        alert = create_success_alert(
            title="Succès !",
            description="L'alert de succès a été créée dynamiquement.",
            closable=True
        )
        # Ajouter l'alert au début du layout principal
        root = self.root.children[0].children[0]  # ScrollView -> BoxLayout
        root.add_widget(alert, index=len(root.children))
    
    def show_error_alert(self):
        """Affiche un alert d'erreur dynamique"""
        alert = create_error_alert(
            title="Erreur !",
            description="Ceci est un exemple d'alert d'erreur créée dynamiquement.",
            closable=True
        )
        root = self.root.children[0].children[0]
        root.add_widget(alert, index=len(root.children))
    
    def show_warning_alert(self):
        """Affiche un alert d'avertissement dynamique"""
        alert = create_warning_alert(
            title="Attention !",
            description="Cet alert d'avertissement a été ajouté dynamiquement.",
            closable=True
        )
        root = self.root.children[0].children[0]
        root.add_widget(alert, index=len(root.children))
    
    def show_info_alert(self):
        """Affiche un alert d'information dynamique"""
        alert = create_info_alert(
            title="Information",
            description="Voici un alert d'information créé à la volée.",
            closable=True
        )
        root = self.root.children[0].children[0]
        root.add_widget(alert, index=len(root.children))
    
    def on_checkbox_change(self, name, checked):
        """Gère les changements d'état des checkboxes"""
        state = "coché" if checked else "décoché"
        print(f"{name} est maintenant {state}")
    
    def on_language_change(self):
        """Gère les changements dans le groupe de langages"""
        # Récupérer les checkboxes des langages
        root_widget = self.root.children[0].children[0]
        
        # Trouver les checkboxes par leur id (méthode simple pour la démo)
        languages = []
        try:
            if hasattr(self.root, 'ids'):
                if self.root.ids.get('cb_python') and self.root.ids.cb_python.checked:
                    languages.append('Python')
                if self.root.ids.get('cb_javascript') and self.root.ids.cb_javascript.checked:
                    languages.append('JavaScript')
                if self.root.ids.get('cb_rust') and self.root.ids.cb_rust.checked:
                    languages.append('Rust')
                if self.root.ids.get('cb_go') and self.root.ids.cb_go.checked:
                    languages.append('Go')
        except:
            pass
        
        if languages:
            print(f"Langages sélectionnés: {', '.join(languages)}")
        else:
            print("Aucun langage sélectionné")
    
    def on_language_select(self, value):
        """Gère la sélection du langage"""
        if value:
            print(f"Langage sélectionné: {value}")
    
    def on_level_select(self, value):
        """Gère la sélection du niveau"""
        if value:
            print(f"Niveau sélectionné: {value}")
    
    def on_country_select(self, value):
        """Gère la sélection du pays"""
        if value:
            print(f"Pays sélectionné: {value}")
        # Effacer le message d'erreur si un pays est sélectionné
        try:
            country_error = self.root.ids.get('country_error')
            if country_error:
                country_error.text = ''
        except:
            pass
    
    def validate_selections(self):
        """Valide toutes les sélections"""
        try:
            # Récupérer les widgets de sélection
            language_select = self.root.ids.get('language_select')
            level_select = self.root.ids.get('level_select')
            country_select = self.root.ids.get('country_select')
            country_error = self.root.ids.get('country_error')
            
            # Valider le pays (requis)
            if country_select and not country_select.selected_value:
                if country_error:
                    country_error.text = 'Ce champ est requis'
                print("Erreur: Veuillez sélectionner un pays")
                return
            
            # Afficher un résumé des sélections
            selections = []
            if language_select and language_select.selected_value:
                selections.append(f"Langage: {language_select.get_selected_text()}")
            if level_select and level_select.selected_value:
                selections.append(f"Niveau: {level_select.selected_value}")
            if country_select and country_select.selected_value:
                selections.append(f"Pays: {country_select.get_selected_text()}")
            
            if selections:
                print("Sélections validées:")
                for selection in selections:
                    print(f"  - {selection}")
            else:
                print("Aucune sélection à valider")
                
        except Exception as e:
            print(f"Erreur lors de la validation: {e}")
    
    def reset_selections(self):
        """Remet à zéro toutes les sélections"""
        try:
            # Récupérer les widgets de sélection
            language_select = self.root.ids.get('language_select')
            level_select = self.root.ids.get('level_select')
            country_select = self.root.ids.get('country_select')
            country_error = self.root.ids.get('country_error')
            
            # Réinitialiser les sélections
            if language_select:
                language_select.clear_selection()
            if level_select:
                level_select.clear_selection()
            if country_select:
                country_select.clear_selection()
            if country_error:
                country_error.text = ''
            
            print("Toutes les sélections ont été réinitialisées")
            
        except Exception as e:
            print(f"Erreur lors de la réinitialisation: {e}")
    
    def setup_datatable(self):
        """Configure le DataTable avec des données d'exemple"""
        datatable = self.root.ids.datatable
        
        # Configuration des colonnes
        columns = [
            {'key': 'id', 'title': 'ID', 'width': 60, 'align': 'center'},
            {'key': 'name', 'title': 'Nom', 'width': 140},
            {'key': 'email', 'title': 'Email', 'width': 180},
            {'key': 'age', 'title': 'Âge', 'width': 60, 'align': 'center'},
            {'key': 'city', 'title': 'Ville', 'width': 100},
            {'key': 'status', 'title': 'Statut', 'width': 80, 'align': 'center'}
        ]
        
        # Données d'exemple
        data = [
            {'id': 1, 'name': 'Alice Martin', 'email': 'alice@example.com', 'age': 28, 'city': 'Paris', 'status': 'Actif'},
            {'id': 2, 'name': 'Bob Dupont', 'email': 'bob@example.com', 'age': 34, 'city': 'Lyon', 'status': 'Inactif'},
            {'id': 3, 'name': 'Claire Bernard', 'email': 'claire@example.com', 'age': 25, 'city': 'Marseille', 'status': 'Actif'},
            {'id': 4, 'name': 'David Moreau', 'email': 'david@example.com', 'age': 42, 'city': 'Toulouse', 'status': 'Actif'},
            {'id': 5, 'name': 'Emma Petit', 'email': 'emma@example.com', 'age': 31, 'city': 'Nice', 'status': 'Inactif'},
            {'id': 6, 'name': 'François Roux', 'email': 'francois@example.com', 'age': 29, 'city': 'Nantes', 'status': 'Actif'},
            {'id': 7, 'name': 'Gabrielle Simon', 'email': 'gabrielle@example.com', 'age': 26, 'city': 'Strasbourg', 'status': 'Actif'},
            {'id': 8, 'name': 'Henri Laurent', 'email': 'henri@example.com', 'age': 38, 'city': 'Bordeaux', 'status': 'Inactif'}
        ]
        
        # Configuration du tableau
        datatable.columns = columns
        datatable.data = data
        datatable.selectable = True
        datatable.sortable = True
        datatable.striped = True
        
        # Événements
        datatable.bind(on_row_select=self.on_datatable_row_select)
        datatable.bind(on_column_sort=self.on_datatable_column_sort)
    
    def on_datatable_row_select(self, table, row_index, row_data):
        """Gère la sélection de ligne dans le DataTable"""
        print(f"Ligne sélectionnée: {row_index} - {row_data['name']} ({row_data['email']})")
    
    def on_datatable_column_sort(self, table, column_key):
        """Gère le tri par colonne dans le DataTable"""
        print(f"Tri par colonne: {column_key}")
        
        # Tri simple avec alternance croissant/décroissant
        if not hasattr(table, '_sort_reverse'):
            table._sort_reverse = {}
        
        reverse = table._sort_reverse.get(column_key, False)
        table.sort_by_column(column_key, reverse)
        table._sort_reverse[column_key] = not reverse
        
        order = "décroissant" if reverse else "croissant"
        print(f"Données triées par {column_key} en ordre {order}")

MyApp().run()