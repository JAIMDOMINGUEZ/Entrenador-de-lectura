import sqlite3
def establecer_conexion():
        conn = None
        try:
            conn = sqlite3.connect('EntrenadorLectura.db')
            return conn
        except sqlite3.Error as e:
            print("Error al conectar a la base de datos:", e)
            return None