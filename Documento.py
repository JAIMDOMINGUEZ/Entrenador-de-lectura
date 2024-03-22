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
    def validar_documento(self):
        file_extension = os.path.splitext(self.ubicacion)[1].lower()
        # Comprobar si la extensión es .pdf
        if file_extension == '.pdf':
            return True
        else:
            return False
    def separar_pdf(self):
        try:
            # Abrir el archivo PDF
            with open(self.ubicacion, 'rb') as archivo:
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
    def salvar_archivo(self,id_usuario,nombre_lectura,tipo_lectura,selected_pdf):
        # Obtener la ubicación del archivo actual
            current_path = os.path.dirname(os.path.realpath(__file__))
            # Crear la ruta a la subcarpeta "lecturas" relativa a la ubicación actual del archivo
            ubicacion="lecturas/"+str(id_usuario)
            lecturas_path = os.path.join(current_path, ubicacion)
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
            return relative_pdf_path
    def eliminar_archivo(self,ubicacion):
        try:
            os.remove(ubicacion)
            print(f"El archivo {ubicacion} ha sido eliminado.")
            return True
        except OSError as e:
            print(f"No se pudo eliminar el archivo {ubicacion}: {e}")
            return False