from Modelo import Usuario, Lectura 
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
    
    def verificar_usuario(self, nombre_usuario):
        return self.modelo.verificar_usuario(nombre_usuario)
    def obtener_id_usuario(self,nombre_usuario,contraseña):
        modelo=Usuario(nombre_usuario,contraseña)
        return modelo.obtener_id_usuario(nombre_usuario)


class ControladorLecturas:
    def __init__(self):
        self.modelo=Lectura("","","")
    def mostrar_lecturas_disponibles(self):
        return self.modelo.consultar_lecturas()
    def mostrar_lectura_nombre(self,nombre_lectura):
        return self.modelo.consultar_por_nombre(nombre_lectura)
    def elimniar_lectura(self):
        pass
    

    
   
    
    