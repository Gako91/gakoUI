"""Demo: UModal — open a styled modal with body and footer buttons.

Run: uv run python demos/demo_modal.py
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

from gakoui.widgets import UButton, UModal

Window.size = (520, 360)


class ModalDemoApp(App):
    title = "GakoUI · UModal"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=14)
        root.add_widget(Label(
            text="Click the button to open a modal.",
            color=(0.85, 0.85, 0.85, 1),
        ))

        open_btn = UButton(text="Open modal", color="blue",
                           size_hint=(None, None), size=(180, 44))
        open_btn.bind(on_release=lambda *_: self._open())
        wrap = BoxLayout(size_hint_y=None, height=60)
        wrap.add_widget(open_btn)
        root.add_widget(wrap)
        return root

    def _open(self):
        modal = UModal(title="Confirm action", modal_width=420, modal_height=240)

        body = Label(
            text="Are you sure you want to continue?",
            color=(1, 1, 1, 1),
        )
        modal.add_content(body)

        cancel = UButton(text="Cancel", color="stone", variant="outline",
                         size_hint_x=None, width=110)
        cancel.bind(on_release=lambda *_: modal.dismiss())
        ok = UButton(text="Confirm", color="blue", size_hint_x=None, width=110)
        ok.bind(on_release=lambda *_: modal.dismiss())
        modal.add_footer_button(cancel)
        modal.add_footer_button(ok)

        modal.open()


if __name__ == "__main__":
    ModalDemoApp().run()


if __name__ == "__main__":
    ModalDemoApp().run()
