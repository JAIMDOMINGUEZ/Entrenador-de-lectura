import os
import sqlite3
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from Home import Home


# Modelo
class GestorCuentas:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Usuario (
                                    ID_Usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                                    Nombre_Usuario TEXT NOT NULL UNIQUE,
                                    Contraseña TEXT NOT NULL
                                )''')
        self.conn.commit()
    
    def crear_cuenta(self, Nombre_Usuario, Contraseña):
        try:
            self.cursor.execute("INSERT INTO Usuario (Nombre_Usuario, Contraseña) VALUES (?, ?)", (Nombre_Usuario, Contraseña))
            self.conn.commit()
            print("Cuenta creada exitosamente")
            return True
        except sqlite3.IntegrityError:
            print("El usuario ya existe")
            return False
        except sqlite3.Error as e:
            print("Error al crear la cuenta:", e)
            return False
    
    def iniciar_sesion(self, Nombre_Usuario, Contraseña):
        self.cursor.execute("SELECT * FROM Usuario WHERE Nombre_Usuario=? AND Contraseña=?", (Nombre_Usuario, Contraseña))
        user = self.cursor.fetchone()
        if user:
            print("Inicio de sesión exitoso")
            return True
        else:
            print("Nombre de usuario o contraseña incorrectos")
            return False
    
    def verificar_usuario(self, Nombre_Usuario):
        self.cursor.execute("SELECT * FROM Usuario WHERE Nombre_Usuario=?", (Nombre_Usuario,))
        user = self.cursor.fetchone()
        if user:
            return True
        else:
            return False
    
    def __del__(self):
        self.conn.close()


# Vista
class VentanaCrearCuenta(BoxLayout):
    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = [50, 20]
        self.controlador = controlador
        
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
        self.login_button.bind(on_press=self.controlador.ir_a_inicio_sesion)
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
        
        if self.controlador.crear_cuenta(nombre_usuario, contraseña):
            self.mostrar_mensaje_cuenta_creada()
        else:
            self.mostrar_mensaje_usuario_existente()
    
    def mostrar_mensaje_cuenta_creada(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Cuenta creada con éxito", font_size=20))
        popup = Popup(title='Éxito', content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()
    
    def ir_a_inicio(self, instance):
        ventana_iniciar_sesion = VentanaIniciarSesion(self.controlador)
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_iniciar_sesion)
    
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


# Vista
# Vista
class VentanaIniciarSesion(BoxLayout):
    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = [50, 20]
        self.controlador = controlador
        
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
        self.create_account_button.bind(on_press=self.controlador.ir_a_crear_cuenta)
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



# Controlador
class ControladorCuentas:
    def __init__(self, db_path):
        self.modelo = GestorCuentas(db_path)

    def crear_cuenta(self, Nombre_Usuario, Contraseña):
        if self.modelo.crear_cuenta(Nombre_Usuario, Contraseña):
            self.ir_a_Home()  # Redirige a HOME después de crear la cuenta
            return True
        else:
            return False

    def iniciar_sesion(self, Nombre_Usuario, Contraseña):
        if self.modelo.iniciar_sesion(Nombre_Usuario, Contraseña):
            self.ir_a_Home()  # Redirige a HOME después de iniciar sesión
            return True
        else:
            return False

    def verificar_usuario(self, Nombre_Usuario):
        return self.modelo.verificar_usuario(Nombre_Usuario)

    def ir_a_crear_cuenta(self):
        ventana_crea_cuenta = VentanaCrearCuenta(self)
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_crea_cuenta)


    def ir_a_inicio_sesion(self, instance):
        ventana_inicio_sesion = VentanaIniciarSesion(self)
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_inicio_sesion)
    
    def ir_a_Home(self):
        ventana_Home = Home()  # Crear una instancia de HOME
        ventana_Home.size = Window.size  # Establecer el tamaño de la ventana Home igual al tamaño de la ventana principal
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Home)



# Aplicación
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
        self.controlador = ControladorCuentas('EntrenadorLectura.db')
        ventana_crea_cuenta = VentanaCrearCuenta(self.controlador)
        root.add_widget(ventana_crea_cuenta)
        return root

    def on_stop(self):
        # Cerrar la conexión de la base de datos al salir de la aplicación
        self.root.controlador.modelo.__del__()

if __name__ == "__main__":
    if not os.path.exists('EntrenadorLectura.db'):
        with open('EntrenadorLectura.db', 'w'):
            pass
    CreaCuentaApp().run()
