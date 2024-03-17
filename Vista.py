from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from Controlador import ControladorCuentas
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

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
# Vista
class VentanaIniciarSesion(BoxLayout):
    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = [50, 20]
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
        ventana_Home = Home()  # Crear una instancia de HOME
        ventana_Home.size = Window.size  # Establecer el tamaño de la ventana Home igual al tamaño de la ventana principal
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Home)
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
        #button1.bind(on_press=self.ir_a_Administrador)
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
    


    """
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
    """