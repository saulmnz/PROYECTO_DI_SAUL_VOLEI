import sqlite3
from sqlite3 import Error

class ConexionBD:

    """
        CLASE PARA GESTIONAR LA CONEXIÓN A SQLITE.
        SE ENCARGA DE CREAR LAS TABLAS SOBRE LAS QUE VAMOS A OPERAR.
    """

    def __init__(self):
        # RUTA DE LA BASE DE DATOS LOCAL
        self.ruta_bd = "voleibol.db"
        # MÉTODO PARA CONECTAR A LA BD
        self.conexion = self.conectar()
        # MÉTODO PARA CREAR LAS TABLAS
        self.crear_tablas()

    def conectar(self):
        """
        CONEXIÓN CON LA BASE DE DATOS.
        """
        try:
            # CONECTA O CREA LA BASE DE DATOS
            conexion = sqlite3.connect(self.ruta_bd)
            # ACTIVAMOS LAS CLAVES FORÁNEAS (NECESARIO EN SQLITE PARA QUE FUNCIONEN)
            conexion.execute("PRAGMA foreign_keys = ON")
            return conexion
        except Error as e:
            print(f"ERROR CONECTADO A LA BASE DE DATOSS: {e}")
            return None

    def crear_tablas(self):
        """
        CREA LAS TABLAS EN LA BASE DE DATOS
        """
        if self.conexion is not None:
            try:
                cursor = self.conexion.cursor()
                # TABLA EQUIPOS
                cursor.execute('''
                               CREATE TABLE IF NOT EXISTS equipos (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   nombre TEXT NOT NULL,
                                   categoria TEXT NOT NULL,
                                   federado BOOLEAN NOT NULL
                               )
                               ''')
                # TABLA JUGADORES CON CLAVE FORÁNEA A EQUIPOS
                cursor.execute('''
                               CREATE TABLE IF NOT EXISTS jugadores (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   nombre_completo TEXT NOT NULL,
                                   dorsal INTEGER NOT NULL,
                                   posicion TEXT NOT NULL,
                                   id_equipo INTEGER,
                                   FOREIGN KEY (id_equipo) REFERENCES equipos (id) ON DELETE CASCADE
                               )
                               ''')
                # TABLA PARTIDOS (CON DOS CLAVES FORÁNEAS A EQUIPOS)
                cursor.execute('''
                               CREATE TABLE IF NOT EXISTS partidos (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   id_equipo_local INTEGER NOT NULL,
                                   id_equipo_visitante INTEGER NOT NULL,
                                   resultado TEXT NOT NULL,
                                   FOREIGN KEY (id_equipo_local) REFERENCES equipos (id) ON DELETE CASCADE,
                                   FOREIGN KEY (id_equipo_visitante) REFERENCES equipos (id) ON DELETE CASCADE
                               )
                               ''')
                # GUARDAMOS LOS CAMBIOS EN LA BASE DE DATOS
                self.conexion.commit()
                print("CONEXIÓN Y VERIFICACIÓN DE TABLAS OK!!")
            except Error as e:
                print(f"ERROR AL CREAR LAS TABLAS!!!: {e}")

    # OPERACIONES CRUD PARA EQUIPOS
    def insertar_equipo(self, nombre, categoria, federado):
        sql = ''' INSERT INTO equipos(nombre, categoria, federado) VALUES(?,?,?) '''
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, (nombre, categoria, federado))
            self.conexion.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"ERROR AL INSERTAR EQUIPO!!!!: {e}")
            return None

    def obtener_equipos(self):
        sql = ''' SELECT * FROM equipos '''
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"ERROR AL OBTENER EQUIPOS!!!!: {e}")
            return []

    def actualizar_equipo(self, id_equipo, nombre, categoria, federado):
        sql = ''' UPDATE equipos SET nombre = ?, categoria = ?, federado = ? WHERE id = ?'''
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, (nombre, categoria, federado, id_equipo))
            self.conexion.commit()
        except Error as e:
            print(f"ERROR AL ACTUALIZAR EQUIPOOO!!: {e}")

    def eliminar_equipo(self, id_equipo):
        sql = ''' DELETE FROM equipos WHERE id = ? '''
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, (id_equipo,))
            self.conexion.commit()
        except Error as e:
            print(f"ERROORCH AL ELIMINAR EQUIPO: {e}")

    # OPERACIONES CRUD PARA JUGADORES
    def insertar_jugador(self, nombre, dorsal, posicion, id_equipo):
        sql = ''' INSERT INTO jugadores(nombre_completo, dorsal, posicion, id_equipo) VALUES(?,?,?,?) '''
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, (nombre, dorsal, posicion, id_equipo))
            self.conexion.commit()
        except Error as e:
            print(f"ERROR AL INSERTAR JUGADOR!!!: {e}")

    def obtener_jugadores(self):
        """
        RECUPERA LOS JUGADORES HACIENDO UN JOIN PARA OBTENER EL NOMBRE DEL EQUIPO.
        """
        sql = ''' SELECT j.id, j.nombre_completo, j.dorsal, j.posicion, e.nombre 
                  FROM jugadores j INNER JOIN equipos e ON j.id_equipo = e.id '''
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"ERROR AL OBTENER JUGADORES!!!!: {e}")
            return []

    def eliminar_jugador(self, id_jugador):
        sql = ''' DELETE FROM jugadores WHERE id = ? '''
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, (id_jugador,))
            self.conexion.commit()
        except Error as e:
            print(f"ERROR AL ELIMINAR JUGADOR: {e}")

    # OPERACIONES CRUD PARA PARTIDOS
    def insertar_partido(self, id_local, id_visitante, resultado):
        sql = ''' INSERT INTO partidos(id_equipo_local, id_equipo_visitante, resultado) VALUES(?,?,?) '''
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, (id_local, id_visitante, resultado))
            self.conexion.commit()
        except Error as e:
            print(f"ERROR AL INSERTAR PARTIDO!!: {e}")

    def obtener_partidos(self):
        """
        RECUPERA LOS PARTIDOS CRUZANDO CON LA TABLA EQUIPOS DOS VECES (LOCAL Y VISITANTE).
        """
        sql = ''' SELECT p.id, e1.nombre, e2.nombre, p.resultado 
                  FROM partidos p 
                  INNER JOIN equipos e1 ON p.id_equipo_local = e1.id 
                  INNER JOIN equipos e2 ON p.id_equipo_visitante = e2.id '''
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Error as e:
            print(f"ERROR AL OBTENER PARTIDOS!!!!: {e}")
            return []

    def eliminar_partido(self, id_partido):
        sql = ''' DELETE FROM partidos WHERE id = ? '''
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, (id_partido,))
            self.conexion.commit()
        except Error as e:
            print(f"ERROR AL ELIMINAR PARTIDO: {e}")

if __name__ == "__main__":
    db = ConexionBD()