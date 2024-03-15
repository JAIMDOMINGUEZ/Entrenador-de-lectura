from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.treeview import TreeView
from kivy.uix.treeview import TreeViewLabel
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App
from Iniciar_Lectura import IniciarLecturaApp
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.config import Config

from kivy.uix.floatlayout import FloatLayout



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



class Preferencias(RelativeLayout):
    def __init__(self,archivo, **kwargs):
        super(Preferencias, self).__init__(**kwargs)
        self.popup = None 
        self.archivo=archivo
        self.gui()

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def gui(self):
        
        self.w1 = self
        with self.w1.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.w1.size, pos=self.w1.pos)
        self.w1.bind(pos=self.update_rect, size=self.update_rect)
        self.widget_menu_bar = RelativeLayout(pos_hint ={'x':-0.0772201, 'y':0.860465}, size_hint = (1.46718, 0.162791))
        self.w1.add_widget(self.widget_menu_bar)

        self.home = Button(text = "Home", pos_hint ={'x':0.0526316, 'y':0.4}, size_hint = (0.236842, 0.314286), color = [1, 1, 1, 1])
        self.widget_menu_bar.add_widget(self.home)

        self.lbl_preferencias = Label(text = "Preferencias", halign='left', pos_hint ={'x':0.30888, 'y':0.8}, size_hint = (0.34749, 0.0837209), color = [0, 0, 0, 1])
        self.lbl_preferencias.bind(size=self.lbl_preferencias.setter('text_size'))
        self.w1.add_widget(self.lbl_preferencias)

        self.lbl_tipografia = Label(text = "Tipografia:", halign='left', pos_hint ={'x':0.03861, 'y':0.739535}, size_hint = (0.34749, 0.0511628), color = [0, 0, 0, 1])
        self.lbl_tipografia.bind(size=self.lbl_tipografia.setter('text_size'))
        self.w1.add_widget(self.lbl_tipografia)

        self.select_tipografia = Spinner(text = "Arial", values = ("Arial", "Times New Roman ", "Helvetica"), pos_hint ={'x':0.11583, 'y':0.669767}, size_hint = (0.694981, 0.0511628))
        self.w1.add_widget(self.select_tipografia)

        self.lbl_tamanio = Label(text = "Tamaño:", halign='left', pos_hint ={'x':0.03861, 'y':0.576744}, size_hint = (0.34749, 0.0511628), color = [0.0235294, 0.0235294, 0.0235294, 1])
        self.lbl_tamanio.bind(size=self.lbl_tamanio.setter('text_size'))
        self.w1.add_widget(self.lbl_tamanio)
        
        self.widget2 = RelativeLayout(pos_hint ={'x':0.19305, 'y':0.465116}, size_hint = (0.501931, 0.0930233))
        self.w1.add_widget(self.widget2)
        self.btn_mas_tamanio = Button(text = "+", pos_hint ={'x':0.666667, 'y':-0.05}, size_hint = (0.333333, 1.05))
        self.widget2.add_widget(self.btn_mas_tamanio)
        self.btn_mas_tamanio.bind(on_press = self.mas_tamanio)
        self.btn_menos_tamanio = Button(text = "-", pos_hint ={'x':0, 'y':-0.05}, size_hint = (0.333333, 1.05))
        self.widget2.add_widget(self.btn_menos_tamanio)
        self.btn_menos_tamanio.bind(on_press = self.menos_tamanio)
        self.input_tamanio = TextInput(text = "20", multiline = False, pos_hint ={'x':0.333333, 'y':-0.05}, size_hint = (0.333333, 1.05), foreground_color = [0, 0, 0, 1], background_color = [1, 1, 1, 1],readonly=True ,halign='center')
        self.widget2.add_widget(self.input_tamanio)
        self.widget_omitir_guardar = RelativeLayout(pos_hint ={'x':0.03861, 'y':0}, size_hint = (0.926641, 0.0930233))
        self.w1.add_widget(self.widget_omitir_guardar)
        self.btn_omitir = Button(text = "Omitir", pos_hint ={'x':0, 'y':0.2}, size_hint = (0.375, 0.55), color = [0, 0, 0, 1], background_color = [1, 1, 1, 1])
        self.widget_omitir_guardar.add_widget(self.btn_omitir)
        self.btn_omitir.bind(on_press = self.omitir_preferencias)
        self.btn_guardar = Button(text = "Guardar", pos_hint ={'x':0.625, 'y':0.2}, size_hint = (0.375, 0.55), color = [1, 1, 1, 1], background_color = [0, 0, 0, 1])
        self.widget_omitir_guardar.add_widget(self.btn_guardar)
        self.btn_guardar.bind(on_press = self.guardar_preferencias)
        self.lbl_color = Label(text = "Color:", halign='left', pos_hint ={'x':0.03861, 'y':0.390698}, size_hint = (0.34749, 0.0511628), color = [0, 0, 0, 1])
        self.lbl_color.bind(size=self.lbl_color.setter('text_size'))
        self.w1.add_widget(self.lbl_color)
        self.lbl_velocidad = Label(text = "Velocidad:", halign='left', pos_hint ={'x':0.03861, 'y':0.251163}, size_hint = (0.34749, 0.0511628), color = [0, 0, 0, 1])
        self.lbl_velocidad.bind(size=self.lbl_velocidad.setter('text_size'))
        self.w1.add_widget(self.lbl_velocidad)
        self.widget_color = RelativeLayout(pos_hint ={'x':0.0772201, 'y':0.302326}, size_hint = (0.733591, 0.0930233))
        self.w1.add_widget(self.widget_color)
        self.select_color = Spinner(text = "Rojo", values = ("Rojo", "Negro", "Azul"), pos_hint ={'x':0.210526, 'y':0.2}, size_hint = (0.578947, 0.55), color = [0, 0, 0, 1], background_color = [1, 1, 1, 1])
        self.widget_color.add_widget(self.select_color)
        self.select_color.bind(text = self.cambiar_color)
        self.btn_mas_velocidad = Button(text = "+", pos_hint ={'x':0.501931, 'y':0.134884}, size_hint = (0.15444, 0.0976744))        
        self.w1.add_widget(self.btn_mas_velocidad)
        self.btn_mas_velocidad.bind(on_press = self.mas_velocidad)
        self.btn_menos_velocidad = Button(text = "-", pos_hint ={'x':0.19305, 'y':0.134884}, size_hint = (0.15444, 0.0976744))        
        self.w1.add_widget(self.btn_menos_velocidad)
        self.btn_menos_velocidad.bind(on_press = self.menos_velocidad)
        self.input_velocidad = TextInput(text = "2", multiline = False, pos_hint ={'x':0.34749, 'y':0.134884}, size_hint = (0.15444, 0.0976744), foreground_color = [0, 0, 0, 1], background_color = [1, 1, 1, 1],readonly=True,halign='center')
        self.w1.add_widget(self.input_velocidad)
        return self.w1

    def mas_tamanio(self, widget):
        if(int(self.input_tamanio.text)>=30):
            self.input_tamanio.text=str(30)
        else:
            self.input_tamanio.text=str(int(self.input_tamanio.text)+2)

    def menos_tamanio(self, widget):
        if(int(self.input_tamanio.text)<=2):
            self.input_tamanio.text=str(2)
        else:
            self.input_tamanio.text=str(int(self.input_tamanio.text)-2)

    def mas_velocidad(self, widget):
        if(int(self.input_velocidad.text)>=4):
            self.input_velocidad.text=str(4)
        else:
            self.input_velocidad.text=str(int(self.input_velocidad.text)+1)

    def menos_velocidad(self, widget):
        if(int(self.input_velocidad.text)<=1):
            self.input_velocidad.text=str(1)
        else:
            self.input_velocidad.text=str(int(self.input_velocidad.text)-1)


    def guardar_preferencias(self, widget):
        self.confirmar_guardar()


    def cambiar_color(self, widget, value):
        if value == "Rojo":
            self.select_color.background_color="white"
            self.select_color.color="red"
        if value == "Azul":
            self.select_color.background_color="white"
            self.select_color.color="blue"
        if value == "Negro":
            self.select_color.background_color="white"
            self.select_color.color="black"

    
    def omitir_preferencias(self, instance):
        content = BoxLayout(orientation='vertical')
        message_label = Label(text='¿Estás seguro de que deseas omitir las preferencias?')
        content.add_widget(message_label)
        btn_layout = BoxLayout(size_hint_y=None, height=40)
        btn_layout.add_widget(Button(text='Si', on_release=self.abrir_ventana_iniciar_lectura))
        btn_layout.add_widget(Button(text='No', on_release=self.cerrar_ventana))
        content.add_widget(btn_layout)
        self.popup = Popup(title='Confirmar Omitir', content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()

    def abrir_ventana_iniciar_lectura(self,instance):
        self.popup.dismiss()
        # Deshabilitar la detección de eventos táctiles
        Config.set('input', 'wm_touch', '')
        tamanio=24
        color= [0, 0, 0, 1]
        tipografia="Arial"
        velocidad=4
        archivo=self.archivo
        if instance.text=="Si": 
            Config.set('input', 'wm_touch', '')
            self.main_app = IniciarLecturaApp(tamanio,color,tipografia,velocidad,archivo)
            self.main_app.run()
        elif instance.text=="Continuar":
            print(self.archivo)
            tamanio=self.input_tamanio.text
            color=self.select_color.color
            tipografia=self.select_tipografia.text
            velocidad=self.input_velocidad.text
            archivo=self.archivo
            self.main_app = IniciarLecturaApp(tamanio,color,tipografia,velocidad,archivo)
            self.main_app.run()
    def cerrar_ventana(self, instance):
        self.popup.dismiss()
    def confirmar_guardar(self):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='¿Estás seguro de que deseas guardar las preferencias?',font_size=12))
        btn_layout = BoxLayout(size_hint_y=None, height=40)
        btn_layout.add_widget(Button(text='Continuar', on_release=self.abrir_ventana_iniciar_lectura))
        btn_layout.add_widget(Button(text='No', on_release=self.cerrar_ventana))
        content.add_widget(btn_layout)
        self.popup = Popup(title='Confirmar Guardar', content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()
    

class PreferenciasApp(App):
    def __init__(self,archvo):
        super(PreferenciasApp, self).__init__()
        self.archivo=archvo
    def build(self):
        self.root = Preferencias(self.archivo)
        root = RootLayout()
        return self.root
    
if __name__ == '__main__':
    PreferenciasApp().run()