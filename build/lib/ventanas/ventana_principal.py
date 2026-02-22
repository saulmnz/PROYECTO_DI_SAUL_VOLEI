import gi
gi.require_version('Gtk', '3.0')
from ventanas.ventana_equipos import VentanaEquipos
from ventanas.ventana_jugadores import VentanaJugadores
from ventanas.ventana_partidos import VentanaPartidos
from gi.repository import Gtk, GdkPixbuf
class VentanaPrincipal(Gtk.Window):
    """
    VENTANA PRINCIPAL DE LA APLICACIÓN.
    SIRVE COMO PUNTO DE ENTRADA GRÁFICO.
    """

    def __init__(self):
        """
        CONFIGURAMOS TAMAÑO, TÍTULO Y LOS CONTENEDORES INICIALES.
        """
        super().__init__(title="GESTOR CLUB DE VOLEIBOL GALICIIA")

        # CONFIGURAMOS EL TAMAÑO DE LA VENTANA
        self.set_default_size(600, 400)
        self.set_border_width(15)
        self.set_position(Gtk.WindowPosition.CENTER)

        # CONTENEDOR PRINCIPAL TIPO BOX CON ORIENTACIÓN VERTICAL
        self.caja_principal = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.caja_principal)

        # ETIQUETA DE BIENVENIDA CON ESTILO PANGO MARKUP (PARA QUE NO SEA SOSETE)
        self.etiqueta_bienvenida = Gtk.Label()
        self.etiqueta_bienvenida.set_markup("<span foreground='#20B2AA' font_desc='28' weight='bold'>BIENVENIDO AL SISTEMA DE GESTIÓN DE VOLEIBOL</span>")
        self.caja_principal.pack_start(self.etiqueta_bienvenida, True, True, 10)

        # CARGAMOS EL GIF COMO UNA ANIMACIÓN
        animacion = GdkPixbuf.PixbufAnimation.new_from_file("img/gif1.gif")
        # CREAMOS EL WIDGET DE IMAGEN A PARTIR DE LA ANIMACIÓN
        self.imagen_logo = Gtk.Image.new_from_animation(animacion)
        self.caja_principal.pack_start(self.imagen_logo, False, False, 10)

        # CAJA PARA AGRUPAR LOS BOTONES Y QUE NO SEAN TAN ANCHOS
        self.caja_botones = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.caja_principal.pack_start(self.caja_botones, False, False, 0)

        # BOTÓN 1: ABRIR GESTIÓN DE EQUIPOS
        self.btn_equipos = Gtk.Button(label="1. GESTIONAR EQUIPOS")
        self.btn_equipos.connect("clicked", self.abrir_ventana_equipos)
        self.caja_botones.pack_start(self.btn_equipos, False, False, 10)

        # BOTÓN 2: ABRIR GESTIÓN DE JUGADORES
        self.btn_jugadores = Gtk.Button(label="2. GESTIONAR JUGADORES")
        self.btn_jugadores.connect("clicked", self.abrir_ventana_jugadores)
        self.caja_botones.pack_start(self.btn_jugadores, False, False, 10)

        # BOTÓN 3: ABRIR GESTIÓN PARTIDOS
        self.btn_partidos = Gtk.Button(label="3. GESTIONAR PARTIDOS")
        self.btn_partidos.connect("clicked", self.abrir_ventana_partidos)
        self.caja_botones.pack_start(self.btn_partidos, False, False, 10)


    def abrir_ventana_equipos(self, widget):
        self.ventana_equipos = VentanaEquipos()
        self.ventana_equipos.show_all()

    def abrir_ventana_jugadores(self, widget):
        self.ventana_jugadores = VentanaJugadores()
        self.ventana_jugadores.show_all()

    def abrir_ventana_partidos(self, widget):
        self.ventana_partidos = VentanaPartidos()
        self.ventana_partidos.show_all()
