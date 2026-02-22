import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from conexionBD import ConexionBD


class VentanaEquipos(Gtk.Window):
    """
    VENTANA PARA GESTIONAR LA CREACIÓN, EDICIÓN Y BORRADO DE EQUIPOS.
    IMPLEMENTA TREEVIEW Y MENSAJES DE DIÁLOGO (CRUD COMPLETO).
    """

    def __init__(self):
        super().__init__(title="GESTIÓN DE EQUIPOS")
        self.set_default_size(500, 500)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)

        # INSTANCIAMOS BD
        self.db = ConexionBD()

        self.caja_principal = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.caja_principal)

        # ZONA SUPERIOR: TREEVIEW PARA CONSULTAR LOS EQUIPOS
        self.modelo = Gtk.ListStore(int, str, str, bool)
        self.treeview = Gtk.TreeView(model=self.modelo)

        # RENDERERS, CÓMO SE DIBUJA CADA CELDA
        renderer_text = Gtk.CellRendererText()
        renderer_toggle = Gtk.CellRendererToggle()

        # CREAMOS LAS COLUMNAS
        self.treeview.append_column(Gtk.TreeViewColumn("ID", renderer_text, text=0))
        self.treeview.append_column(Gtk.TreeViewColumn("NOMBRE", renderer_text, text=1))
        self.treeview.append_column(Gtk.TreeViewColumn("CATEGORÍA", renderer_text, text=2))
        self.treeview.append_column(Gtk.TreeViewColumn("FEDERADO", renderer_toggle, active=3))

        # GESTIONAMOS CUANDO EL USUARIO HACE CLIC EN UNA FILA
        self.seleccion = self.treeview.get_selection()
        self.seleccion.connect("changed", self.on_seleccion_cambiada)

        # AÑADIMOS SCROLL A LA TABLA POR SI HAY MUCHOS DATOS
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.add(self.treeview)
        self.caja_principal.pack_start(scroll, True, True, 0)

        # CARGAMOS LOS DATOS DE LA BD EN EL TREEVIEW
        self.cargar_datos()

        # ZONA INFERIOR: FORMULARIO SECUNDARIO PARA AÑADIR/EDITAR
        self.frame_datos = Gtk.Frame(label="DATOS DEL EQUIPO")
        self.caja_principal.pack_start(self.frame_datos, False, False, 0)
        self.caja_formulario = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.caja_formulario.set_border_width(10)
        self.frame_datos.add(self.caja_formulario)

        # ENTRADA: NOMBRE DEL EQUIPO
        self.caja_formulario.pack_start(Gtk.Label(label="NOMBRE DEL EQUIPO:", xalign=0), False, False, 0)
        self.entry_nombre = Gtk.Entry()
        self.caja_formulario.pack_start(self.entry_nombre, False, False, 0)

        # COMBOBOXTEXT: CATEGORÍA DEL EQUIPO
        self.caja_formulario.pack_start(Gtk.Label(label="CATEGORÍA:", xalign=0), False, False, 0)
        self.combo_categoria = Gtk.ComboBoxText()
        for cat in ["INFANTIL", "CADETE", "JUVENIL", "SENIOR"]:
            self.combo_categoria.append_text(cat)
        self.caja_formulario.pack_start(self.combo_categoria, False, False, 0)

        # CHECKBUTTON PARA SABER SI ESTÁ FEDERADO
        self.check_federado = Gtk.CheckButton(label="¿ESTE EQUIPO ESTÁ FEDERADO?")
        self.caja_formulario.pack_start(self.check_federado, False, False, 0)

        # CAJA PARA BOTONES CRUD
        self.caja_botones = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.caja_formulario.pack_start(self.caja_botones, False, False, 10)

        # BOTONES
        self.btn_guardar = Gtk.Button(label="GUARDAR NUEVO")
        self.btn_guardar.connect("clicked", self.on_btn_guardar_clicked)
        self.caja_botones.pack_start(self.btn_guardar, True, True, 0)

        self.btn_actualizar = Gtk.Button(label="ACTUALIZAR")
        self.btn_actualizar.connect("clicked", self.on_btn_actualizar_clicked)
        self.caja_botones.pack_start(self.btn_actualizar, True, True, 0)

        self.btn_eliminar = Gtk.Button(label="ELIMINAR")
        self.btn_eliminar.connect("clicked", self.on_btn_eliminar_clicked)
        self.caja_botones.pack_start(self.btn_eliminar, True, True, 0)

        # VARIABLE PARA SABER QUÉ ID ESTAMOS EDITANDO
        self.id_equipo_actual = None

    # FUNCIONES PARA LA LÓGICA
    def mostrar_mensaje(self, tipo, mensaje, botones=Gtk.ButtonsType.OK):
        """ FUNCIÓN AUXILIAR PARA MOSTRAR CUADROS DE DIÁLOGO AL USUARIO """
        dialogo = Gtk.MessageDialog(transient_for=self, flags=0, message_type=tipo, buttons=botones, text=mensaje)
        respuesta = dialogo.run()
        dialogo.destroy()
        return respuesta

    def cargar_datos(self):
        """ LIMPIA EL TREEVIEW Y VUELVE A CARGAR DESDE LA BASE DE DATOS """
        self.modelo.clear()
        equipos = self.db.obtener_equipos()
        for eq in equipos:
            # eq[0]=ID, eq[1]=Nombre, eq[2]=Cat, eq[3]=Federado(0 o 1)
            federado_bool = True if eq[3] == 1 else False
            self.modelo.append([eq[0], eq[1], eq[2], federado_bool])

    def on_seleccion_cambiada(self, seleccion):
        """ CARGA LOS DATOS DE LA TABLA EN EL FORMULARIO CUANDO SE HACE CLIC """
        modelo, iterador = seleccion.get_selected()
        if iterador is not None:
            self.id_equipo_actual = modelo[iterador][0]
            self.entry_nombre.set_text(modelo[iterador][1])

            # BUSCAMOS LA CATEGORÍA EN EL COMBO PARA SELECCIONARLA
            cat_seleccionada = modelo[iterador][2]
            for i, cat in enumerate(["INFANTIL", "CADETE", "JUVENIL", "SENIOR"]):
                if cat == cat_seleccionada:
                    self.combo_categoria.set_active(i)
                    break

            self.check_federado.set_active(modelo[iterador][3])

    def on_btn_guardar_clicked(self, widget):
        nombre = self.entry_nombre.get_text()
        categoria = self.combo_categoria.get_active_text()
        federado = 1 if self.check_federado.get_active() else 0

        if nombre and categoria:
            self.db.insertar_equipo(nombre, categoria, federado)
            self.mostrar_mensaje(Gtk.MessageType.INFO, f"¡¡EQUIPO '{nombre}' CREADO CON ÉXITO!!")
            self.cargar_datos()
            self.limpiar_formulario()
        else:
            self.mostrar_mensaje(Gtk.MessageType.WARNING, "ERROOORRR: FALTAN DATOS POR RELLENAR.")

    def on_btn_actualizar_clicked(self, widget):
        if self.id_equipo_actual is not None:
            nombre = self.entry_nombre.get_text()
            categoria = self.combo_categoria.get_active_text()
            federado = 1 if self.check_federado.get_active() else 0

            self.db.actualizar_equipo(self.id_equipo_actual, nombre, categoria, federado)
            self.mostrar_mensaje(Gtk.MessageType.INFO, "¡¡DATOS DEL EQUIPO ACTUALIZADOS!!")
            self.cargar_datos()
        else:
            self.mostrar_mensaje(Gtk.MessageType.ERROR, "SELECCIONA PRIMERO UN EQUIPO EN LA TABLA PARA ACTUALIZARLO.")

    def on_btn_eliminar_clicked(self, widget):
        if self.id_equipo_actual is not None:
            # INTERFAZ DIALOGANDO CON EL USUARIO EN OPERACIÓN CRÍTICA
            respuesta = self.mostrar_mensaje(
                Gtk.MessageType.QUESTION,
                "¿¿ESTÁS SEGURO DE QUE QUIERES ELIMINAR ESTE REGISTRO?? ESTA ACCIÓN NO SE PUEDE DESHACER...",
                Gtk.ButtonsType.YES_NO
            )
            if respuesta == Gtk.ResponseType.YES:
                self.db.eliminar_equipo(self.id_equipo_actual)
                self.mostrar_mensaje(Gtk.MessageType.INFO, "¡REGISTRO ELIMINADO CON ÉXITO!")
                self.cargar_datos()
                self.limpiar_formulario()
        else:
            self.mostrar_mensaje(Gtk.MessageType.ERROR, "SELECCIONA UN EQUIPO EN LA TABLA PARA ELIMINARLO.")

    def limpiar_formulario(self):
        self.id_equipo_actual = None
        self.entry_nombre.set_text("")
        self.combo_categoria.set_active(-1)
        self.check_federado.set_active(False)
        self.seleccion.unselect_all()