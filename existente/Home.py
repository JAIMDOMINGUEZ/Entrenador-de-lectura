from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from Administrar import MainAppp  # Importar la clase MainAppp del otro archivo
from kivy.config import Config
from seleccionarlectura import SeleccionarLecturaApp

class Home(BoxLayout):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.gui()

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def gui(self):
        # Crear el diseño principal
        self.layout = RelativeLayout()
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.layout.bind(pos=self.update_rect, size=self.update_rect)

        # Crear la etiqueta "Entrenador De Lectura"
        label1 = Label(text="Entrenador De Lectura", size_hint=(None, None), size=(Window.width, 100),
                       font_family="MS Shell Dlg 2", font_size="20sp", color=[0, 0, 0, 1])
        label1.bind(size=label1.setter('text_size'), texture_size=label1.setter('size'))
        label1.pos_hint = {'center_x': 0.5, 'top': 0.9}
        self.layout.add_widget(label1)

        # Crear los botones
        button1 = Button(text="Administrar Lecturas", size_hint=(None, None), size=(200, 50),
                         font_family="MS Shell Dlg 2", font_size="15sp", color=[1, 1, 1, 1])
        button1.bind(on_press=self.ir_a_Administrador)
        button1.pos_hint = {'center_x': 0.5, 'y': 0.7}

        button2 = Button(text="Iniciar Lectura", size_hint=(None, None), size=(200, 50),
                         font_family="MS Shell Dlg 2", font_size="15sp", color=[1, 1, 1, 1])
        button2.bind(on_press=self.iniciar_lectura)
        button2.pos_hint = {'center_x': 0.5, 'y': 0.6}

        # Agregar los elementos al diseño principal
        self.layout.add_widget(button1)
        self.layout.add_widget(button2)

        # Agregar el diseño principal al diseño de la pantalla Home
        self.add_widget(self.layout)

    def ir_a_Administrador(self, instance):
        # Crear una instancia de la clase Administrador
        ventana_Admin = MainAppp()

        # Cambiar a la nueva instancia de la aplicación
        App.get_running_app().stop()  # Detener la aplicación actual
        ventana_Admin.run()  # Ejecutar la nueva aplicación

    def iniciar_lectura(self, widget):
        print('iniciar_lectura')
        Config.set('input', 'wm_touch', '')
        self.main_app = SeleccionarLecturaApp()
        self.main_app.run()

class MainApp(App):
    def build(self):
        return Home()


if __name__ == '__main__':
    MainApp().run()
