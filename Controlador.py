from Modelo import Usuario, Lectura 
from kivy.app import App
import os
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
    def mostrar_lecturas_disponibles(self,id_usuario):
        return self.modelo.consultar_lecturas(id_usuario)
    def mostrar_lectura_id(self,nombre_lectura,id_usuario):
        return self.modelo.consultar_por_id(nombre_lectura,id_usuario)
    def eliminar_lectura(self,nombre_lectura,id_usuario):
        return self.modelo.eliminar_lectura(nombre_lectura,id_usuario)
    def es_valido(self,file_path):
        # Obtener la extensión del archivo
        file_extension = os.path.splitext(file_path)[1].lower()
        # Comprobar si la extensión es .pdf
        if file_extension == '.pdf':
            return True
        else:
            return False
    def salvar_archivo(self,id_usuario,nombre_lectura,tipo_lectura,selected_pdf):
        # Obtener la ubicación del archivo actual
            current_path = os.path.dirname(os.path.realpath(__file__))
            # Crear la ruta a la subcarpeta "lecturas" relativa a la ubicación actual del archivo
            lecturas_path = os.path.join(current_path, "lecturas")
            # Si la subcarpeta no existe, créala
            if not os.path.exists(lecturas_path):
                os.makedirs(lecturas_path)
            # Crear una copia del archivo PDF en la subcarpeta "lecturas"
            new_pdf_path = os.path.join(lecturas_path, os.path.basename(selected_pdf))
            with open(selected_pdf, 'rb') as f_in:
                with open(new_pdf_path, 'wb') as f_out:
                    f_out.write(f_in.read())

            # Guardar la ubicación de la copia del archivo PDF de manera relativa
            relative_pdf_path = os.path.relpath(new_pdf_path, current_path)
            return self.modelo.guardar_lectura(id_usuario,nombre_lectura,tipo_lectura,relative_pdf_path)

    
   
    
    