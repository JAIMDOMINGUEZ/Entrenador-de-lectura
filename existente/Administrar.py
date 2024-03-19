import os
import sqlite3
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout



class RootLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)

        with self.canvas.before:
            # Establecer el color de fondo como blanco
            Color(1, 1, 1, 1) 
            # Crear un rectángulo que cubra toda la pantalla
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # Escuchar cambios en el tamaño y la posición para actualizar el rectángulo
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        # Actualizar el tamaño y la posición del rectángulo para que cubra toda la pantalla
        self.rect.pos = self.pos
        self.rect.size = self.size

class Administrador(RelativeLayout):
    def __init__(self, **kwargs):
        super(Administrador, self).__init__(**kwargs)
        self.selected_lectura_id = None  # Variable para almacenar el ID de la lectura seleccionada
        self.gui()
        self.mostrar_lecturas()

    def mostrar_lecturas(self):
        # Conectarse a la base de datos SQLite
        conn = sqlite3.connect('EntrenadorLectura.db')
        c = conn.cursor()

        # Seleccionar todas las lecturas disponibles
        c.execute("SELECT ID_Lecturas, Nombre_Lectura, Tipo_Lectura FROM Lecturas")
        lecturas = c.fetchall()
        conn.close()

        # Crear un ScrollView para contener los botones de lectura
        scroll_view = ScrollView(size_hint=(1, 0.5), pos_hint={'x': 0, 'y': 0.3})
        layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Crear botones para mostrar las lecturas disponibles
        for lectura in lecturas:
            ID_Lecturas, nombre_lectura, tipo_lectura = lectura
            button_text = f"{nombre_lectura} ------ {tipo_lectura}"
            button = Button(text=button_text, size_hint_y=None, height=40)

            # Modificar el evento on_press para almacenar el ID de la lectura seleccionada
            button.bind(on_press=lambda instance, ID_Lecturas=ID_Lecturas: self.select_lectura(ID_Lecturas))
            layout.add_widget(button)

        scroll_view.add_widget(layout)
        self.add_widget(scroll_view)

    def select_lectura(self, lectura_id):
        # Almacenar el ID de la lectura seleccionada
        self.selected_lectura_id = lectura_id


    def show_notification(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message, size_hint_y=None, height=dp(40)))
        popup = Popup(title="Notificación", content=content, size_hint=(None, None), size=(300, 200))
        popup.open()

    def eliminar_lectura(self):
        if self.selected_lectura_id:
            # Obtener el nombre de la lectura seleccionada
            conn = sqlite3.connect('EntrenadorLectura.db')
            c = conn.cursor()
            c.execute("SELECT Nombre_Lectura FROM Lecturas WHERE ID_Lecturas=?", (self.selected_lectura_id,))
            lectura = c.fetchone()
            conn.close()

            if lectura:
                lectura_nombre = lectura[0]
                # Mostrar la advertencia para confirmar la eliminación con el nombre de la lectura
                content = BoxLayout(orientation='vertical')
                content.add_widget(Label(text=f"¿Estás seguro de eliminar la lectura '{lectura_nombre}'?", size_hint_y=None, height=dp(40)))
                btn_layout = BoxLayout(size_hint_y=None, height=dp(40))
                cancel_button = Button(text='Cancelar', on_release=self.dismiss_popup)
                confirm_button = Button(text='Confirmar', on_release=lambda instance: self.confirm_delete(lectura_nombre))
                btn_layout.add_widget(cancel_button)
                btn_layout.add_widget(confirm_button)
                content.add_widget(btn_layout)
                self.popup = Popup(title="Confirmar Eliminación", content=content, size_hint=(None, None), size=(500, 200))
                self.popup.open()
            else:
                # Si no se encuentra la lectura, mostrar un mensaje de error
                self.show_error_popup("Por favor, selecciona una lectura antes de intentar eliminar.")
        else:
            # Si no se ha seleccionado ninguna lectura, mostrar un mensaje de error
            self.show_error_popup("Por favor, selecciona una lectura antes de intentar eliminar.")



    def confirm_delete(self, lectura_nombre):
        # Eliminar la lectura seleccionada de la base de datos
        conn = sqlite3.connect('EntrenadorLectura.db')
        c = conn.cursor()
        c.execute("DELETE FROM Lecturas WHERE ID_Lecturas=?", (self.selected_lectura_id,))
        conn.commit()
        conn.close()

        # Mostrar notificación de eliminación exitosa
        self.show_notification(f"Lectura '{lectura_nombre}' eliminada exitosamente.")

        # Actualizar la vista
        self.clear_widgets()
        self.gui()
        self.mostrar_lecturas()

        # Cerrar la ventana emergente
        self.dismiss_popup()

    def dismiss_popup(self, instance=None):
        # Cerrar la ventana emergente
        if self.popup:
            self.popup.dismiss()

    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message, size_hint_y=None, height=dp(40)))
        btn_layout = BoxLayout(size_hint_y=None, height=dp(40))
        ok_button = Button(text='OK', on_release=self.dismiss_error_popup)
        btn_layout.add_widget(ok_button)
        content.add_widget(btn_layout)
        self.error_popup = Popup(title="Error", content=content, size_hint=(None, None), size=(300, 200))
        self.error_popup.open()

    def dismiss_error_popup(self, instance):
        self.error_popup.dismiss()


    def gui(self):
        self.agregar = Button(text="Agregar Lectura", pos_hint={'x': 0.0884956, 'y': 0.13}, size_hint=(0.383481, 0.05))
        self.agregar.bind(on_press=self.switch_to_add_lectura)
        self.add_widget(self.agregar)

        self.eliminar = Button(text="Eliminar Lectura", pos_hint={'x': 0.530973, 'y': 0.13}, size_hint=(0.383481, 0.05))
        self.eliminar.bind(on_press=lambda instance: self.eliminar_lectura())
        self.add_widget(self.eliminar)

        self.label = Label(text="Administrador de Lecturas", halign='center', pos_hint={'x': 0.100000, 'y': 0.8},
                           size_hint=(0.843658, 0.303333), font_size=26, color=[0, 0, 0, 1])
        self.add_widget(self.label)

        self.label2 = Label(text="Lecturas Disponibles", halign='center', pos_hint={'x': 0.100000, 'y': 0.7},
                           size_hint=(0.843658, 0.303333), font_size=24, color=[0, 0, 0, 1])
        self.add_widget(self.label2)

        self.home_button = Button(text="HOME", pos_hint={'x': 0.0294985, 'y': 0.9}, size_hint=(0.2, 0.03))
        self.home_button.bind(on_press=self.ir_a_home)
        self.add_widget(self.home_button)

    def switch_to_add_lectura(self, instance):
        self.parent.parent.current = 'agregar_lectura'

    def ir_a_home(self, instance):
        # Buscar el widget padre de tipo ScreenManager
        screen_manager = self.parent.parent
        if isinstance(screen_manager, ScreenManager):
            # Cambiar a la pantalla de inicio ('Home')
            screen_manager.current = 'Home'

class Agregar_Lectura(RelativeLayout):
    def __init__(self, **kwargs):
        super(Agregar_Lectura, self).__init__(**kwargs)
        self.selected_pdf = None  # Variable para guardar la ubicación del PDF seleccionado
        self.gui()

    def gui(self):

        self.label = Label(text="Agregar Lectura", halign='center', pos_hint={'x': 0.100000, 'y': 0.8},
                           size_hint=(0.843658, 0.303333), font_size=26, color=[0, 0, 0, 1])
        self.add_widget(self.label)

        self.nombre_label = Label(text="Nombre Lectura", halign='center', pos_hint={'x': 0.176991, 'y': 0.8},
                                  size_hint=(0.678466, 0.0866667), font_size=20, color=[0, 0, 0, 1])
        self.add_widget(self.nombre_label)

        self.text_input = TextInput(multiline=False, halign='center', pos_hint={'x': 0.147493, 'y': 0.7},
                                    size_hint=(0.678466, 0.05), foreground_color=[0, 0, 0, 1],
                                    background_color=[1, 1, 1, 1])
        self.add_widget(self.text_input)

        self.tipo_label = Label(text="Tipo Lectura", halign='center', pos_hint={'x': 0.235988, 'y': 0.6},
                                size_hint=(0.501475, 0.07), font_size=20, color=[0, 0, 0, 1])
        self.add_widget(self.tipo_label)

        self.tipo_lectura_spinner = Spinner(text="Cuento", values=("Cuento", "Novela", "Articulo", ""),
                                            pos_hint={'x': 0.324484, 'y': 0.55},
                                            size_hint=(0.324484, 0.0366667), font_size=20, color=[1, 1, 1, 1])
        self.add_widget(self.tipo_lectura_spinner)

        self.archivo_label = Label(text="Archivo", halign='center', pos_hint={'x': 0.3, 'y': 0.45},
                                   size_hint=(0.383481, 0.07), font_size=20, color=[0, 0, 0, 1])
        self.add_widget(self.archivo_label)

        self.buscar_button = Button(text="Buscar Archivo", pos_hint={'x': 0.353982, 'y': 0.40},
                                    size_hint=(0.265487, 0.0366667), font_size=20, color=[1, 1, 1, 1])
        self.buscar_button.bind(on_press=self.show_file_chooser)
        self.add_widget(self.buscar_button)

        self.cancelar_button = Button(text="Cancelar", pos_hint={'x': 0.117994, 'y': 0.113333},
                                      size_hint=(0.265487, 0.05), font_size=20)
        self.cancelar_button.bind(on_press=self.switch_to_administrador)
        self.add_widget(self.cancelar_button)

        self.subir_lectura_button = Button(text="Subir Lectura", pos_hint={'x': 0.619469, 'y': 0.113333},
                                           size_hint=(0.265487, 0.05), font_size=20)
        self.subir_lectura_button.bind(on_press=self.confirm_upload)
        self.add_widget(self.subir_lectura_button)
    


    def show_file_chooser(self, instance):
        content = FileChooserListView()
        self.popup = Popup(title="Seleccionar Archivo PDF", content=content, size_hint=(0.9, 0.9))
        content.bind(on_submit=self.file_selected)
        self.popup.open()

    def file_selected(self, instance, selection, touch):
        self.selected_pdf = selection[0]
        self.popup.dismiss()

    def confirm_upload(self, instance):
        if self.selected_pdf is None or self.text_input.text.strip() == '' or self.tipo_lectura_spinner.text == '':
            self.show_error_popup("Por favor completa todos los campos.")
        else:
            # Verificar si el archivo seleccionado es un archivo PDF válido
            if not self.is_valid_pdf(self.selected_pdf):
                self.show_error_popup("El archivo seleccionado no es un archivo PDF válido.")
                return

            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text="¿Estás seguro de subir la lectura?", size_hint_y=None, height=dp(40)))
            btn_layout = BoxLayout(size_hint_y=None, height=dp(40))
            cancel_button = Button(text='Cancelar', on_release=self.cancel_upload)
            confirm_button = Button(text='Confirmar', on_release=self.upload_lecture)
            btn_layout.add_widget(cancel_button)
            btn_layout.add_widget(confirm_button)
            content.add_widget(btn_layout)
            self.popup = Popup(title="Confirmar Subida", content=content, size_hint=(None, None), size=(400, 200))
            self.popup.open()
    
    def is_valid_pdf(self,file_path):
        # Obtener la extensión del archivo
        file_extension = os.path.splitext(file_path)[1].lower()
    
        # Comprobar si la extensión es .pdf
        if file_extension == '.pdf':
            return True
        else:
            return False
        
    """
    def is_valid_pdf(self, file_path):
        try:
            doc = fitz.open(file_path)
            num_pages = len(doc)
            doc.close()
            return num_pages > 0
        except:
            return False
    """

    def cancel_upload(self, instance):
        self.popup.dismiss()

    def upload_lecture(self, instance):
        if self.selected_pdf:
            nombre_lectura = self.text_input.text
            tipo_lectura = self.tipo_lectura_spinner.text

            # Obtener la ubicación del archivo actual
            current_path = os.path.dirname(os.path.realpath(__file__))
            # Crear la ruta a la subcarpeta "lecturas" relativa a la ubicación actual del archivo
            lecturas_path = os.path.join(current_path, "lecturas")
            # Si la subcarpeta no existe, créala
            if not os.path.exists(lecturas_path):
                os.makedirs(lecturas_path)
            # Crear una copia del archivo PDF en la subcarpeta "lecturas"
            new_pdf_path = os.path.join(lecturas_path, os.path.basename(self.selected_pdf))
            with open(self.selected_pdf, 'rb') as f_in:
                with open(new_pdf_path, 'wb') as f_out:
                    f_out.write(f_in.read())

            # Guardar la ubicación de la copia del archivo PDF de manera relativa
            relative_pdf_path = os.path.relpath(new_pdf_path, current_path)

            # Guardar la información en la base de datos SQLite
            conn = sqlite3.connect('EntrenadorLectura.db')
            c = conn.cursor()
            c.execute("INSERT INTO Lecturas (Nombre_Lectura, Tipo_Lectura, Ubicacion_Lectura) VALUES (?, ?, ?)",
                    (nombre_lectura, tipo_lectura, relative_pdf_path))
            conn.commit()
            conn.close()

            print("Archivo PDF copiado:", relative_pdf_path)

            admin_screen = self.parent.parent.get_screen('administrador')
            admin_layout = admin_screen.children[0]

            lecturas_layout = None
            for child in admin_layout.children:
                if isinstance(child, ScrollView):
                    lecturas_layout = child.children[0]
                    break

            # Limpiar widgets del GridLayout de las lecturas antes de mostrar lecturas actualizadas
            if lecturas_layout:
                lecturas_layout.clear_widgets()
                admin_layout.mostrar_lecturas()

            # Restablecer campos de entrada de texto y archivo seleccionado
            self.text_input.text = ""
            self.tipo_lectura_spinner.text = "Cuento"
            self.selected_pdf = None

        self.popup.dismiss()
        self.show_success_popup()

    def show_success_popup(self):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="¡Lectura agregada con éxito!", size_hint_y=None, height=dp(40)))
        btn_layout = BoxLayout(size_hint_y=None, height=dp(40))
        home_button = Button(text='Volver al inicio', on_release=self.go_to_main_screen)
        btn_layout.add_widget(home_button)
        content.add_widget(btn_layout)
        self.success_popup = Popup(title="Éxito", content=content, size_hint=(None, None), size=(300, 200))
        self.success_popup.open()

    def go_to_main_screen(self, instance):
        # Cambiar a la pantalla principal donde se muestran las lecturas disponibles
        self.parent.parent.current = 'administrador'
        # Cerrar la notificación emergente
        self.success_popup.dismiss()

    def switch_to_administrador(self, instance):
        self.parent.parent.current = 'administrador'

    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message, size_hint_y=None, height=dp(40)))
        btn_layout = BoxLayout(size_hint_y=None, height=dp(40))
        ok_button = Button(text='OK', on_release=self.dismiss_error_popup)
        btn_layout.add_widget(ok_button)
        content.add_widget(btn_layout)
        self.error_popup = Popup(title="Error", content=content, size_hint=(None, None), size=(300, 200))
        self.error_popup.open()

    def dismiss_error_popup(self, instance):
        self.error_popup.dismiss()


class MainAppp(App):
    def build(self):
        from Home import Home
        sm = ScreenManager()

        # Definir las pantallas
        admin_screen = Screen(name='administrador')
        add_lectura_screen = Screen(name='agregar_lectura')
        home_screen = Screen(name='Home')  # Agregar esta línea

        # Crear instancias de las vistas correspondientes
        admin_view = Administrador()
  # Pasar referencia al ScreenManager
        add_lectura_view = Agregar_Lectura()
        Home_view = Home()

        # Agregar las vistas a las pantallas
        admin_screen.add_widget(admin_view)
        add_lectura_screen.add_widget(add_lectura_view)
        home_screen.add_widget(Home_view)

        # Agregar las pantallas al ScreenManager
        sm.add_widget(admin_screen)
        sm.add_widget(add_lectura_screen)
        sm.add_widget(home_screen)  # Agregar esta línea

        root = RootLayout()
        root.add_widget(sm)
        return root
if __name__ == '__main__':
    MainAppp().run()
