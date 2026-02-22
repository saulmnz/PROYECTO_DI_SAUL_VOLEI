import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from conexionBD import ConexionBD


class VentanaJugadores(Gtk.Window):
    """
    VENTANA PARA AÑADIR JUGADORES Y CONSULTARLOS EN TABLA.
    """

    def __init__(self):
        super().__init__(title="GESTIÓN DE JUGADORES")
        self.set_default_size(500, 550)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)

        self.db = ConexionBD()

        self.caja_principal = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.caja_principal)

        # ZONA SUPERIOR: TREEVIEW PARA CONSULTAR LOS JUGADORES
        self.modelo = Gtk.ListStore(int, str, int, str, str)
        self.treeview = Gtk.TreeView(model=self.modelo)
        renderer_text = Gtk.CellRendererText()
        self.treeview.append_column(Gtk.TreeViewColumn("ID", renderer_text, text=0))
        self.treeview.append_column(Gtk.TreeViewColumn("NOMBRE", renderer_text, text=1))
        self.treeview.append_column(Gtk.TreeViewColumn("DORSAL", renderer_text, text=2))
        self.treeview.append_column(Gtk.TreeViewColumn("POSICIÓN", renderer_text, text=3))
        self.treeview.append_column(Gtk.TreeViewColumn("EQUIPO", renderer_text, text=4))

        self.seleccion = self.treeview.get_selection()

        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.add(self.treeview)
        self.caja_principal.pack_start(scroll, True, True, 0)

        self.cargar_datos()

        # ZONA INFERIOR: FORMULARIO
        self.frame_datos = Gtk.Frame(label="FICHA DEL JUGADOR")
        self.caja_principal.pack_start(self.frame_datos, False, False, 0)
        self.caja_formulario = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.caja_formulario.set_border_width(10)
        self.frame_datos.add(self.caja_formulario)

        self.caja_formulario.pack_start(Gtk.Label(label="NOMBRE COMPLETO:", xalign=0), False, False, 0)
        self.entry_nombre = Gtk.Entry()
        self.caja_formulario.pack_start(self.entry_nombre, False, False, 0)

        self.caja_formulario.pack_start(Gtk.Label(label="DORSAL (1-99):", xalign=0), False, False, 0)
        ajuste_dorsal = Gtk.Adjustment(value=1, lower=1, upper=99, step_increment=1, page_increment=10, page_size=0)
        self.spin_dorsal = Gtk.SpinButton()
        self.spin_dorsal.set_adjustment(ajuste_dorsal)
        self.caja_formulario.pack_start(self.spin_dorsal, False, False, 0)

        self.caja_formulario.pack_start(Gtk.Label(label="POSICIÓN:", xalign=0), False, False, 0)
        self.radio_colocador = Gtk.RadioButton.new_with_label_from_widget(None, "COLOCADOR")
        self.radio_rematador = Gtk.RadioButton.new_with_label_from_widget(self.radio_colocador, "RECEPTOR")
        self.radio_libero = Gtk.RadioButton.new_with_label_from_widget(self.radio_colocador, "LÍBERO")
        self.caja_formulario.pack_start(self.radio_colocador, False, False, 0)
        self.caja_formulario.pack_start(self.radio_rematador, False, False, 0)
        self.caja_formulario.pack_start(self.radio_libero, False, False, 0)

        self.caja_formulario.pack_start(Gtk.Label(label="ASIGNAR AL EQUIPO:", xalign=0), False, False, 0)
        self.combo_equipos = Gtk.ComboBoxText()
        self.cargar_equipos_en_combo()
        self.caja_formulario.pack_start(self.combo_equipos, False, False, 0)

        # BOTONES
        self.caja_botones = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.caja_formulario.pack_start(self.caja_botones, False, False, 10)

        self.btn_guardar = Gtk.Button(label="GUARDAR JUGADOR")
        self.btn_guardar.connect("clicked", self.on_btn_guardar_clicked)
        self.caja_botones.pack_start(self.btn_guardar, True, True, 0)

        self.btn_eliminar = Gtk.Button(label="ELIMINAR SELECCIONADO")
        self.btn_eliminar.connect("clicked", self.on_btn_eliminar_clicked)
        self.caja_botones.pack_start(self.btn_eliminar, True, True, 0)

    def mostrar_mensaje(self, tipo, mensaje, botones=Gtk.ButtonsType.OK):
        dialogo = Gtk.MessageDialog(transient_for=self, flags=0, message_type=tipo, buttons=botones, text=mensaje)
        respuesta = dialogo.run()
        dialogo.destroy()
        return respuesta

    def cargar_datos(self):
        self.modelo.clear()
        jugadores = self.db.obtener_jugadores()
        for j in jugadores:
            self.modelo.append([j[0], j[1], j[2], j[3], j[4]])

    def cargar_equipos_en_combo(self):
        for equipo in self.db.obtener_equipos():
            self.combo_equipos.append(str(equipo[0]), equipo[1])

    def on_btn_guardar_clicked(self, widget):
        nombre = self.entry_nombre.get_text()
        dorsal = self.spin_dorsal.get_value_as_int()
        posicion = "COLOCADOR"
        if self.radio_rematador.get_active():
            posicion = "REMATADOR"
        elif self.radio_libero.get_active():
            posicion = "LÍBERO"

        id_equipo = self.combo_equipos.get_active_id()

        if nombre and id_equipo:
            self.db.insertar_jugador(nombre, dorsal, posicion, id_equipo)
            self.mostrar_mensaje(Gtk.MessageType.INFO, "¡¡JUGADOR GUARDADO CON ÉXITO!!")
            self.cargar_datos()
            self.entry_nombre.set_text("")
            self.combo_equipos.set_active(-1)
        else:
            self.mostrar_mensaje(Gtk.MessageType.WARNING, "ERROOOR, FALTAN DATOS POR SELECCIONAR!!")

    def on_btn_eliminar_clicked(self, widget):
        modelo, iterador = self.seleccion.get_selected()
        if iterador is not None:
            respuesta = self.mostrar_mensaje(Gtk.MessageType.QUESTION, "¿QUIERES ELIMINAR ESTE JUGADOR DEFINITIVAMENTE?",
                                             Gtk.ButtonsType.YES_NO)
            if respuesta == Gtk.ResponseType.YES:
                self.db.eliminar_jugador(modelo[iterador][0])
                self.mostrar_mensaje(Gtk.MessageType.INFO, "¡JUGADOR ELIMINADOOOO PARA SIEMPRE!")
                self.cargar_datos()
        else:
            self.mostrar_mensaje(Gtk.MessageType.ERROR, "SELECCIONA UN JUGADOR PRIMERO.")