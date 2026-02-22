import unittest
import os
import sys
import logging

logging.basicConfig(
    filename='registro_tests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexionBD import ConexionBD


class TestBaseDatos(unittest.TestCase):

    def setUp(self):
        self.db = ConexionBD()

        # CAMBIO BD ORIGINAL A UNA DE PRUEBA PARA NO MEZCLAR DATOS
        self.db.ruta_bd = "bd_de_prueba.db"
        self.db.conexion = self.db.conectar()
        self.db.crear_tablas()

    def test_conexion_correcta(self):
        # PRIMERA PRUEBA O TEST SERÁ VERIFICAR QUE LA BD SE CONECTA BIEN
        # 'assertIsNotNone' COMPRUEBA QUE LA VARIABLE NO ESTÉ VACÍA
        self.assertIsNotNone(self.db.conexion, "LA CONEXIÓN BD A FALLADO.")
        logging.info("PRUEBA 1 SUPERADA: CONEXIÓN A LA BD EXITOSA.")

    def test_insertar_y_obtener_equipo(self):
        # SEGUNDA PRUEBA VERIFICA QUE AL GUARDAR UN EQUIPO LUEGO APAREZCA EN LA LISTA
        self.db.insertar_equipo("EQUIPO FANTASMA", "SENIOR", 1)

        equipos = self.db.obtener_equipos()

        # COMPRUEBO QUE AL MENOS ME HA DEVUELTO UN EQUIPO
        self.assertTrue(len(equipos) > 0, "LA LISTA ESTÁ VACÍA.")

        # COMPRUEBO QUE EL EQUIPO FANTASMA ESTÁ EN LA LISTA
        nombres = [equipo[1] for equipo in equipos]
        self.assertIn("EQUIPO FANTASMA", nombres, "EL EQUIPO NO SE GUARDÓ CORRECTAMENTE.")
        logging.info("PRUEBA 2 SUPERADA: INSERCIÓN Y LECTURA DE EQUIPOS EN LA BD CORRECTA.")

    def tearDown(self):
        """
        LIMPIA EL TERRENO DESPUÉS DE CADA TEST
        """
        self.db.conexion.close()
        if os.path.exists("bd_de_prueba.db"):
            os.remove("bd_de_prueba.db")


if __name__ == '__main__':
    logging.info("INICIANDO PRUEBAS ")
    unittest.main()