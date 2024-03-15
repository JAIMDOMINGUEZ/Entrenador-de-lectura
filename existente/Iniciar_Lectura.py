
    # Python code
import PyPDF2
import os
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
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
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from consultas import separar_pdf


kv_code = """
<Iniciar_lectura>:
    canvas.before:
        Color:
            rgba: 0.254902, 0.254902, 0.254902, 1
        Rectangle:
            size: root.size
            pos: root.pos

    TextInput:
        id: textf_parrafo
        text: ""
        multiline: True
        pos_hint: {'x':0.0346021, 'y':0.255814}
        size_hint: (0.934256, 0.604651)
        foreground_color: [0.0313725, 0.0313725, 0.0313725, 1]
        background_color: [0.909804, 0.909804, 0.909804, 1]
        max_length: 1000
        readonly: True

    ProgressBar:
        id: barra_progreso
        max: 100
        value: 0
        pos_hint: {'x':0.0346021, 'y':0.181395}
        size_hint: (0.934256, 0.0511628)

    Button:
        text: "Siguiente"
        pos_hint: {'x':0.657439, 'y':0.0651163}
        size_hint: (0.311419, 0.0744186)
        color: [1, 1, 1, 1]
        background_color: [0, 0, 0, 1]
        on_press: root.siguiente_parrafo()

<MainApp>:
    Iniciar_lectura:
"""

Builder.load_string(kv_code)

class Iniciar_lectura(RelativeLayout):
    def __init__(self,tamanio,color,tipografia,velocidad,archivo, **kwargs):
        super(Iniciar_lectura, self).__init__(**kwargs)
        self.max_value = 100
        self.current_value = self.max_value
        Clock.schedule_interval(self.decrementar_barra, 0.1)
        self.indice_actual = 0
        self.clock_event = None
        self.documento=archivo
        self.velocidad = 1  # Velocidad predeterminada  
        self.asignarprefencias(tamanio,color,tipografia,velocidad)
        self.iniciar_temporizador()
        self.actualizar_texto() 

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def decrementar_barra(self, dt):
        if self.current_value > 0:
            self.current_value -= 1
            self.ids.barra_progreso.value = self.current_value
        else:
            self.current_value = self.max_value
            self.actualizar_texto()

    def siguiente_parrafo(self):
        self.actualizar_texto()
        self.current_value = self.max_value
        Clock.schedule_once(self.detener_temporizador, 0.5)

    def actualizar_texto(self):
        contenido = separar_pdf(self.documento)
        self.ids.textf_parrafo.text = ""
        if self.indice_actual < len(contenido) and len(contenido) > 0:
            self.ids.textf_parrafo.text = contenido[self.indice_actual]
            self.indice_actual = (self.indice_actual + 1)
        else:
            self.mostrar_popup_felicidades()

    def mostrar_popup_felicidades(self):
        popup = Popup(title='¡Felicidades!',
                      size_hint=(None, None), size=(300, 200))
        boton_cerrar = Button(text='Cerrar', size_hint_y=None, height=40)
        boton_cerrar.bind(on_press=lambda *args: self.dismiss())

        contenido = BoxLayout(orientation='vertical')
        contenido.add_widget(Label(text='Has terminado tu lección.'))
        contenido.add_widget(boton_cerrar)
        popup.content = contenido
        popup.open()


    def iniciar_temporizador(self):
        intervalo=0.60
      
        if self.velocidad == 4:
            intervalo = 0.1
        elif self.velocidad == 3:
            intervalo = 0.2
        elif self.velocidad == 2:
            intervalo = 0.5
        elif self.velocidad == 1:
            intervalo = 0.6
        
        if self.clock_event is not None:
            self.clock_event.cancel()
        self.clock_event = Clock.schedule_interval(self.decrementar_barra, intervalo)

    def detener_temporizador(self, dt):
        if self.clock_event is not None:
            self.clock_event.cancel()

    def asignarprefencias(self,tamanio,color,tipografia,velocidad):
        self.velocidad = velocidad
        self.ids.textf_parrafo.foreground_color = color
        self.ids.textf_parrafo.font_name = tipografia
        self.ids.textf_parrafo.font_size = tamanio

class IniciarLecturaApp(App):
    def __init__(self, tamanio, color, tipografia, velocidad,archivo):
        super(IniciarLecturaApp, self).__init__()
        self.tamanio = tamanio
        self.color = color
        self.tipografia = tipografia
        self.velocidad = velocidad
        self.archivo=archivo
    
    def build(self):
        self.root = Iniciar_lectura(self.tamanio,self.color,self.tipografia,self.velocidad,self.archivo)
        return self.root

if __name__ == '__main__':
    IniciarLecturaApp.run()


    def mostrar_popup_felicidades(self):
        popup = Popup(title='¡Felicidades!',
                      content=Label(text='Has terminado tu lección.'),
                      size_hint=(None, None), size=(300, 200))  # Ajuste el tamaño aquí
        

        boton_cerrar = Button(text='Cerrar', size_hint_y=None, height=40)  # Agregar un botón con tamaño personalizado
        boton_cerrar.bind(on_press=self.cambiar_a_pantalla_inicio)



        contenido = BoxLayout(orientation='vertical')
        contenido.add_widget(Label(text='Has terminado tu lección.'))
        contenido.add_widget(boton_cerrar)  # Agregar el botón al contenido
        popup.content = contenido  # Actualizar el contenido del Popup
        popup.open()

    
    def cambiar_a_pantalla_inicio(self, instance):
        from Home import Home  # Importa la clase MainApp del archivo home.py
        App.get_running_app().stop()  # Detiene la aplicación actual
        Home().run()  # Ejecuta la nueva aplicación Home

    def iniciar_temporizador(self):
        intervalo=0.60
        
        if self.velocidad == 4:
            intervalo = 0.1
        elif self.velocidad == 3:
            intervalo = 0.2
        elif self.velocidad == 2:
            intervalo = 0.5
        elif self.velocidad == 1:
            intervalo = 0.6
        
        if self.clock_event is not None:
            self.clock_event.cancel()
        self.clock_event = Clock.schedule_interval(self.decrementar_barra, intervalo)

    def detener_temporizador(self, dt):
        if self.clock_event is not None:
            self.clock_event.cancel()

    def asignarprefencias(self,tamanio,color,tipografia,velocidad):
        self.velocidad = velocidad
        self.ids.textf_parrafo.foreground_color = color
        self.ids.textf_parrafo.font_name = tipografia
        self.ids.textf_parrafo.font_size = tamanio

class IniciarLecturaApp(App):
    def __init__(self, tamanio, color, tipografia, velocidad,archivo):
        super(IniciarLecturaApp, self).__init__()
        self.tamanio = tamanio
        self.color = color
        self.tipografia = tipografia
        self.velocidad = velocidad
        self.archivo=archivo
    
    def build(self):
        self.root = Iniciar_lectura(self.tamanio,self.color,self.tipografia,self.velocidad,self.archivo)
        return self.root

if __name__ == '__main__':
    IniciarLecturaApp.run()
