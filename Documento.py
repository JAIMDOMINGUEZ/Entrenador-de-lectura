import PyPDF2
import os
class Documento:
    def __init__(self,ubicacion):
        self.ubicacion= ubicacion
    def separar_Documento(self):
        try:
            # Abrir el archivo PDF
            with open(self.ubicacion, 'rb') as archivo:
                # Crear un objeto de lectura de PDF
                lector_pdf = PyPDF2.PdfReader(self.ubicacion)
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
    def verificar_existencia_pdf(self):
        if os.path.exists(self.ubicacion):
            return True
        else:
            return False