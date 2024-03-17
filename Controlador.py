from Modelo import Usuario  
from kivy.app import App
class ControladorCuentas:
    def __init__(self):
        pass

    def crear_cuenta(Nombre_Usuario,Contraseña):
        modelo = Usuario(Nombre_Usuario,Contraseña)
        if modelo.registrar_Usuario():
            #self.ir_a_Home()  # Redirige a HOME después de crear la cuenta
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

    def ir_a_Home(self):
        ventana_Home = Home()  # Crear una instancia de HOME
        ventana_Home.size = Window.size  # Establecer el tamaño de la ventana Home igual al tamaño de la ventana principal
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Home)
    
    def ir_a_inicio_sesion(self, instance):
        ventana_inicio_sesion = VentanaIniciarSesion(self)
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_inicio_sesion)
    
    