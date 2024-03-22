import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from Controlador import ControladorCuentas
from Vista import VentanaIniciarSesion
class RootLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Establecer el color de fondo como blanco (RGBA)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = self.size
        self.rect.pos = self.pos

class CreaCuentaApp(App):
    def build(self):
        root = RootLayout(orientation='vertical')
        self.controlador = ControladorCuentas()
        ventana_iniciar_session = VentanaIniciarSesion(self.controlador)
        root.add_widget(ventana_iniciar_session)
        return root
if __name__ == "__main__":
    CreaCuentaApp().run()