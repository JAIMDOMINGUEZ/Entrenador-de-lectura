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
        modelo=Usuario(Nombre_Usuario,Contraseña)
        if modelo.consultar_Usuario():
            #self.ir_a_Home()  # Redirige a HOME después de iniciar sesión
            return True
        else:
            return False
    
    def verificar_usuario(self, Nombre_Usuario):
        return self.modelo.verificar_usuario(Nombre_Usuario)
       
    

    
   
    
    