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
            self.cursor.execute("INSERT INTO Usuario (Nombre_Usuario, Contraseña) VALUES (?, ?)", (self.nombre_usuario, self.contraseña))
            self.conn.commit()
            print("Cuenta creada exitosamente")
            return True
        except sqlite3.IntegrityError:
            print("El usuario ya existe")
            return False
        except sqlite3.Error as e:
            print("Error al crear la cuenta:", e)
            return False

    def consultar_Usuario(self):
        try:
            self.cursor.execute("SELECT * FROM Usuario WHERE Nombre_Usuario=? AND Contraseña=?", (self.nombre_usuario, self.contraseña))
            user = self.cursor.fetchone()
            if user:
                print("Inicio de sesión exitoso")
                return True
            else:
                print("Nombre de usuario o contraseña incorrectos")
                return False
        finally:
            self.conn.close()
    def obtener_id_usuario(self, nombre_usuario):
        try:
            self.cursor.execute("SELECT ID_Usuario FROM Usuario WHERE Nombre_Usuario=?", (nombre_usuario,))
            id_usuario = self.cursor.fetchone()  # Obtenemos la fila del resultado
            if id_usuario:
                id_usuario = id_usuario[0]  # Extraemos el ID de usuario de la tupla
                print("ID de usuario encontrado:", id_usuario)
                return id_usuario
            else:
                print("No se encontró ningún usuario con el nombre proporcionado.")
                return None
        except Exception as e:
            print("Error al obtener el ID de usuario:", e)
            return None
        finally:
            self.conn.close()

    def __del__(self):
        self.conn.close()

class Lectura:
    def __init__(self, nombre, tipo_lectura,ubicacion):
        self.nombre = nombre
        self.tipo_lectura = tipo_lectura
        self.ubicacion=ubicacion
        self.connexion = establecer_conexion()
        self.cursor = self.connexion.cursor()
    def consultar_por_tipo(self,tipo_de_lectura):
        lecturas = []
        if self.connexion:
            try:
                cursor = self.connexion.cursor()
                cursor.execute("SELECT Nombre_Lectura FROM Lecturas WHERE Tipo_Lectura = ?", (tipo_de_lectura,))
                rows = cursor.fetchall()
                for row in rows:
                   
                    lecturas.append(str(row[0]))   
            except sqlite3.Error as e:
                print("Error al ejecutar la consulta:", e)
            finally:
                self.connexion.close()
        else:
            print("No se pudo obtener la conexión a la base de datos.")
        return lecturas
    def consultar_por_nombre(self,nombre_lectura):
        self.connexion=establecer_conexion()
        if self.connexion:
            try:
                cursor = self.connexion.cursor()
                cursor.execute("SELECT Nombre_Lectura FROM Lecturas WHERE ID_Lecturas = ?", (nombre_lectura,))
                row = cursor.fetchall()
                
                return row[0]
            except sqlite3.Error as e:
                print("Error al ejecutar la consulta:", e)
            finally:
                self.connexion.close()
        else:
            print("No se pudo obtener la conexión a la base de datos.")
        return ""

    def eliminar_lectura(self,nombre_lectura):
        self.cursor.execute("DELETE FROM Lecturas WHERE ID_Lecturas=?", (nombre_lectura,))
        self.connexion.close()
    def consultar_lecturas(self):
        lecturas = []
        self.connexion=establecer_conexion()
        if self.connexion:
            try:
                self.cursor.execute("SELECT ID_Lecturas, Nombre_Lectura, Tipo_Lectura FROM Lecturas")
                rows = self.cursor.fetchall()
                for row in rows:
                   
                    lecturas.append(row)   
            except sqlite3.Error as e:
                print("Error al ejecutar la consulta:", e)
            finally:
                self.connexion.close()
        else:
            print("No se pudo obtener la conexión a la base de datos.")
        return lecturas