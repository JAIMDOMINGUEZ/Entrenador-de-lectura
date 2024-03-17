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
from Vista import VentanaCrearCuenta
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
        ventana_crea_cuenta = VentanaCrearCuenta(self.controlador)
        root.add_widget(ventana_crea_cuenta)
        return root
    def on_stop(self):
        # Cerrar la conexión de la base de datos al salir de la aplicación
        self.controlador.modelo.__del__()

if __name__ == "__main__":
    CreaCuentaApp().run()