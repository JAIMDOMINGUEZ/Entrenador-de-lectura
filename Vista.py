from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from Controlador import ControladorCuentas ,ControladorLecturas
from kivy.uix.relativelayout import RelativeLayout

import os
import sqlite3
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.filechooser import FileChooserListView
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout


class VentanaCrearCuenta(BoxLayout):
    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = [50, 20]
        self.controlador = ControladorCuentas
        self.add_widget(Label(text="Crear Cuenta", font_size=40,color=[0, 0, 0, 1]))
        self.add_widget(Label(text="Nombre de Usuario:",color=[0, 0, 0, 1],font_size=20))
        self.username_input = TextInput(multiline=False)
        self.add_widget(self.username_input)
        
        self.add_widget(Label(text="Ingrese Contraseña",color=[0, 0, 0, 1],font_size=20))
        self.password_input = TextInput(multiline=False, password=True)
        self.add_widget(self.password_input)

        self.show_password_button = Button(text="Mostrar Contraseña")
        self.show_password_button.bind(on_press=self.toggle_password_visibility)
        self.add_widget(self.show_password_button)
        
        self.add_widget(Label(text="Confirmar Contraseña",color=[0, 0, 0, 1],font_size=20))
        self.confirm_password_input = TextInput(multiline=False, password=True)
        self.add_widget(self.confirm_password_input)
        
        self.show_confirm_password_button = Button(text="Mostrar Contraseña")
        self.show_confirm_password_button.bind(on_press=self.toggle_confirm_password_visibility)
        self.add_widget(self.show_confirm_password_button)

        self.create_button = Button(text="Crear Cuenta")
        self.create_button.bind(on_press=self.crear_cuenta)
        self.add_widget(self.create_button)
        
        self.add_widget(Label(text="¿Ya tienes una cuenta?", font_size=25,color=[0, 0, 0, 1]))
        self.login_button = Button(text="Iniciar Sesión")
        self.login_button.bind(on_press=lambda instance: self.ir_a_inicio_sesion())

        self.add_widget(self.login_button)


    def toggle_password_visibility(self, instance):
        if self.password_input.password:
            self.password_input.password = False
            self.show_password_button.text = "Ocultar Contraseña"
        else:
            self.password_input.password = True
            self.show_password_button.text = "Mostrar Contraseña"

    def toggle_confirm_password_visibility(self, instance):
        # Cambia la visibilidad de la contraseña en el campo de confirmación
        if self.confirm_password_input.password:
            self.confirm_password_input.password = False
            self.show_confirm_password_button.text = "Ocultar Contraseña"
        else:
            self.confirm_password_input.password = True
            self.show_confirm_password_button.text = "Mostrar Contraseña"

    def crear_cuenta(self, instance):
        nombre_usuario = self.username_input.text
        contraseña = self.password_input.text
        confirmar_contraseña = self.confirm_password_input.text
        
        if nombre_usuario.strip() == '' or contraseña.strip() == '' or confirmar_contraseña.strip() == '':
            self.mostrar_mensaje_campos_vacios()
            return
        
        if contraseña != confirmar_contraseña:
            self.mostrar_mensaje_contrasenas_no_coinciden()
            return
        
        if self.controlador.crear_cuenta(nombre_usuario,contraseña):
            self.mostrar_mensaje_cuenta_creada()
        else:
            self.mostrar_mensaje_usuario_existente()
    
    def mostrar_mensaje_cuenta_creada(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Cuenta creada con éxito", font_size=20))
        popup = Popup(title='Éxito', content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()
    def mostrar_mensaje_usuario_existente(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="El usuario ya existe", font_size=20))
        btn_volver_a_intentarlo = Button(text="Volver a Intentarlo")
        btn_volver_a_intentarlo.bind(on_press=self.volver_a_intentarlo)
        popup_content.add_widget(btn_volver_a_intentarlo)
        self.popup_usuario_existente = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
        self.popup_usuario_existente.open()
    
    def volver_a_intentarlo(self, instance):
        self.popup_usuario_existente.dismiss()
        self.username_input.text = ''
        self.password_input.text = ''
        self.confirm_password_input.text = ''
    
    def mostrar_mensaje_contrasenas_no_coinciden(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Las contraseñas no coinciden", font_size=20))
        btn_volver_a_intentarlo = Button(text="Volver a Intentarlo")
        btn_volver_a_intentarlo.bind(on_press=self.volver_a_intentarlo_contraseñas)
        popup_content.add_widget(btn_volver_a_intentarlo)
        self.popup_contraseñas_no_coinciden = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
        self.popup_contraseñas_no_coinciden.open()
    
    def volver_a_intentarlo_contraseñas(self, instance):
        self.popup_contraseñas_no_coinciden.dismiss()
        self.password_input.text = ''
        self.confirm_password_input.text = ''
    
    def mostrar_mensaje_campos_vacios(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Por favor completa todos los campos", font_size=20))
        btn_ok = Button(text="OK")
        btn_ok.bind(on_press=self.dismiss_popup)
        popup_content.add_widget(btn_ok)
        self.popup_campos_vacios = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
        self.popup_campos_vacios.open()

    def dismiss_popup(self, instance):
        self.popup_campos_vacios.dismiss()
    def ir_a_inicio_sesion(self):
        ventana_inicio_sesion = VentanaIniciarSesion(self)
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_inicio_sesion)

class VentanaIniciarSesion(BoxLayout):
    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = [50, 20]
        self.id_usuario = None
        self.controlador = ControladorCuentas()
        
        self.add_widget(Label(text="Iniciar Sesión", font_size=40, color=[0, 0, 0, 1]))
        
        self.add_widget(Label(text="Nombre de Usuario", color=[0, 0, 0, 1], font_size=20))
        self.username_input = TextInput(multiline=False)
        self.add_widget(self.username_input)
        
        self.add_widget(Label(text="Contraseña", color=[0, 0, 0, 1], font_size=20))
        self.password_input = TextInput(multiline=False, password=True)
        self.add_widget(self.password_input)

        self.show_password_button = Button(text="Mostrar Contraseña")
        self.show_password_button.bind(on_press=self.toggle_password_visibility)
        self.add_widget(self.show_password_button)
        
        self.login_button = Button(text="Iniciar Sesión")
        self.login_button.bind(on_press=self.iniciar_sesion)
        self.add_widget(self.login_button)
        
        self.check_user_button = Button(text="Verificar Usuario")
        self.check_user_button.bind(on_press=self.verificar_usuario)
        self.check_user_button.disabled = True  # Desactiva el botón
        self.check_user_button.opacity = 0
        self.add_widget(self.check_user_button)
        
        self.add_widget(Label(text="¿No tienes una cuenta?", font_size=25, color=[0, 0, 0, 1]))
        self.create_account_button = Button(text="Crear cuenta nueva")
        self.create_account_button.bind(on_press=lambda instance: self.ir_a_crear_cuenta())
        self.add_widget(self.create_account_button)
    
    def toggle_password_visibility(self, instance):
        # Cambia la visibilidad de la contraseña en el campo de entrada
        if self.password_input.password:
            self.password_input.password = False
            self.show_password_button.text = "Ocultar Contraseña"
        else:
            self.password_input.password = True
            self.show_password_button.text = "Mostrar Contraseña"

    def mostrar_mensaje_campos_vacios(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Por favor completa todos los campos", font_size=20))
        btn_ok = Button(text="OK")
        btn_ok.bind(on_press=self.dismiss_popup)
        popup_content.add_widget(btn_ok)
        self.popup_campos_vacios = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
        self.popup_campos_vacios.open()

    def mostrar_mensaje_campos_vacios(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Por favor completa todos los campos", font_size=20))
        btn_ok = Button(text="OK")
        btn_ok.bind(on_press=self.dismiss_popup)
        # Crear el Popup y asignarlo a self.popup_campos_vacios
        self.popup_campos_vacios = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
        self.popup_campos_vacios.open()  # Abre el popup

    def dismiss_popup(self, instance):
        if hasattr(self, 'popup_campos_vacios'):
            self.popup_campos_vacios.dismiss()
    

    def mostrar_mensaje_credenciales_incorrectas(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Nombre de usuario o contraseña incorrectos", font_size=20))
        btn_ok = Button(text="OK")
        btn_ok.bind(on_press=self.dismiss_popup)
        popup = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()

        self.username_input.text = ''
        self.password_input.text = ''

    
    def iniciar_sesion(self, instance):
        nombre_usuario = self.username_input.text
        contraseña = self.password_input.text
        
        if nombre_usuario.strip() == '' or contraseña.strip() == '':
            self.mostrar_mensaje_campos_vacios()
            return

        if self.controlador.iniciar_sesion(nombre_usuario, contraseña):
            print("Inicio de sesión exitoso")
            self.id_usuario=self.controlador.obtener_id_usuario(nombre_usuario,contraseña)
            self.ir_a_Home()
        else:
            self.mostrar_mensaje_credenciales_incorrectas()
    
    def verificar_usuario(self, instance):
        nombre_usuario = self.username_input.text
        
        if self.controlador.verificar_usuario(nombre_usuario):
            popup = Popup(title='Usuario Existente',
                          content=Label(text='El usuario existe en la base de datos.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            popup = Popup(title='Usuario No Existente',
                          content=Label(text='El usuario no existe en la base de datos.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()

    def ir_a_crear_cuenta(self):
        ventana_crea_cuenta = VentanaCrearCuenta(self)
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_crea_cuenta)
    
    def ir_a_Home(self):
        ventana_Home = Home(self.id_usuario)  # Crear una instancia de HOME
        ventana_Home.size = Window.size  # Establecer el tamaño de la ventana Home igual al tamaño de la ventana principal
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Home)
class Home(BoxLayout):
    def __init__(self,id_usuario,**kwargs):
        super(Home, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.id_usuario = id_usuario
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
        label1 = Label(text="Entrenador De Lectura {}".format(self.id_usuario), size_hint=(None, None), size=(Window.width, 100),
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
        #button2.bind(on_press=self.iniciar_lectura)
        button2.pos_hint = {'center_x': 0.5, 'y': 0.6}

        # Agregar los elementos al diseño principal
        self.layout.add_widget(button1)
        self.layout.add_widget(button2)

        # Agregar el diseño principal al diseño de la pantalla Home
        self.add_widget(self.layout)
    def ir_a_Administrador(self, instance):
        # Crear una instancia de la clase Administrador
        ventana_Admin = Administrador()
        ventana_Admin.size = Window.size
        # Cambiar a la nueva instancia de la aplicación
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Admin)
       
    """
    def iniciar_lectura(self, widget):
        print('iniciar_lectura')
        Config.set('input', 'wm_touch', '')
        self.main_app = SeleccionarLecturaApp()
        self.main_app.run()
    """

############################
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
#############################
class Administrador(RelativeLayout):
    def __init__(self, **kwargs):
        super(Administrador, self).__init__(**kwargs)
        self.selected_lectura_id = None  # Variable para almacenar el ID de la lectura seleccionada
        self.controlador=ControladorLecturas()
        self.gui()
        self.mostrar_lecturas()

    def mostrar_lecturas(self):
        lecturas=self.controlador.mostrar_lecturas_disponibles()
        # Crear un ScrollView para contener los botones de lectura
        scroll_view = ScrollView(size_hint=(1, 0.5), pos_hint={'x': 0, 'y': 0.3})
        layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Crear botones para mostrar las lecturas disponibles
        for lectura in lecturas:
            ID_Lecturas, nombre_lectura, tipo_lectura = lectura
            button_text = f"{nombre_lectura} ------ {tipo_lectura}"
            button = Button(text=button_text, size_hint_y=None, height=40)

            # Modificar el evento on_press para almacenar el ID de la lectura seleccionada
            button.bind(on_press=lambda instance, ID_Lecturas=ID_Lecturas: self.select_lectura(ID_Lecturas))
            layout.add_widget(button)

        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def select_lectura(self, lectura_id):
        # Almacenar el ID de la lectura seleccionada
        self.selected_lectura_id = lectura_id


    def show_notification(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message, size_hint_y=None, height=dp(40)))
        popup = Popup(title="Notificación", content=content, size_hint=(None, None), size=(300, 200))
        popup.open()

    def eliminar_lectura(self):
        print(self.selected_lectura_id)
        if self.selected_lectura_id:
            lectura= self.controlador.mostrar_lectura_nombre(self.selected_lectura_id)
            if lectura:
                nombre_lectura = lectura[0]
                # Mostrar la advertencia para confirmar la eliminación con el nombre de la lectura
                content = BoxLayout(orientation='vertical')
                content.add_widget(Label(text=f"¿Estás seguro de eliminar la lectura '{nombre_lectura}'?", size_hint_y=None, height=dp(40)))
                btn_layout = BoxLayout(size_hint_y=None, height=dp(40))
                cancel_button = Button(text='Cancelar', on_release=self.dismiss_popup)
                confirm_button = Button(text='Confirmar', on_release=lambda instance: self.confirm_delete(nombre_lectura))
                btn_layout.add_widget(cancel_button)
                btn_layout.add_widget(confirm_button)
                content.add_widget(btn_layout)
                self.popup = Popup(title="Confirmar Eliminación", content=content, size_hint=(None, None), size=(500, 200))
                self.popup.open()
            else:
                # Si no se encuentra la lectura, mostrar un mensaje de error
                self.show_error_popup("Por favor, selecciona una lectura antes de intentar eliminar.")
        else:
            # Si no se ha seleccionado ninguna lectura, mostrar un mensaje de error
            self.show_error_popup("Por favor, selecciona una lectura antes de intentar eliminar.")



    def confirm_delete(self, lectura_nombre):
        self.controlador.elimniar_lectura(lectura_nombre)
        # Mostrar notificación de eliminación exitosa
        self.show_notification(f"Lectura '{lectura_nombre}' eliminada exitosamente.")
        # Actualizar la vista
        self.clear_widgets()
        self.gui()
        self.mostrar_lecturas()
        # Cerrar la ventana emergente
        self.dismiss_popup()

    def dismiss_popup(self, instance=None):
        # Cerrar la ventana emergente
        if self.popup:
            self.popup.dismiss()

    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message, size_hint_y=None, height=dp(40)))
        btn_layout = BoxLayout(size_hint_y=None, height=dp(40))
        ok_button = Button(text='OK', on_release=self.dismiss_error_popup)
        btn_layout.add_widget(ok_button)
        content.add_widget(btn_layout)
        self.error_popup = Popup(title="Error", content=content, size_hint=(None, None), size=(300, 200))
        self.error_popup.open()

    def dismiss_error_popup(self, instance):
        self.error_popup.dismiss()


    def gui(self):
        self.agregar = Button(text="Agregar Lectura", pos_hint={'x': 0.0884956, 'y': 0.13}, size_hint=(0.383481, 0.05))
        self.agregar.bind(on_press=self.switch_to_add_lectura)
        self.add_widget(self.agregar)

        self.eliminar = Button(text="Eliminar Lectura", pos_hint={'x': 0.530973, 'y': 0.13}, size_hint=(0.383481, 0.05))
        self.eliminar.bind(on_press=lambda instance: self.eliminar_lectura())
        self.add_widget(self.eliminar)

        self.label = Label(text="Administrador de Lecturas", halign='center', pos_hint={'x': 0.100000, 'y': 0.8},
                           size_hint=(0.843658, 0.303333), font_size=26, color=[0, 0, 0, 1])
        self.add_widget(self.label)

        self.label2 = Label(text="Lecturas Disponibles", halign='center', pos_hint={'x': 0.100000, 'y': 0.7},
                           size_hint=(0.843658, 0.303333), font_size=24, color=[0, 0, 0, 1])
        self.add_widget(self.label2)

        self.home_button = Button(text="HOME", pos_hint={'x': 0.0294985, 'y': 0.9}, size_hint=(0.2, 0.03))
        self.home_button.bind(on_press=self.ir_a_home)
        self.add_widget(self.home_button)

    def switch_to_add_lectura(self, instance):
        self.parent.parent.current = 'agregar_lectura'

    def ir_a_home(self, instance):
        # Buscar el widget padre de tipo ScreenManager
        screen_manager = self.parent.parent
        if isinstance(screen_manager, ScreenManager):
            # Cambiar a la pantalla de inicio ('Home')
            screen_manager.current = 'Home'

