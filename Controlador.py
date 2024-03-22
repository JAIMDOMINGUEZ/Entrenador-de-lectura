from Modelo import Usuario, Lectura 
from kivy.app import App
import os
from Documento import Documento
class ControladorCuentas:
    def __init__(self):
        pass

    def crear_cuenta(Nombre_Usuario,Contraseña):

        modelo = Usuario(Nombre_Usuario.rstrip(),Contraseña.rstrip())
        if modelo.registrar_Usuario():
            #self.ir_a_Home()  # Redirige a HOME después de crear la cuenta
            return True
        else:
            return False
    def iniciar_sesion(self, Nombre_Usuario, Contraseña):
        modelo=Usuario(Nombre_Usuario.rstrip(),Contraseña.rstrip())
        if modelo.consultar_Usuario():
            #self.ir_a_Home()  # Redirige a HOME después de iniciar sesión
            return True
        else:
            return False
    
    def verificar_usuario(self, nombre_usuario):
        return self.modelo.verificar_usuario(nombre_usuario.rstrip())
    def obtener_id_usuario(self,nombre_usuario,contraseña):
        modelo=Usuario(nombre_usuario.rstrip(),contraseña.rstrip())
        return modelo.obtener_id_usuario(nombre_usuario)
    

class ControladorLecturas:
    def __init__(self):
        self.modelo=Lectura("","","")
    def mostrar_lecturas_disponibles(self,id_usuario):
        return self.modelo.consultar_lecturas(id_usuario)
    def mostrar_lectura_id(self,nombre_lectura,id_usuario):
        return self.modelo.consultar_por_id(nombre_lectura,id_usuario)
    def eliminar_lectura(self,nombre_lectura,id_usuario):
        return self.modelo.eliminar_lectura(nombre_lectura,id_usuario) 
           
    def es_valido(self,file_path):
        self.doc=Documento(file_path)
        return self.doc.validar_documento()
    def salvar_archivo(self,id_usuario,nombre_lectura,tipo_lectura,selected_pdf):
            self.doc= Documento(nombre_lectura)
            relative_pdf_path = self.doc.salvar_archivo(id_usuario,nombre_lectura,tipo_lectura,selected_pdf)
            return self.modelo.guardar_lectura(id_usuario,nombre_lectura,tipo_lectura,relative_pdf_path)

    def mostar_lectura_tipo(self,id_usuario,tipo):
        return self.modelo.consultar_por_tipo(id_usuario,tipo)
    def mostar_lectura_nombre(self,id_usuario,nombre):
        return self.modelo.consultar_ubicacion(id_usuario,nombre)
    def archivo_existe(self,archivo):
        self.doc=Documento(archivo)
        return self.doc.verificar_existencia_pdf()
    def dividir_documento(self,archivo):
        self.doc=Documento(archivo)
        return self.doc.separar_pdf()
    """
    def eliminar_archivo(self,nombre_lectura,id_usuario):
        ubicacion=self.modelo.consultar_ubicacion(id_usuario,nombre_lectura)
        print("ubucacuin")
        print(ubicacion)
        self.doc=Documento(ubicacion)
        return self.doc.eliminar_archivo(ubicacion)
    """