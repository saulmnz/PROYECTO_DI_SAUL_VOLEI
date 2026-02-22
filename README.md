# `GESTOR DE EQUIPOS DE VOLEIBOL` 🏐

![img](https://i.pinimg.com/originals/15/1c/ee/151ceebcc0ad1e1665c4b723dfe8e276.gif)

---

## `ESTRUCTURA DEL PROYECTO` ⭕

>[!NOTE]
>***EL PROYECTO SIGUE UNA ARQUITECTURA MODULAR QUE SEPARA LA LÓGICA DE NEGOCIO, LA INTERFAZ GRÁFICA Y LA DOCUMENTACIÓN***

```text
Proyecto_Voleibol/
│
├── main.py                 # PUNTO DE ENTRADA PRINCIPAL DE LA APLICACIÓN
├── main.spec               # ARCHIVO DE CONFIGURACIÓN DE PyInstaller.
├── conexionBD.py           # LÓGICA DE CONEXIÓN Y CONSULTAS A LA BASE DE DATOS SQLITE
├── voleibol.db             # BASE DE DATOS SQLITE
├── setup.py                # ARCHIVO DE CONFIGURACIÓN PARA DISTRIBUCIÓN DE PYTHON
├── registro_tests.log      # REGISTRO DE LOGS PARA LOS RESULTADOS DE LOS TESTS
│
├── ventanas/               # MÓDULOS DE LA INTERFAZ GRÁFICA
│   ├── ventana_principal.py
│   ├── ventana_equipos.py
│   ├── ventana_jugadores.py
│   └── ventana_partidos.py
│
├── tests/                  # PRUEBAS UNITARIAS
│   └── test_bd.py          
│
├── img/                    # EL GIF QUE LE PUSE.
│
├── dist/                   # VERSIÓN EMPAQUETADO (Ejecutable)
│   └── main/               # CARPETA CON EL PROGRAMA LISTO PARA USAR SIN PYTHON.
│
└── docs/                   # DOCUMENTACIÓN OFICIAL GENERADA POR SPHYNX.
    ├── source/             # ARCHIVOS FUENTE (.rst y conf.py).
    └── build/html/         # WEB CON LA DOCUMENTACIÓN OFICIAL
```

---

## `DESCRIPCIÓN DE ARCHIVOS` 🔻

### `MAIN.PY` 🔺

>[!TIP]
>***Es el motor de arranque del programa. Se encarga de inicializar la aplicación, cargar la interfaz gráfica principal y mantener el bucle de eventos activo.***

---

### `CONEXIONBD.PY` 🔺

>[!TIP]
>***Gestiona toda la comunicación entre aplicación y base de datos `voleibol.db`. Maneja las operaciones CRUD ⚠️⚠️***

**`MÉTODOS CLAVE`:**
- ***`conectar()`: Establece y devuelve la conexión con SQLite.***
- ***`crear_tablas()`: Genera la estructura inicial si la BD está vacía***
- ***`insertar_equipo`, `insertar_jugador()`,`insertar_partido()`: Añaden nuevos registros a la base de datos en cada una de las tablas especificadas***
- ***`actualizar_equipo()`,`eliminar_jugador()`,`eliminar_partido()...`: Modifican o borran datos existentes en la BD***

---

### `VENTANAS/` 🔺

>[!TIP]
>***Contiene la lógica de distintas pantallas de la aplicación. Cada archivo maneja los eventos de los botones, las tablas y los formularios de su respectiva sección, conectando las acciones del usuario con los métodos de `conexionBD.py`***

- ***`ventana_principal.py`: Actúa como el menú central (Dashboard). Contiene los botones de navegación (`Gtk.Button`) que, al ser pulsados, instancian y abren las ventanas secundarias.***
  * ***Métodos clave: `abrir_equipos()`, `abrir_jugadores()`, `abrir_partidos()`.***

- ***`ventana_equipos.py`: Permite gestionar los clubes. Utiliza campos de texto (`Gtk.Entry`) para introducir el nombre y ciudad del equipo. Para mostrar los datos guardados, emplea una tabla interactiva (`Gtk.TreeView`) conectada a un modelo de datos (`Gtk.ListStore`).***
  - ***Métodos clave: `cargar_datos_tabla()` (Refresca el TreeView consultando a la BD), `on_guardar_clicked()` (Captura el texto de los Entry y llama a `insertar_equipo()`).***

- ***`ventana_jugadores.py`: Diseñada para registrar a los deportistas. Destaca el uso de **ComboBoxes** (`Gtk.ComboBoxText`), los cuales se rellenan dinámicamente haciendo una consulta a la tabla de Equipos. De esta forma, el usuario no escribe el equipo a mano, sino que lo selecciona de una lista desplegable, evitando errores de integridad referencial.***
  - ***Métodos clave: `cargar_combobox_equipos()`, `limpiar_formularios()`, `on_eliminar_clicked()` (Captura el ID de la fila seleccionada en el TreeView para borrarla).***
    
- ***`ventana_partidos.py`: Gestiona los encuentros. Utiliza dos ComboBoxes distintos (uno para el Equipo Local y otro para el Equipo Visitante) y campos de entrada numéricos o de texto para el resultado.***

>[!IMPORTANT]
>***`CONTROL DE ERRORES Y VALIDACIÓN`: Las ventanas incorporan manejo de excepciones. Se validan las entradas del usuario (inputs) para evitar cuelgues si se dejan campos obligatorios vacíos o si se introducen formatos incorrectos, mostrando avisos en lugar de romper la ejecución.***

---

### `TESTS/` (`test_bd.py`) 🔺

>[!TIP]
>***Contiene las pruebas unitarias para garantizar que las consultas a la base de datos funcionan correctamente antes de integrar los cambios en la interfaz. El resultado de estas pruebas se guarda automáticamente en `registro_tests.log`.***

- ***Métodos clave: `setUp()` (Prepara una base de datos temporal en memoria), `test_insertar_jugador()`, `tearDown()` (Limpia la base de datos tras la prueba).***

<img width="800" height="100" alt="image" src="https://github.com/user-attachments/assets/3d13762f-c168-457f-9afa-0d8c1ea9c470" />

---

## `LIBRERÍAS UTILIZADAS` 🔻

- ***`PyGObject (GTK)`: Es la librería principal utilizada para construir toda la interfaz gráfica de usuario (GUI). Proporciona los contenedores (`Gtk.Box`, `Gtk.Grid`) y los widgets (`Entry`, `ComboBoxText`, `TreeView`, `Button`) que componen las ventanas.***
  
- ***`SQLite3`: Motor de base de datos ligero y local. Se conecta con GTK a través de `conexionBD.py` para rellenar los TreeViews y ComboBoxes con información persistente.***
  
- ***`Unittest / Logging`: Usadas en `test_bd.py` para automatizar las pruebas del código y registrar los resultados en un archivo `.log`.***
  
- ***`Setuptools`: Utilizada en `setup.py` para empaquetar el proyecto bajo el estándar de Python.***
  
- ***`PyInstaller`: Herramienta utilizada para congelar el código Python y las librerías de GTK en un ejecutable independiente (standalone).***
  
- ***`Sphinx & PyStemmer`: Librerías externas utilizadas para extraer los *docstrings* (comentarios) del código y compilar la página web navegable del manual técnico.***

---

---

## `PROCESO DE EMPAQUETADO` 🔻

>[!NOTE]
>***PARA ASEGURAR QUE LA APLICACIÓN PUEDA SER DISTRIBUIDA, INSTALADA Y EJECUTADA EN CUALQUIER EQUIPO SIN COMPLICACIONES DE DEPENDENCIAS, HE IMPLEMENTADO DOS METODOLOGÍAS DE EMPAQUETADO***

### `EMPAQUETADO COMO PAQUETE DE PYTHON (SETUP.PY)` 🔺

- ***Este método está orientado a desarrolladores o entornos que ya cuentan con Python.***
- ***Se creó un script `setup.py` utilizando la librería `setuptools`.***
- ***En él se definieron los metadatos esenciales (nombre, versión, autor) y se utilizó `[ventanas]` para ubicar el código de la interfaz.***
- ***Ventaja/Uso: Al ejecutar `pip install .` en el directorio raíz, el gestor de paquetes de Python lee el `setup.py`, resuelve las dependencias automáticamente, y compila la carpeta `.egg-info`. Esto convierte nuestro proyecto en una librería o módulo instalable en cualquier entorno virtual.***

>***USANDO EL COMANDO `pip install .` CON ANTELACIÓN:***
<img width="950" height="500" alt="image" src="https://github.com/user-attachments/assets/422fb76f-c431-48db-a3a8-14d13f29f1bc" />



### `EMPAQUETADO COMO EJECUTABLE INDEPENDIENTE (PYINSTALLER)` 🔺

- ***Este método está pensado para el usuario final que no tiene Python ni librerías gráficas instaladas en su sistema.***
- ***Se utilizó la herramienta externa `PyInstaller`. Inicialmente se lanzó el comando base, pero para asegurar que el ejecutable incluyera los recursos externos, se configuró y ajustó el archivo `main.spec`.***
- ***En el archivo `.spec`, se modificó la variable `datas=[]` para incluir explícitamente la carpeta de imágenes (`img/`) y asegurarse de que la base de datos local (`voleibol.db`) viajara junto al ejecutable.***
- ***Se optó por el formato de salida en un solo directorio (`--onedir`) en lugar de un solo archivo. Esto genera la carpeta `dist/main/`, que arranca mucho más rápido y contiene todas las librerías dinámicas (`.so` / `.dll`) y dependencias (como GTK y SQLite) precompiladas.***

<img width="250" height="100" alt="image" src="https://github.com/user-attachments/assets/abfb9800-b4b2-4825-900a-0e2db0dc2037" />

<img width="925" height="500" alt="image" src="https://github.com/user-attachments/assets/815a5868-39e4-4b4e-bb4b-c0a7fe734133" />


---

## `DOCUMENTACIÓN (DOCSTRINGS Y SPHINX)` 🔺

>[!NOTE]
>***EL PROYECTO CUENTA CON UNA DOCUMENTACIÓN TÉCNICA AUTOGENERADA, IMPLEMENTADA EN DOS FASES INTERCONECTADAS:***

### `FASE 1: COMENTARIOS ESTRUCTURADOS (DOCSTRINGS)` 🔺

- ***Todas las clases y métodos de la lógica de negocio (como `conexionBD.py`) y de la interfaz gráfica (`ventanas`) han sido documentados directamente en el código fuente mediante comentarios.***
  
- ***Se ha utilizado el estándar de docstrings de Python, detallando el propósito de cada función, los parámetros de entrada esperados (`Args:`) y el tipo de dato devuelto (`Returns:`).***

### `FASE 2: GENERACIÓN WEB DINÁMICA CON SPHINX` 🔺

- ***Configuración del entorno (`conf.py`): Se inicializó Sphinx en la carpeta `docs/`. Para que Sphinx pudiera "leer" el código de las carpetas superiores, se inyectó la ruta del proyecto en el sistema mediante `sys.path.insert(0, os.path.abspath('../../'))`.***
  
- ***Extensión Autodoc: Se activó la extensión `sphinx.ext.autodoc`, la cual importa los módulos de Python en segundo plano y extrae automáticamente los docstrings que escribimos en la Fase 1.***
  
- ***Mapeo del proyecto (`sphinx-apidoc`): Se ejecutó este comando para escanear todos nuestros archivos `.py` (omitiendo entornos virtuales) y generar los archivos "plano" en formato reStructuredText (`.rst`).***
  
- ***Soporte de Búsqueda en Español (`PyStemmer`): Al configurar el idioma del manual en español (`es`), Sphinx requería un motor de indexación de palabras específico para crear la barra de búsqueda rápida. Se instaló la librería `PyStemmer` para resolver la tokenización del idioma.***
  
- ***Construcción Final (`sphinx-build`): Finalmente, se compiló el proyecto a formato HTML dentro de `docs/build/html/`.***

>***COMANDOS UTILIZADOS***

```bash
> sphinx-quickstart docs
> sphinx-apidoc -o docs/source/ . .venv dist build GESTOR_VOLEIBOL.egg-info tests
> pip install PyStemmer
> python -m sphinx -b html docs/source docs/build/html
```

<img width="900" height="400" alt="image" src="https://github.com/user-attachments/assets/0e86f020-85b8-47ef-b2c5-37e55a0856b3" />


---

## `GUÍA DE USO RÁPIDO` 🔻

### `¿CÓMO EJECUTAR EL PROGRAMA?` 🔺

>[!CAUTION]
>***No necesitas instalar Python, ni IDEs, ni configurar variables de entorno para usar el programa.***

- ***Navega hasta la carpeta empaquetada: `dist/main/`.***
- ***Haz doble clic en el archivo ejecutable llamado `main`.***
- ***Nota sobre la Base de Datos: Si es la primera vez que lo abres o si borras el archivo `voleibol.db`, el programa detectará su ausencia y, gracias al método `crear_tablas()`, generará una base de datos nueva y limpia automáticamente de forma transparente.***

### `FLUJO DE TRABAJO RECOMENDADO EN LA APLICACIÓN` 🔺

>[!TIP]
>***Para mantener la integridad de los datos (debido a las llaves foráneas y los ComboBoxes), recomiendo seguir este orden al introducir información:***

- ***Ve a la pestaña "Equipos": Registra al menos un par de equipos (Ej: Club Vigo Voleibol, Oleiros, Calasancias).***
- ***Ve a la pestaña "Jugadores": Ahora, al crear un jugador, el desplegable te permitirá asignarlo a los equipos que creaste en el paso anterior.***
- ***Ve a la pestaña "Partidos": Selecciona los equipos locales y visitantes desde los desplegables y registra sus resultados.***

### `¿CÓMO CONSULTAR EL MANUAL TÉCNICO (DESARROLLADORES)?` 🔺

>[!TIP]
>***Si eres un desarrollador y quieres explorar la arquitectura del código fuente:***

1. ***Navega hasta la carpeta: `docs/build/html/`.***
2. ***Abre el archivo principal `index.html` con cualquier navegador web (Chrome, Firefox, Safari).***
3. ***Navega por el índice lateral (`Módulos`) o utiliza la barra de "Búsqueda Rápida" para encontrar instantáneamente cualquier función o clase del proyecto.***

---

### `CAPTURAS DEL FUNCIONAMIENTO` ⭕

<img width="700" height="450" alt="image" src="https://github.com/user-attachments/assets/09ed5e4a-85e7-491f-afc5-7fbd69ee880b" />

<img width="700" height="450" alt="image" src="https://github.com/user-attachments/assets/2920c880-f47b-4a35-8bf1-9f0fd8a17156" />

<img width="700" height="450" alt="image" src="https://github.com/user-attachments/assets/4fb19fcc-25b9-48d6-8d87-e7379ec2bd43" />

