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
    def registrar_Usuario(self, Nombre_Usuario, Contraseña):
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
    def consultar_Usuario(self, Nombre_Usuario, Contraseña):
        self.cursor.execute("SELECT * FROM Usuario WHERE Nombre_Usuario=? AND Contraseña=?", (Nombre_Usuario, Contraseña))
        user = self.cursor.fetchone()
        if user:
            print("Inicio de sesión exitoso")
            return True
        else:
            print("Nombre de usuario o contraseña incorrectos")
            return False
class Lectura:
    def __init__(self, nombre, tipo_lectura,ubicacion):
        self.nombre = nombre
        self.tipo_lectura = tipo_lectura
        self.ubicacion=ubicacion
    def consultar_por_tipo(tipo_de_lectura):
        lecturas = []
        conn = establecer_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Nombre_Lectura FROM Lecturas WHERE Tipo_Lectura = ?", (tipo_de_lectura,))
                rows = cursor.fetchall()
                for row in rows:
                   
                    lecturas.append(str(row[0]))   
            except sqlite3.Error as e:
                print("Error al ejecutar la consulta:", e)
            finally:
                conn.close()
        else:
            print("No se pudo obtener la conexión a la base de datos.")
        return lecturas
    def consultar_por_nombre(nombre_lectura):
        conn = establecer_conexion()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT Ubicacion_lectura FROM Lecturas WHERE Nombre_Lectura = ?", (nombre_lectura,))
                rows = cursor.fetchall()
                for row in rows:
                    return str(row[0])  
            except sqlite3.Error as e:
                print("Error al ejecutar la consulta:", e)
            finally:
                conn.close()
        else:
            print("No se pudo obtener la conexión a la base de datos.")
        return ""

    def verificar_existencia_pdf(archivo):
        if os.path.exists(archivo):
            return True
        else:
            return False
    def separar_pdf(nombre_archivo):
        try:
            # Abrir el archivo PDF
            with open(nombre_archivo, 'rb') as archivo:
                # Crear un objeto de lectura de PDF
                lector_pdf = PyPDF2.PdfReader(archivo)
                # Inicializar una lista para almacenar los párrafos
                parrafos = []
                # Iterar sobre cada página del PDF
                for pagina_num in range(len(lector_pdf.pages)):
                    # Extraer el texto de la página actual
                    texto_pagina = lector_pdf.pages[pagina_num].extract_text()
                    # Separar el texto por párrafos
                    parrafos_pagina = texto_pagina.split('\n\n')  # Se asume que los párrafos están separados por dos saltos de línea
                    # Agregar los párrafos de la página a la lista general de párrafos
                    parrafos.extend(parrafos_pagina)
                return parrafos
        except FileNotFoundError:
            print("El archivo especificado no fue encontrado.")
            return None
        except Exception as e:
            print("Ocurrió un error:", e)
            return None