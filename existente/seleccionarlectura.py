from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from consultas import *
from preferencias import PreferenciasApp
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen


class RootLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)
    
        with self.canvas.before:
            # Establecer el color de fondo como blanco
            Color(1, 1, 1, 1) 
            # Crear un rectángulo que cubra toda la pantalla
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # Escuchar cambios en el tamaño y la posición para actualizar el rectángulo
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        # Actualizar el tamaño y la posición del rectángulo para que cubra toda la pantalla
        self.rect.pos = self.pos
        self.rect.size = self.size


class Seleccionar_Lectura(RelativeLayout):
    def __init__(self, **kwargs):
        super(Seleccionar_Lectura, self).__init__(**kwargs)

        self.gui()

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    
    def go_to_home(self, instance):
        # Acceder al ScreenManager y cambiar a la pantalla 'Home'
        screen_manager = self.parent.parent  # Parent del RootLayout es el ScreenManager
        screen_manager.current = 'Home'

    def gui(self):
        from Home import Home 
        self.w1 = self
        with self.w1.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.w1.size, pos=self.w1.pos)
        self.w1.bind(pos=self.update_rect, size=self.update_rect)
        self.menu_bar = RelativeLayout(pos_hint ={'x':-0.041841, 'y':0.880952}, size_hint = (1.51464, 0.142857))
        self.w1.add_widget(self.menu_bar)

        self.home_button = Button(text="HOME", pos_hint={'x': 0.0294985, 'y': 0.9}, size_hint=(0.2, 0.04))
        self.home_button.bind(on_press=self.go_to_home)  # Vincular el botón al método go_to_home
        self.add_widget(self.home_button)



        self.vertical = BoxLayout(orientation = 'vertical', pos_hint ={'x':0.083682, 'y':0.0714286}, size_hint = (0.83682, 0.714286))
        
        self.w1.add_widget(self.vertical)
        self.Select_Tipo = Spinner(text = "Tipo Lectura", values = ("Cuento", "Novela", "Articulo"), pos_hint ={'x':0.167364, 'y':0.8}, size_hint = (0.627615, 0.0809524), font_family = "MS Shell Dlg 2", font_size = "19", color = [1, 1, 1, 1], background_color = [1, 1, 1, 1])
        self.w1.add_widget(self.Select_Tipo)
        self.Select_Tipo.bind(text = self.on_Select_Tipo)
        return self.w1
    
    
    
    def seleccionador(self, widget, value):
        print('seleccionador')
    def lectura_Seleccionada(self, instance):
        archivo=consultar_por_nombre(instance.text)
        if (1==1):#verificar_existencia_pdf(archivo)
        #
            Config.set('input', 'wm_touch', '')
            self.main_app = PreferenciasApp(archivo)
            self.main_app.run()

        else:
            
            popup_content = Label(text="El archivo no existe.")
            popup = Popup(title="Error", content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()
    def on_Select_Tipo(self, widget, value):
        self.mostar_lecturas(value)

    def mostar_lecturas(self, value):
        self.grid = GridLayout(cols=2, size_hint_y=None)  # Permitir que el tamaño en y no dependa del contenido
        self.grid.bind(minimum_height=self.grid.setter('height'))  # Ajustar automáticamente la altura del GridLayout según el contenido
        lista = []
        if value == "Cuento" or value == "Novela" or value == "Articulo":
            lista = consultar_por_tipo(value)
        for element in lista:
            btn = Button(text=element, background_color=(1, 1, 1, 1), color=(1, 1, 1, 1), size_hint_y=None, height=120)  # Establecer una altura fija para los botones
            btn.text_size = (80, None)
            btn.bind(on_press=self.lectura_Seleccionada)
            self.grid.add_widget(btn)

        # Crear ScrollView y agregar el GridLayout
        scroll_view = ScrollView()
        scroll_view.add_widget(self.grid)

        # Limpiar y agregar ScrollView a la vertical layout
        self.vertical.clear_widgets()
        self.vertical.add_widget(scroll_view)
    
    
  

class SeleccionarLecturaApp(App):
    def build(self):
        from Home import Home 
        sm = ScreenManager()

        # Definir las pantallas
        seleccionar_lectura_screen = Screen(name='seleccionar_lectura')
        home_screen = Screen(name='Home')  # Agregar esta línea

        # Crear instancias de las vistas correspondientes
        seleccionar_lectura_view = Seleccionar_Lectura()
        home_view = Home()  # Agregar esta línea

        # Agregar las vistas a las pantallas
        seleccionar_lectura_screen.add_widget(seleccionar_lectura_view)
        home_screen.add_widget(home_view)  # Agregar esta línea

        # Agregar las pantallas al ScreenManager
        sm.add_widget(seleccionar_lectura_screen)
        sm.add_widget(home_screen)  # Agregar esta línea

        root = RootLayout()
        root.add_widget(sm)
        return root

if __name__ == '__main__':
    SeleccionarLecturaApp().run()
