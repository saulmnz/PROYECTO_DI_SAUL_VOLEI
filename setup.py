from setuptools import setup, find_packages

setup(
    name="GESTOR_VOLEIBOL",
    version="1.0",
    description="SISTEMA DE GESTIÓN DE EQUIPOS Y JUGADORES DE VOLEIBOL",
    author="SAÚL",
    py_modules=["main", "conexionBD"],
    packages=["ventanas"],
    install_requires=[
        "PyGObject"
    ],
    entry_points={
        'console_scripts': [
            'iniciar-volei=main:main',
        ],
    },
)