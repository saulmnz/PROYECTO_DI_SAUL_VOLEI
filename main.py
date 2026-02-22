import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from ventanas.ventana_principal import VentanaPrincipal


def main():

    # INSTANCIAMOS LA VENTANA PRINCIPAL QUE ACABAMOS DE CREAR
    ventana = VentanaPrincipal()

    # PARA QUE FUNCIONE LA X
    ventana.connect("destroy", Gtk.main_quit)
    ventana.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()