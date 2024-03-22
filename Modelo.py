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
    def consultar_por_tipo(self,id_usuario,tipo_de_lectura):
        self.connexion=establecer_conexion()
        lecturas = []
        if self.connexion:
            try:
                cursor = self.connexion.cursor()
                cursor.execute("SELECT Nombre_Lectura FROM Lecturas WHERE Tipo_Lectura = ? AND ID_Lecturas IN (SELECT ID_Lectura FROM Cliente_Lecturas WHERE ID_Usuario = ?)", 
                           (tipo_de_lectura, id_usuario))
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
    def consultar_por_id(self,id_lectura,id_usuario):
        self.connexion=establecer_conexion()
        if self.connexion:
            try:
                cursor = self.connexion.cursor()
                cursor.execute("SELECT l.Nombre_Lectura FROM Lecturas l JOIN Cliente_Lecturas cl ON l.ID_Lecturas = cl.ID_Lectura WHERE l.ID_Lecturas = ? AND cl.ID_Usuario = ?", (id_lectura, id_usuario))
                row = cursor.fetchall()
                return row[0]
            except sqlite3.Error as e:
                print("Error al ejecutar la consulta de id:", e)
            finally:
                self.connexion.close()
        else:
            print("No se pudo obtener la conexión a la base de datos.")
        return ""

    def eliminar_lectura(self, nombre_lectura,id_usuario):
        self.connexion = establecer_conexion()
        if self.connexion:
            try:
                self.cursor = self.connexion.cursor()
                self.cursor.execute("DELETE FROM Cliente_Lecturas WHERE ID_Lectura IN ( SELECT ID_Lecturas FROM Lecturas WHERE Nombre_Lectura = ?)AND ID_Usuario = ?", (nombre_lectura,id_usuario))
                self.cursor.execute("DELETE FROM Lecturas WHERE Nombre_Lectura = ?", (nombre_lectura,))
                self.connexion.commit()  # Es importante hacer commit después de ejecutar la eliminación
                print("La lectura se ha eliminado correctamente.")
                return True
            except sqlite3.Error as e:
                print("Error al ejecutar la consulta de eliminacion:", e)
            finally:
                self.connexion.close()
        else:
            print("No se pudo obtener la conexión a la base de datos.")
        return False

    def consultar_lecturas(self, id_usuario):
        lecturas = []
        
        self.connexion=establecer_conexion()
        if self.connexion:
            try:
                self.cursor.execute("SELECT l.* FROM Lecturas l JOIN Cliente_Lecturas cl ON l.ID_Lecturas = cl.ID_Lectura WHERE cl.ID_Usuario = ?",(id_usuario,))
                rows = self.cursor.fetchall()
                for row in rows:
                    lecturas.append(row)   
            except sqlite3.Error as e:
                print("Error al ejecutar la consulta lecturas:", e)
            finally:
                self.connexion.close()
        else:
            print("No se pudo obtener la conexión a la base de datos.")
        return lecturas
    def guardar_lectura(self, id_usuario, nombre_lectura, tipo_lectura, ubicacion):
        self.connexion = establecer_conexion()
        if self.connexion:
            try:
                cursor = self.connexion.cursor()
                # Insertar la lectura en la tabla Lecturas
                cursor.execute("INSERT INTO Lecturas (Nombre_Lectura, Tipo_Lectura, Ubicacion_Lectura) VALUES (?, ?, ?)",
                               (nombre_lectura, tipo_lectura, ubicacion))
                # Obtener el ID de la última fila insertada
                last_row_id = cursor.lastrowid
                # Insertar el ID de la lectura y el ID del usuario en la tabla Cliente_Lecturas
                cursor.execute("INSERT INTO Cliente_Lecturas (ID_Usuario, ID_Lectura) VALUES (?, ?)",
                               (id_usuario, last_row_id))
                self.connexion.commit()
                return True
            except sqlite3.Error as e:
                print("Error al ejecutar la consulta:", e)
            finally:
                self.connexion.close()
        else:
            print("No se pudo obtener la conexión a la base de datos.")
        return False
    
    def consultar_ubicacion(self,id_usuario,nombre_lectura):
        self.connexion= establecer_conexion()
        ubicacion = "" 
        if self.connexion:
            try:
                cursor = self.connexion.cursor()
                # Modificamos la consulta SQL para incluir el criterio de id_usuario
                cursor.execute("SELECT l.Ubicacion_lectura FROM Lecturas l JOIN Cliente_Lecturas cl ON l.ID_Lecturas = cl.ID_Lectura WHERE l.Nombre_Lectura = ? AND cl.ID_Usuario = ?", 
                               (nombre_lectura, id_usuario))
                row = cursor.fetchone()  # Obtenemos solo una fila
                if row:
                    ubicacion = str(row[0])  # Si se encontró una fila, obtenemos la ubicación
            except sqlite3.Error as e:
                print("Error al ejecutar la consulta de ubucacion:", e)
            finally:
                self.connexion.close()
        else:
            print("No se pudo obtener la conexión a la base de datos.")
        return ubicacion