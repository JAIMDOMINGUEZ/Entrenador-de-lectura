from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from Controlador import ControladorCuentas ,ControladorLecturas
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserListView
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock


class VentanaCrearCuenta(BoxLayout):
    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = [50, 20]
        self.controlador = ControladorCuentas
        self.add_widget(Label(text="Crear Cuenta", font_size=40,color=[0, 0, 0, 1]))
        self.add_widget(Label(text="Nombre de Usuario:",color=[0, 0, 0, 1],font_size=20))
        self.username_input = TextInput(multiline=False,halign="center",font_size=25)
        self.add_widget(self.username_input)
        
        self.add_widget(Label(text="Ingrese Contraseña:",color=[0, 0, 0, 1],font_size=20))
        self.password_input = TextInput(multiline=False, password=True,halign="center",font_size=25)
        self.add_widget(self.password_input)

        self.show_password_button = Button(text="Mostrar Contraseña")
        self.show_password_button.bind(on_press=self.toggle_password_visibility)
        self.add_widget(self.show_password_button)
        
        self.add_widget(Label(text="Confirmar Contraseña:",color=[0, 0, 0, 1],font_size=20))
        self.confirm_password_input = TextInput(multiline=False, password=True,halign="center",font_size=25)
        self.add_widget(self.confirm_password_input)
        
        self.show_confirm_password_button = Button(text="Mostrar Contraseña")
        self.show_confirm_password_button.bind(on_press=self.toggle_confirm_password_visibility)
        self.add_widget(self.show_confirm_password_button)

        self.create_button = Button(text="Crear Cuenta")
        self.create_button.bind(on_press=self.crear_cuenta)
        self.add_widget(self.create_button)
        
        self.add_widget(Label(text="¿Ya tienes una cuenta?", font_size=25,color=[0, 0, 0, 1]))
        self.login_button = Button(text="Iniciar Sesión")
        self.login_button.bind(on_press=lambda instance: self.ir_a_inicio_sesion())

        self.add_widget(self.login_button)


    def toggle_password_visibility(self, instance):
        if self.password_input.password:
            self.password_input.password = False
            self.show_password_button.text = "Ocultar Contraseña"
        else:
            self.password_input.password = True
            self.show_password_button.text = "Mostrar Contraseña"

    def toggle_confirm_password_visibility(self, instance):
        # Cambia la visibilidad de la contraseña en el campo de confirmación
        if self.confirm_password_input.password:
            self.confirm_password_input.password = False
            self.show_confirm_password_button.text = "Ocultar Contraseña"
        else:
            self.confirm_password_input.password = True
            self.show_confirm_password_button.text = "Mostrar Contraseña"

    def crear_cuenta(self, instance):
        nombre_usuario = self.username_input.text
        contraseña = self.password_input.text
        confirmar_contraseña = self.confirm_password_input.text
        
        if nombre_usuario.strip() == '' or contraseña.strip() == '' or confirmar_contraseña.strip() == '':
            self.mostrar_mensaje_campos_vacios()
            return
        
        if contraseña != confirmar_contraseña:
            self.mostrar_mensaje_contrasenas_no_coinciden()
            return
        
        if self.controlador.crear_cuenta(nombre_usuario,contraseña):
            self.mostrar_mensaje_cuenta_creada()
            self.ir_a_inicio_sesion()
        else:
            self.mostrar_mensaje_usuario_existente()
    
    def mostrar_mensaje_cuenta_creada(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Cuenta creada con éxito", font_size=20))
        popup = Popup(title='Éxito', content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()
    def mostrar_mensaje_usuario_existente(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="El usuario ya existe", font_size=20))
        btn_volver_a_intentarlo = Button(text="Volver a Intentarlo")
        btn_volver_a_intentarlo.bind(on_press=self.volver_a_intentarlo)
        popup_content.add_widget(btn_volver_a_intentarlo)
        self.popup_usuario_existente = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
        self.popup_usuario_existente.open()
    
    def volver_a_intentarlo(self, instance):
        self.popup_usuario_existente.dismiss()
        self.username_input.text = ''
        self.password_input.text = ''
        self.confirm_password_input.text = ''
    
    def mostrar_mensaje_contrasenas_no_coinciden(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Las contraseñas no coinciden", font_size=20))
        btn_volver_a_intentarlo = Button(text="Volver a Intentarlo")
        btn_volver_a_intentarlo.bind(on_press=self.volver_a_intentarlo_contraseñas)
        popup_content.add_widget(btn_volver_a_intentarlo)
        self.popup_contraseñas_no_coinciden = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
        self.popup_contraseñas_no_coinciden.open()
    
    def volver_a_intentarlo_contraseñas(self, instance):
        self.popup_contraseñas_no_coinciden.dismiss()
        self.password_input.text = ''
        self.confirm_password_input.text = ''
    
    def mostrar_mensaje_campos_vacios(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Por favor completa todos los campos", font_size=20))
        btn_ok = Button(text="OK")
        btn_ok.bind(on_press=self.dismiss_popup)
        popup_content.add_widget(btn_ok)
        self.popup_campos_vacios = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
        self.popup_campos_vacios.open()

    def dismiss_popup(self, instance):
        self.popup_campos_vacios.dismiss()
    def ir_a_inicio_sesion(self):
        ventana_inicio_sesion = VentanaIniciarSesion(self)
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_inicio_sesion)

class VentanaIniciarSesion(BoxLayout):
    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = [50, 20]
        self.id_usuario = None
        self.controlador = ControladorCuentas()
        
        self.add_widget(Label(text="Iniciar Sesión", font_size=40, color=[0, 0, 0, 1]))
        
        self.add_widget(Label(text="Nombre de Usuario:", color=[0, 0, 0, 1], font_size=35))
        self.username_input = TextInput(multiline=False,halign="center",font_size=25)

        self.add_widget(self.username_input)
        
        self.add_widget(Label(text="Contraseña:", color=[0, 0, 0, 1], font_size=35))
        self.password_input = TextInput(multiline=False, password=True,halign="center",font_size=25)
        self.add_widget(self.password_input)

        self.show_password_button = Button(text="Mostrar Contraseña")
        self.show_password_button.bind(on_press=self.toggle_password_visibility)
        self.add_widget(self.show_password_button)
        
        self.login_button = Button(text="Iniciar Sesión")
        self.login_button.bind(on_press=self.iniciar_sesion)
        self.add_widget(self.login_button)
        
        self.check_user_button = Button(text="Verificar Usuario")
        self.check_user_button.bind(on_press=self.verificar_usuario)
        self.check_user_button.disabled = True  # Desactiva el botón
        self.check_user_button.opacity = 0
        self.add_widget(self.check_user_button)
        
        self.add_widget(Label(text="¿No tienes una cuenta?", font_size=25, color=[0, 0, 0, 1]))
        self.create_account_button = Button(text="Crear cuenta nueva")
        self.create_account_button.bind(on_press=lambda instance: self.ir_a_crear_cuenta())
        self.add_widget(self.create_account_button)
    
    def toggle_password_visibility(self, instance):
        # Cambia la visibilidad de la contraseña en el campo de entrada
        if self.password_input.password:
            self.password_input.password = False
            self.show_password_button.text = "Ocultar Contraseña"
        else:
            self.password_input.password = True
            self.show_password_button.text = "Mostrar Contraseña"

    def mostrar_mensaje_campos_vacios(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Por favor completa todos los campos", font_size=20))
        btn_ok = Button(text="OK")
        btn_ok.bind(on_press=self.dismiss_popup)
        popup_content.add_widget(btn_ok)
        self.popup_campos_vacios = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
        self.popup_campos_vacios.open()

    def mostrar_mensaje_campos_vacios(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Por favor completa todos los campos", font_size=20))
        btn_ok = Button(text="OK")
        btn_ok.bind(on_press=self.dismiss_popup)
        # Crear el Popup y asignarlo a self.popup_campos_vacios
        self.popup_campos_vacios = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
        self.popup_campos_vacios.open()  # Abre el popup

    def dismiss_popup(self, instance):
        if hasattr(self, 'popup_campos_vacios'):
            self.popup_campos_vacios.dismiss()
    

    def mostrar_mensaje_credenciales_incorrectas(self):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        popup_content.add_widget(Label(text="Nombre de usuario o contraseña incorrectos", font_size=20))
        btn_ok = Button(text="OK")
        btn_ok.bind(on_press=self.dismiss_popup)
        popup = Popup(title='Error', content=popup_content, size_hint=(None, None), size=(400, 200))
        popup.open()

        self.username_input.text = ''
        self.password_input.text = ''

    
    def iniciar_sesion(self, instance):
        nombre_usuario = self.username_input.text
        contraseña = self.password_input.text
        
        if nombre_usuario.strip() == '' or contraseña.strip() == '':
            self.mostrar_mensaje_campos_vacios()
            return

        if self.controlador.iniciar_sesion(nombre_usuario, contraseña):
            print("Inicio de sesión exitoso")
            self.id_usuario=self.controlador.obtener_id_usuario(nombre_usuario,contraseña)
            self.ir_a_Home()
        else:
            self.mostrar_mensaje_credenciales_incorrectas()
    
    def verificar_usuario(self, instance):
        nombre_usuario = self.username_input.text
        
        if self.controlador.verificar_usuario(nombre_usuario):
            popup = Popup(title='Usuario Existente',
                          content=Label(text='El usuario existe en la base de datos.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
        else:
            popup = Popup(title='Usuario No Existente',
                          content=Label(text='El usuario no existe en la base de datos.'),
                          size_hint=(None, None), size=(400, 200))
            popup.open()

    def ir_a_crear_cuenta(self):
        ventana_crea_cuenta = VentanaCrearCuenta(self)
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_crea_cuenta)
    
    def ir_a_Home(self):
        ventana_Home = Home(self.id_usuario)  # Crear una instancia de HOME
        ventana_Home.size = Window.size  # Establecer el tamaño de la ventana Home igual al tamaño de la ventana principal
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Home)
class Home(BoxLayout):
    def __init__(self,id_usuario,**kwargs):
        super(Home, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.id_usuario = id_usuario
        self.gui()

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def gui(self):
        # Crear el diseño principal
        self.layout = RelativeLayout()
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.layout.bind(pos=self.update_rect, size=self.update_rect)

        # Crear la etiqueta "Entrenador De Lectura"
        label1 = Label(text="Entrenador De Lectura ", size_hint=(None, None), size=(Window.width, 100),
               font_family="MS Shell Dlg 2", font_size="20sp", color=[0, 0, 0, 1])

        label1.bind(size=label1.setter('text_size'), texture_size=label1.setter('size'))
        label1.pos_hint = {'center_x': 0.5, 'top': 0.9}
        self.layout.add_widget(label1)

        # Crear los botones
        button1 = Button(text="Administrar Lecturas", size_hint=(None, None), size=(200, 50),
                         font_family="MS Shell Dlg 2", font_size="15sp", color=[1, 1, 1, 1])
        button1.bind(on_press=self.ir_a_Administrador)
        button1.pos_hint = {'center_x': 0.5, 'y': 0.7}

        button2 = Button(text="Iniciar Lectura", size_hint=(None, None), size=(200, 50),
                         font_family="MS Shell Dlg 2", font_size="15sp", color=[1, 1, 1, 1])
        button2.bind(on_press=self.iniciar_lectura)
        button2.pos_hint = {'center_x': 0.5, 'y': 0.6}

        # Agregar los elementos al diseño principal
        self.layout.add_widget(button1)
        self.layout.add_widget(button2)

        # Agregar el diseño principal al diseño de la pantalla Home
        self.add_widget(self.layout)
    def ir_a_Administrador(self, instance):
        # Crear una instancia de la clase Administrador
        ventana_Admin = Administrador(self.id_usuario)
        ventana_Admin.size = Window.size
        # Cambiar a la nueva instancia de la aplicación
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Admin)
       
   
    def iniciar_lectura(self, widget):
       # Crear una instancia de la clase Administrador
        ventana_Iniciar_lectura = Seleccionar_Lectura(self.id_usuario)
        ventana_Iniciar_lectura.size = Window.size
        # Cambiar a la nueva instancia de la aplicación
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Iniciar_lectura)
       
    


class Administrador(RelativeLayout):
    def __init__(self,id_usuario, **kwargs):
        super(Administrador, self).__init__(**kwargs)
        self.selected_lectura_id = None  # Variable para almacenar el ID de la lectura seleccionada
        self.controlador=ControladorLecturas()
        self.id_usuario=id_usuario
        self.scroll_view=ScrollView(size_hint=(1, 0.5), pos_hint={'x': 0, 'y': 0.3})
        self.gui()
        self.mostrar_lecturas()
    

    def mostrar_lecturas(self):
        
        lecturas=self.controlador.mostrar_lecturas_disponibles(self.id_usuario)
        # Crear un ScrollView para contener los botones de lectura
        self.scroll_view = ScrollView(size_hint=(1, 0.5), pos_hint={'x': 0, 'y': 0.3})
        layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        # Crear botones para mostrar las lecturas disponibles
        for lectura in lecturas:
            ID_Lecturas, nombre_lectura, tipo_lectura = lectura[:3]  # Desempaqueta los primeros tres valores
            texto_boton = f"{nombre_lectura} ------ {tipo_lectura}"
            boton = Button(text=texto_boton, size_hint_y=None, height=60)

            # Modificar el evento on_press para almacenar el ID de la lectura seleccionada
            boton.bind(on_press=lambda instancia, ID_Lecturas=ID_Lecturas: self.select_lectura(ID_Lecturas))
            layout.add_widget(boton)


        self.scroll_view.add_widget(layout)
        
        self.add_widget(self.scroll_view)

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
            lectura= self.controlador.mostrar_lectura_id(self.selected_lectura_id,self.id_usuario)
            if lectura:
                nombre_lectura = lectura[0]
                # Mostrar la advertencia para confirmar la eliminación con el nombre de la lectura
                content = BoxLayout(orientation='vertical')
                content.add_widget(Label(text=f"¿Estás seguro de eliminar la lectura '{nombre_lectura}'?", size_hint_y=None, height=dp(40)))
                btn_layout = BoxLayout(size_hint_y=None, height=dp(40))
                cancel_button = Button(text='Cancelar', on_release=self.dismiss_popup)
                confirm_button = Button(text='Confirmar', on_release=lambda instance: self.confirm_delete(nombre_lectura))
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
        if self.controlador.eliminar_lectura(lectura_nombre,self.id_usuario):
            # Mostrar notificación de eliminación exitosa
            self.show_notification(f"Lectura '{lectura_nombre}' eliminada exitosamente.")
            # Actualizar la vista
            self.mostrar_lecturas()  # Actualizar la lista de lecturas
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
        self.home_button = Button(text="HOME", pos_hint={'x': 0.0294985, 'y': 0.93}, size_hint=(0.2, 0.03))
        self.home_button.bind(on_press=self.ir_a_home)
        self.add_widget(self.home_button)

        self.label = Label(text="Administrador de Lecturas", halign='center', pos_hint={'x': 0.100000, 'y': 0.8},
                           size_hint=(0.843658, 0.303333), font_size=26, color=[0, 0, 0, 1])
        self.add_widget(self.label)

        self.label2 = Label(text="Lecturas Disponibles", halign='center', pos_hint={'x': 0.100000, 'y': 0.7},
                            size_hint=(0.843658, 0.303333), font_size=24, color=[0, 0, 0, 1])
        self.add_widget(self.label2)

        self.agregar = Button(text="Agregar Lectura", size_hint=(0.5, 0.1), pos_hint={'x': 0, 'y': 0})
        self.agregar.bind(on_press=self.ir_a_agregar_lectura)
        self.add_widget(self.agregar)

        self.eliminar = Button(text="Eliminar Lectura", size_hint=(0.5, 0.1), pos_hint={'x': 0.5, 'y': 0})
        self.eliminar.bind(on_press=lambda instance: self.eliminar_lectura())
        self.add_widget(self.eliminar)
        

    

    def ir_a_home(self, instance):
        ventana_Home = Home(self.id_usuario)
        ventana_Home.size = Window.size
        # Cambiar a la nueva instancia de la aplicación
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Home)
    def ir_a_agregar_lectura(self, instance):
        ventana_agregar_lectura = Agregar_Lectura(self.id_usuario)
        ventana_agregar_lectura.size = Window.size
        # Cambiar a la nueva instancia de la aplicación
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_agregar_lectura)
class Agregar_Lectura(RelativeLayout):
    def __init__(self,id_usuario, **kwargs):
        super(Agregar_Lectura, self).__init__(**kwargs)
        self.selected_pdf = None  # Variable para guardar la ubicación del PDF seleccionado
        self.id_usuario=id_usuario
        self.controlador=ControladorLecturas()
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
        self.cancelar_button.bind(on_press=self.ir_a_Administrador)
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
        try:
            self.selected_pdf = selection[0]
            print("Archivo seleccionado:", self.selected_pdf)
        except IndexError:
            print("Error: No se ha seleccionado ningún archivo.")
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
        return self.controlador.es_valido(file_path)
    def cancel_upload(self, instance):
        self.ir_a_Administrador()

    def upload_lecture(self, instance):
        if self.selected_pdf:
            nombre_lectura = self.text_input.text
            tipo_lectura = self.tipo_lectura_spinner.text
            if(self.controlador.salvar_archivo(self.id_usuario,nombre_lectura,tipo_lectura,self.selected_pdf)):
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
        home_button = Button(text='Volver al inicio', on_release=self.ir_a_Administrador)
        btn_layout.add_widget(home_button)
        content.add_widget(btn_layout)
        self.success_popup = Popup(title="Éxito", content=content, size_hint=(None, None), size=(300, 200))
        self.success_popup.open()

   
    def ir_a_Administrador(self, instance):
        # Cerrar el popup de éxito si está abierto
        if hasattr(self, 'success_popup') and self.success_popup:
            self.success_popup.dismiss()
        # Crear una instancia de la clase Administrador
        ventana_Admin = Administrador(self.id_usuario)
        ventana_Admin.size = Window.size

        # Cambiar a la nueva instancia de la aplicación
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Admin)



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

class Seleccionar_Lectura(RelativeLayout):
    def __init__(self,id_usuario, **kwargs):
        super(Seleccionar_Lectura, self).__init__(**kwargs)
        self.id_usuario=id_usuario
        self.controlador=ControladorLecturas()
        self.gui()

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
 
    def go_to_home(self, instance):
        ventana_Home = Home(self.id_usuario)
        ventana_Home.size = Window.size
        # Cambiar a la nueva instancia de la aplicación
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Home)

    def gui(self):
        self.w1 = self
        with self.w1.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.w1.size, pos=self.w1.pos)
        self.w1.bind(pos=self.update_rect, size=self.update_rect)
        self.menu_bar = RelativeLayout(pos_hint ={'x':-0.041841, 'y':0.880952}, size_hint = (1.51464, 0.142857))
        self.w1.add_widget(self.menu_bar)

        self.home_button = Button(text="HOME", pos_hint={'x': 0.0294985, 'y': 0.9}, size_hint=(0.2, 0.04))
        self.home_button.bind(on_press=self.go_to_home)  # Vincular el botón al método go_to_home
        self.add_widget(self.home_button)



        self.vertical = BoxLayout(orientation = 'vertical', pos_hint ={'x':0.083682, 'y':0.0714286}, size_hint = (0.83682, 0.714286))
        
        self.w1.add_widget(self.vertical)
        self.Select_Tipo = Spinner(text = "Tipo Lectura", values = ("Cuento", "Novela", "Articulo"), pos_hint ={'x':0.167364, 'y':0.8}, size_hint = (0.627615, 0.0809524), font_family = "MS Shell Dlg 2", font_size = "19", color = [1, 1, 1, 1], background_color = [1, 1, 1, 1])
        self.w1.add_widget(self.Select_Tipo)
        self.Select_Tipo.bind(text = self.on_Select_Tipo)
        return self.w1
      
    def seleccionador(self, widget, value):
        print('seleccionador')
    def lectura_Seleccionada(self, instance):
        
        archivo=self.controlador.mostar_lectura_nombre(self.id_usuario,instance.text)
        if (self.controlador.archivo_existe(archivo)):#verificar_existencia_pdf(archivo)
           self.ir_a_preferencias(archivo)
        else:
            print("archivo no encontrado")
            popup_content = Label(text="No se encontro el documento de la lectura.")
            popup = Popup(title="Error", content=popup_content, size_hint=(None, None), size=(400, 200))
            popup.open()  # Mostrar el Popup
           
    def on_Select_Tipo(self, widget, value):
        self.mostar_lecturas(value)

    def mostar_lecturas(self, value):
    
        self.grid = GridLayout(cols=2, size_hint_y=None)  # Permitir que el tamaño en y no dependa del contenido
        self.grid.bind(minimum_height=self.grid.setter('height'))  # Ajustar automáticamente la altura del GridLayout según el contenido
        lista = []
        if value == "Cuento" or value == "Novela" or value == "Articulo":
            lista = self.controlador.mostar_lectura_tipo(self.id_usuario,value)
        for element in lista:
            btn = Button(text=element, background_color=(1, 1, 1, 1), color=(1, 1, 1, 1), size_hint_y=None, height=120)  # Establecer una altura fija para los botones
            btn.text_size = (80, None)
            btn.bind(on_press=self.lectura_Seleccionada)
            self.grid.add_widget(btn)

        # Crear ScrollView y agregar el GridLayout
        scroll_view = ScrollView()
        scroll_view.add_widget(self.grid)

        # Limpiar y agregar ScrollView a la vertical layout
        self.vertical.clear_widgets()
        self.vertical.add_widget(scroll_view)
    def ir_a_preferencias(self,archivo):
        ventana_Preferencias = Preferencias(self.id_usuario,archivo)
        ventana_Preferencias.size = Window.size
        # Cambiar a la nueva instancia de la aplicación
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Preferencias)



class Preferencias(RelativeLayout):
    def __init__(self,id_usuario,archivo, **kwargs):
        super(Preferencias, self).__init__(**kwargs)
        self.popup = None 
        self.archivo=archivo
        self.id_usuario=id_usuario
        self.gui()

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def gui(self):
        
        self.w1 = self
        with self.w1.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.w1.size, pos=self.w1.pos)
        self.w1.bind(pos=self.update_rect, size=self.update_rect)
        self.widget_menu_bar = RelativeLayout(pos_hint ={'x':-0.0772201, 'y':0.860465}, size_hint = (1.46718, 0.162791))
        self.w1.add_widget(self.widget_menu_bar)

        self.home = Button(text = "Home", pos_hint ={'x':0.0526316, 'y':0.4}, size_hint = (0.236842, 0.314286), color = [1, 1, 1, 1])
        self.home.bind(on_press=self.go_to_home)
        self.widget_menu_bar.add_widget(self.home)

        self.lbl_preferencias = Label(text = "Preferencias", halign='left', pos_hint ={'x':0.30888, 'y':0.8}, size_hint = (0.34749, 0.0837209), color = [0, 0, 0, 1])
        self.lbl_preferencias.bind(size=self.lbl_preferencias.setter('text_size'))
        self.w1.add_widget(self.lbl_preferencias)

        self.lbl_tipografia = Label(text = "Tipografia:", halign='left', pos_hint ={'x':0.03861, 'y':0.739535}, size_hint = (0.34749, 0.0511628), color = [0, 0, 0, 1])
        self.lbl_tipografia.bind(size=self.lbl_tipografia.setter('text_size'))
        self.w1.add_widget(self.lbl_tipografia)

        self.select_tipografia = Spinner(text = "Arial", values = ("Arial", "Times New Roman ", "Helvetica"), pos_hint ={'x':0.11583, 'y':0.669767}, size_hint = (0.694981, 0.0511628))
        self.w1.add_widget(self.select_tipografia)

        self.lbl_tamanio = Label(text = "Tamaño:", halign='left', pos_hint ={'x':0.03861, 'y':0.576744}, size_hint = (0.34749, 0.0511628), color = [0.0235294, 0.0235294, 0.0235294, 1])
        self.lbl_tamanio.bind(size=self.lbl_tamanio.setter('text_size'))
        self.w1.add_widget(self.lbl_tamanio)
        
        self.widget2 = RelativeLayout(pos_hint ={'x':0.19305, 'y':0.465116}, size_hint = (0.501931, 0.0930233))
        self.w1.add_widget(self.widget2)
        self.btn_mas_tamanio = Button(text = "+", pos_hint ={'x':0.666667, 'y':-0.05}, size_hint = (0.333333, 1.05))
        self.widget2.add_widget(self.btn_mas_tamanio)
        self.btn_mas_tamanio.bind(on_press = self.mas_tamanio)
        self.btn_menos_tamanio = Button(text = "-", pos_hint ={'x':0, 'y':-0.05}, size_hint = (0.333333, 1.05))
        self.widget2.add_widget(self.btn_menos_tamanio)
        self.btn_menos_tamanio.bind(on_press = self.menos_tamanio)
        self.input_tamanio = TextInput(text = "20", multiline = False, pos_hint ={'x':0.333333, 'y':-0.05}, size_hint = (0.333333, 1.05), foreground_color = [0, 0, 0, 1], background_color = [1, 1, 1, 1],readonly=True ,halign='center')
        self.widget2.add_widget(self.input_tamanio)
        self.widget_omitir_guardar = RelativeLayout(pos_hint ={'x':0.03861, 'y':0}, size_hint = (0.926641, 0.0930233))
        self.w1.add_widget(self.widget_omitir_guardar)
        self.btn_omitir = Button(text = "Omitir", pos_hint ={'x':0, 'y':0.2}, size_hint = (0.375, 0.55), color = [0, 0, 0, 1], background_color = [1, 1, 1, 1])
        self.widget_omitir_guardar.add_widget(self.btn_omitir)
        self.btn_omitir.bind(on_press = self.omitir_preferencias)
        self.btn_guardar = Button(text = "Guardar", pos_hint ={'x':0.625, 'y':0.2}, size_hint = (0.375, 0.55), color = [1, 1, 1, 1], background_color = [0, 0, 0, 1])
        self.widget_omitir_guardar.add_widget(self.btn_guardar)
        self.btn_guardar.bind(on_press = self.guardar_preferencias)
        self.lbl_color = Label(text = "Color:", halign='left', pos_hint ={'x':0.03861, 'y':0.390698}, size_hint = (0.34749, 0.0511628), color = [0, 0, 0, 1])
        self.lbl_color.bind(size=self.lbl_color.setter('text_size'))
        self.w1.add_widget(self.lbl_color)
        self.lbl_velocidad = Label(text = "Velocidad:", halign='left', pos_hint ={'x':0.03861, 'y':0.251163}, size_hint = (0.34749, 0.0511628), color = [0, 0, 0, 1])
        self.lbl_velocidad.bind(size=self.lbl_velocidad.setter('text_size'))
        self.w1.add_widget(self.lbl_velocidad)
        self.widget_color = RelativeLayout(pos_hint ={'x':0.0772201, 'y':0.302326}, size_hint = (0.733591, 0.0930233))
        self.w1.add_widget(self.widget_color)
        self.select_color = Spinner(text = "Rojo", values = ("Rojo", "Negro", "Azul"), pos_hint ={'x':0.210526, 'y':0.2}, size_hint = (0.578947, 0.55), color = [0, 0, 0, 1], background_color = [1, 1, 1, 1])
        self.widget_color.add_widget(self.select_color)
        self.select_color.bind(text = self.cambiar_color)
        self.btn_mas_velocidad = Button(text = "+", pos_hint ={'x':0.501931, 'y':0.134884}, size_hint = (0.15444, 0.0976744))        
        self.w1.add_widget(self.btn_mas_velocidad)
        self.btn_mas_velocidad.bind(on_press = self.mas_velocidad)
        self.btn_menos_velocidad = Button(text = "-", pos_hint ={'x':0.19305, 'y':0.134884}, size_hint = (0.15444, 0.0976744))        
        self.w1.add_widget(self.btn_menos_velocidad)
        self.btn_menos_velocidad.bind(on_press = self.menos_velocidad)
        self.input_velocidad = TextInput(text = "2", multiline = False, pos_hint ={'x':0.34749, 'y':0.134884}, size_hint = (0.15444, 0.0976744), foreground_color = [0, 0, 0, 1], background_color = [1, 1, 1, 1],readonly=True,halign='center')
        self.w1.add_widget(self.input_velocidad)
        return self.w1

    def mas_tamanio(self, widget):
        if(int(self.input_tamanio.text)>=30):
            self.input_tamanio.text=str(30)
        else:
            self.input_tamanio.text=str(int(self.input_tamanio.text)+2)

    def menos_tamanio(self, widget):
        if(int(self.input_tamanio.text)<=2):
            self.input_tamanio.text=str(2)
        else:
            self.input_tamanio.text=str(int(self.input_tamanio.text)-2)

    def mas_velocidad(self, widget):
        if(int(self.input_velocidad.text)>=4):
            self.input_velocidad.text=str(4)
        else:
            self.input_velocidad.text=str(int(self.input_velocidad.text)+1)

    def menos_velocidad(self, widget):
        if(int(self.input_velocidad.text)<=1):
            self.input_velocidad.text=str(1)
        else:
            self.input_velocidad.text=str(int(self.input_velocidad.text)-1)

    def guardar_preferencias(self, widget):
        self.confirmar_guardar()

    def cambiar_color(self, widget, value):
        if value == "Rojo":
            self.select_color.background_color="white"
            self.select_color.color="red"
        if value == "Azul":
            self.select_color.background_color="white"
            self.select_color.color="blue"
        if value == "Negro":
            self.select_color.background_color="white"
            self.select_color.color="black"

    
    def omitir_preferencias(self, instance):
        content = BoxLayout(orientation='vertical')
        message_label = Label(text='¿Estás seguro de que deseas omitir las preferencias?')
        content.add_widget(message_label)
        btn_layout = BoxLayout(size_hint_y=None, height=40)
        btn_layout.add_widget(Button(text='Si', on_release=self.omitir_guardar))
        btn_layout.add_widget(Button(text='No', on_release=self.cerrar_ventana))
        content.add_widget(btn_layout)
        self.popup = Popup(title='Confirmar Omitir', content=content, size_hint=(None, None), size=(500, 200))
        self.popup.open()

    def omitir_guardar(self,instance):
        self.popup.dismiss()
        # Deshabilitar la detección de eventos táctiles
        tamanio=24
        color= [0, 0, 0, 1]
        tipografia="Arial"
        velocidad=4
        archivo=self.archivo
        if instance.text=="Si": 
            self.abrir_ventana_iniciar_lectura(tamanio,color,tipografia,velocidad,archivo)
        elif instance.text=="Continuar":
            print(self.archivo)
            tamanio=self.input_tamanio.text
            color=self.select_color.color
            tipografia=self.select_tipografia.text
            velocidad=self.input_velocidad.text
            archivo=self.archivo
            self.abrir_ventana_iniciar_lectura(tamanio,color,tipografia,velocidad,archivo)
    def abrir_ventana_iniciar_lectura(self,tamanio,color,tipografia,velocidad,archivo):
        ventana_Iniciar_lectura = Iniciar_lectura(self.id_usuario,tamanio,color,tipografia,velocidad,archivo)
        ventana_Iniciar_lectura.size = Window.size
        # Cambiar a la nueva instancia de la aplicación
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Iniciar_lectura)
    def cerrar_ventana(self, instance):
        self.popup.dismiss()
    def confirmar_guardar(self):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='¿Estás seguro de que deseas guardar las preferencias?'))
        btn_layout = BoxLayout(size_hint_y=None, height=40)
        btn_layout.add_widget(Button(text='Continuar', on_release=self.omitir_guardar))
        btn_layout.add_widget(Button(text='No', on_release=self.cerrar_ventana))
        content.add_widget(btn_layout)
        self.popup = Popup(title='Confirmar Guardar', content=content, size_hint=(None, None), size=(500, 200))
        self.popup.open()
    def go_to_home(self, instance):
        ventana_Home = Home(self.id_usuario)
        ventana_Home.size = Window.size
        # Cambiar a la nueva instancia de la aplicación
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Home)
class Iniciar_lectura(RelativeLayout):

    def __init__(self,id_usuario,tamanio,color,tipografia,velocidad,archivo, **kwargs):
        super(Iniciar_lectura, self).__init__(**kwargs)
        self.max_value = 100
        self.current_value = self.max_value
        Clock.schedule_interval(self.decrementar_barra, 0.1)
        self.indice_actual = 0
        self.clock_event = None
        self.documento=archivo
        self.velocidad = 1  # Velocidad predeterminada  
        self.id_usuario=id_usuario
        self.controlador=ControladorLecturas()
        self.gui()
        self.asignarprefencias(tamanio,color,tipografia,velocidad)
        self.iniciar_temporizador()
        self.actualizar_texto() 

    def gui(self):
        self.canvas.before.add(Color(0.254902, 0.254902, 0.254902, 1))
        self.canvas.before.add(Rectangle(size=self.size, pos=self.pos))

        self.text_input = TextInput(text="", multiline=True, pos_hint={'x': 0.0346021, 'y': 0.255814},
                                    size_hint=(0.934256, 0.604651), foreground_color=[0.0313725, 0.0313725, 0.0313725, 1],
                                    background_color=[0.909804, 0.909804, 0.909804, 1], readonly=True)
        self.text_input.readonly=True
        self.add_widget(self.text_input)

        self.progress_bar = ProgressBar(max=100, value=0, pos_hint={'x': 0.0346021, 'y': 0.181395},
                                         size_hint=(0.934256, 0.0511628))
        self.add_widget(self.progress_bar)

        self.button_siguiente = Button(text="Siguiente", pos_hint={'x': 0.657439, 'y': 0.0651163},
                                       size_hint=(0.311419, 0.0744186), color=[1, 1, 1, 1],
                                       background_color=[0, 0, 0, 1], on_press=self.siguiente_parrafo)
        self.add_widget(self.button_siguiente)
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def decrementar_barra(self, dt):
        if self.current_value > 0:
            self.current_value -= 1
            self.progress_bar.value = self.current_value
        else:
            self.current_value = self.max_value
            self.actualizar_texto()

    def siguiente_parrafo(self,instance):
        self.actualizar_texto()
        self.current_value = self.max_value
        Clock.schedule_once(self.detener_temporizador, 0.5)

    def actualizar_texto(self):
        self.documento
        print("archivo")
        print(self.documento)
        contenido = self.controlador.dividir_documento(self.documento)
        self.text_input.text = ""
        if self.indice_actual < len(contenido) and len(contenido) > 0:
            self.text_input.text = contenido[self.indice_actual]
            self.indice_actual = (self.indice_actual + 1)
        else:
            print(self.indice_actual)
            self.detener_temporizador()
            self.mostrar_popup_felicidades()

    def mostrar_popup_felicidades(self):
        print("pop abierto")
        self.popup = Popup(title='¡Felicidades!',
                      size_hint=(None, None), size=(300, 200))
        boton_cerrar = Button(text='Cerrar', size_hint_y=None, height=40)
        boton_cerrar.bind(on_press=self.go_to_home)

        contenido = BoxLayout(orientation='vertical')
        contenido.add_widget(Label(text='Has terminado tu lección.'))
        contenido.add_widget(boton_cerrar)
        self.popup.content = contenido
        self.popup.open()
    def go_to_home(self, instance):
        if self.popup:  # Verifica si el popup existe antes de cerrarlo
            self.popup.dismiss()
            

        ventana_Home = Home(self.id_usuario)
        ventana_Home.size = Window.size
        # Cambiar a la nueva instancia de la aplicación
        App.get_running_app().root.clear_widgets()
        App.get_running_app().root.add_widget(ventana_Home)


    def iniciar_temporizador(self):
        intervalo=0.60
      
        if self.velocidad == 4:
            intervalo = 0.1
        elif self.velocidad == 3:
            intervalo = 0.2
        elif self.velocidad == 2:
            intervalo = 0.5
        elif self.velocidad == 1:
            intervalo = 0.6
        
        if self.clock_event is not None:
            self.clock_event.cancel()
        self.clock_event = Clock.schedule_interval(self.decrementar_barra, intervalo)

    def detener_temporizador(self):
        if self.clock_event is not None:
            self.clock_event.cancel()
            self.clock_event = None  # Asignar None al evento del temporizador

    def asignarprefencias(self,tamanio,color,tipografia,velocidad):
        self.velocidad = velocidad
        self.text_input.foreground_color = color
        self.text_input.font_name = tipografia
        self.text_input.font_size = tamanio
