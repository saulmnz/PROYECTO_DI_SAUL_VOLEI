import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from conexionBD import ConexionBD


class VentanaPartidos(Gtk.Window):
    """
    VENTANA PARA REGISTRAR LOS PARTIDOS ENTRE DOS EQUIPOS EXISTENTES.
    """

    def __init__(self):

        # INICIALIZAMOS LA VENTANA PADRE
        super().__init__(title="REGISTRO DE PARTIDOS")
        self.set_default_size(500, 550)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)

        self.db = ConexionBD()

        # CAJA PRINCIPAL
        self.caja_principal = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.caja_principal)

        # ZONA SUPERIOR: TREEVIEW PARA CONSULTAR LOS PARTIDOS
        # MODELO: ID, EQUIPO LOCAL, EQUIPO VISITANTE, RESULTADO
        self.modelo = Gtk.ListStore(int, str, str, str)
        self.treeview = Gtk.TreeView(model=self.modelo)

        renderer_text = Gtk.CellRendererText()

        # CREAMOS LAS COLUMNAS DE LA TABLA
        self.treeview.append_column(Gtk.TreeViewColumn("ID", renderer_text, text=0))
        self.treeview.append_column(Gtk.TreeViewColumn("LOCAL", renderer_text, text=1))
        self.treeview.append_column(Gtk.TreeViewColumn("VISITANTE", renderer_text, text=2))
        self.treeview.append_column(Gtk.TreeViewColumn("RESULTADO", renderer_text, text=3))

        # CONTROL DE SELECCIÓN DE LA TABLA
        self.seleccion = self.treeview.get_selection()

        # AÑADIMOS SCROLL POR SI HAY MUCHOS PARTIDOS
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.add(self.treeview)
        self.caja_principal.pack_start(scroll, True, True, 0)

        # CARGAMOS LOS DATOS DESDE LA BD
        self.cargar_datos()

        # ZONA INFERIOR: FORMULARIO SECUNDARIO
        # PARA AGRUPAR LOS DATOS DEL PARTIDO
        self.frame_datos = Gtk.Frame(label="NUEVO PARTIDO")
        self.caja_principal.pack_start(self.frame_datos, False, False, 0)

        # CAJA INTERNA DEL FORMULARIO
        self.caja_formulario = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.caja_formulario.set_border_width(10)
        self.frame_datos.add(self.caja_formulario)

        # DESPLEGABLE PARA EL EQUIPO LOCAL
        self.caja_formulario.pack_start(Gtk.Label(label="EQUIPO LOCAL:", xalign=0), False, False, 0)
        self.combo_local = Gtk.ComboBoxText()
        self.caja_formulario.pack_start(self.combo_local, False, False, 0)

        # DESPLEGABLE PARA EL EQUIPO VISITANTE
        self.caja_formulario.pack_start(Gtk.Label(label="EQUIPO VISITANTE:", xalign=0), False, False, 0)
        self.combo_visitante = Gtk.ComboBoxText()
        self.caja_formulario.pack_start(self.combo_visitante, False, False, 0)

        # LLAMAMOS AL MÉTODO PARA RELLENAR AMBOS DESPLEGABLES CON DATOS DE LA BD
        self.cargar_equipos_en_combos()

        # CAMPO DE TEXTO PARA EL RESULTADO (EJ: 3-1)
        self.caja_formulario.pack_start(Gtk.Label(label="RESULTADO (EJ: 3-1):", xalign=0), False, False, 0)
        self.entry_resultado = Gtk.Entry()
        self.caja_formulario.pack_start(self.entry_resultado, False, False, 0)

        # CAJA PARA BOTONES CRUD
        self.caja_botones = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.caja_formulario.pack_start(self.caja_botones, False, False, 10)

        # BOTÓN PARA GUARDAR EL REGISTRO
        self.btn_guardar = Gtk.Button(label="GUARDAR PARTIDO")
        self.btn_guardar.connect("clicked", self.on_btn_guardar_clicked)
        self.caja_botones.pack_start(self.btn_guardar, True, True, 0)

        # BOTÓN PARA ELIMINAR EL REGISTRO SELECCIONADO
        self.btn_eliminar = Gtk.Button(label="ELIMINAR SELECCIONADO")
        self.btn_eliminar.connect("clicked", self.on_btn_eliminar_clicked)
        self.caja_botones.pack_start(self.btn_eliminar, True, True, 0)

    def mostrar_mensaje(self, tipo, mensaje, botones=Gtk.ButtonsType.OK):
        """ FUNCIÓN PARA MOSTRAR DIÁLOGOS AL USUARIO """
        dialogo = Gtk.MessageDialog(transient_for=self, flags=0, message_type=tipo, buttons=botones, text=mensaje)
        respuesta = dialogo.run()
        dialogo.destroy()
        return respuesta

    def cargar_datos(self):
        """ LIMPIA EL TREEVIEW Y VUELVE A CARGAR DESDE LA BASE DE DATOS """
        self.modelo.clear()
        partidos = self.db.obtener_partidos()
        for p in partidos:
            self.modelo.append([p[0], p[1], p[2], p[3]])

    def cargar_equipos_en_combos(self):
        """
        RECUPERA LOS EQUIPOS DE LA BASE DE DATOS Y LOS AÑADE A AMBOS DESPLEGABLES.
        """
        lista_equipos = self.db.obtener_equipos()
        for equipo in lista_equipos:
            self.combo_local.append(str(equipo[0]), equipo[1])
            self.combo_visitante.append(str(equipo[0]), equipo[1])

    def on_btn_guardar_clicked(self, widget):
        """
        EVENTO AL PULSAR EL BOTÓN GUARDAR.
        VERIFICA LOS DATOS Y LOS GUARDA EN LA TABLA PARTIDOS.
        """
        id_local = self.combo_local.get_active_id()
        id_visitante = self.combo_visitante.get_active_id()
        resultado = self.entry_resultado.get_text()

        # VALIDAMOS QUE NINGÚN CAMPO ESTÉ VACÍO
        if id_local and id_visitante and resultado:
            # DEFINIMOS QUE UN EQUIPO NO PUEDE JUGAR CONTRA SÍ MISMO
            if id_local == id_visitante:
                self.mostrar_mensaje(Gtk.MessageType.WARNING, "ERROOOR: UN EQUIPO NO PUEDE JUGAR CONTRA SÍ MISMO.")
            else:
                # INSERTAMOS EN LA BD
                self.db.insertar_partido(id_local, id_visitante, resultado)
                self.mostrar_mensaje(Gtk.MessageType.INFO, "¡¡PARTIDO GUARDADO CON ÉXITO!!")

                # REFRESCAMOS TABLA Y LIMPIAMOS FORMULARIO
                self.cargar_datos()
                self.combo_local.set_active(-1)
                self.combo_visitante.set_active(-1)
                self.entry_resultado.set_text("")
        else:
            self.mostrar_mensaje(Gtk.MessageType.ERROR, "FALTAN DATOS POR RELLENAR PARA GUARDAR EL PARTIDO.")

    def on_btn_eliminar_clicked(self, widget):
        """
        EVENTO PARA ELIMINAR EL PARTIDO SELECCIONADO EN LA TABLA.
        """
        modelo, iterador = self.seleccion.get_selected()
        if iterador is not None:
            respuesta = self.mostrar_mensaje(
                Gtk.MessageType.QUESTION,
                "¿ESTÁS SEGURO DE QUE QUIERES ELIMINAR ESTE PARTIDO DEFINITIVAMENTE PARA SIEMRE SIEMPRE?",
                Gtk.ButtonsType.YES_NO
            )
            if respuesta == Gtk.ResponseType.YES:
                id_partido = modelo[iterador][0]
                self.db.eliminar_partido(id_partido)
                self.mostrar_mensaje(Gtk.MessageType.INFO, "¡PARTIDO ELIMINADO CRACKK!")
                self.cargar_datos()
        else:
            self.mostrar_mensaje(Gtk.MessageType.ERROR, "SELECCIONA UN PARTIDO EN LA TABLA PRIMERO.")