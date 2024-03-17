from conexion import establecer_conexion
import PyPDF2
import sqlite3
import os
class Usuario:
    def __init__(self, nombre_usuario, contraseña):
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.conn = establecer_conexion()
        self.cursor = self.conn.cursor()
    def registrar_Usuario(self):
        try:
            self.conn= establecer_conexion()
            self.cursor.execute("INSERT INTO Usuario (Nombre_Usuario, Contraseña) VALUES (?, ?)", (self.nombre_usuario, self.contraseña))
            self.conn.commit()
            print("Cuenta creada exitosamente")
            self.conn.close()
            return True
        except sqlite3.IntegrityError:
            print("El usuario ya existe")
            self.conn.close()
            return False
            
        except sqlite3.Error as e:
            print("Error al crear la cuenta:", e)
            self.conn.close()
            return False
    def consultar_Usuario(self):
        self.cursor.execute("SELECT * FROM Usuario WHERE Nombre_Usuario=? AND Contraseña=?", ( self.nombre_usuario, self.contraseña))
        user = self.cursor.fetchone()
        if user:
            print("Inicio de sesión exitoso")
            return True
        else:
            print("Nombre de usuario o contraseña incorrectos")
            self.conn.commit()
            #self.conn.close()
            return False
    def __del__(self):
        self.conn.close()    
class Lectura:
    def __init__(self, nombre, tipo_lectura,ubicacion):
        self.nombre = nombre
        self.tipo_lectura = tipo_lectura
        self.ubicacion=ubicacion
    def consultar_por_tipo(self,tipo_de_lectura):
        lecturas = []
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT Nombre_Lectura FROM Lecturas WHERE Tipo_Lectura = ?", (tipo_de_lectura,))
                rows = cursor.fetchall()
                for row in rows:
                   
                    lecturas.append(str(row[0]))   
            except sqlite3.Error as e:
                print("Error al ejecutar la consulta:", e)
            finally:
                self.conn.close()
        else:
            print("No se pudo obtener la conexión a la base de datos.")
        return lecturas
    def consultar_por_nombre(self,nombre_lectura):
        
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT Ubicacion_lectura FROM Lecturas WHERE Nombre_Lectura = ?", (nombre_lectura,))
                rows = cursor.fetchall()
                for row in rows:
                    return str(row[0])  
            except sqlite3.Error as e:
                print("Error al ejecutar la consulta:", e)
            finally:
                self.conn.close()
        else:
            print("No se pudo obtener la conexión a la base de datos.")
        return ""

    def eliminar_lectura(self):
        self.cursor.execute("DELETE FROM Lecturas WHERE ID_Lecturas=?", (self.selected_lectura_id,))
        self.conn.commit()
        self.conn.close()