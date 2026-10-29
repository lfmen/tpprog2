"""Ejemplos de uso del lector.

Se ejecuta con el botón ▷ de Positron, o con `python ejemplos.py` desde la terminal.
Cada ejemplo muestra lo que devuelve el lector y, abajo, lo que se esperaba.
"""

import os
from pathlib import Path

from lector.seleccion import leer_tabla

CARPETA = Path(__file__).parent  # la carpeta de este archivo, donde están los datos

PRODUCTOS = CARPETA / "productos.csv"  # separado por comas, con encabezado
EMPLEADOS = CARPETA / "empleados.txt"  # separado por espacios, sin encabezado
CLIENTES = CARPETA / "clientes.csv"    # separado por punto y coma, guardado con Excel
VACIO = CARPETA / "vacio.csv"          # se crea y se borra en el ejemplo de archivo vacío


def mostrar(titulo, esperado, ruta, **opciones):
    """Lee la tabla con las opciones pedidas y muestra cada fila y lo que se esperaba."""
    print("\n" + titulo)
    for fila in leer_tabla(ruta, **opciones):
        print("  ", fila)
    print("   Esperado:", esperado)


def mostrar_error(titulo, ruta, **opciones):
    """Lee la tabla con opciones que tienen que fallar y muestra el mensaje de error."""
    print("\n" + titulo)
    try:
        leer_tabla(ruta, **opciones)
    except Exception as error:
        print("  ", error)


if __name__ == "__main__":
    print("----- Lectura y tipos -----")
    mostrar("Tipos adivinados", "precio float, stock int, calificacion float, importado bool",
            PRODUCTOS, n_filas=2)
    mostrar("Tipo elegido por el usuario", "stock queda como texto: '12' y '80'",
            PRODUCTOS, n_filas=2, tipos={"stock": str}, columnas=["nombre", "stock"])
    mostrar("Línea vacía y coma entre comillas", "Mochila urbana y Lámpara de escritorio, LED",
            PRODUCTOS, rango=(3, 4), columnas=["nombre"])
    mostrar("Celda vacía", "calificacion None",
            PRODUCTOS, rango=(6, 6), columnas=["nombre", "calificacion"])
    mostrar("Separado por espacios y sin encabezado", "columnas columna_1 a columna_4",
            EMPLEADOS, n_filas=2, separador=None, encabezado=False)
    mostrar("Encabezado con una columna repetida y otra sin nombre",
            "telefono_2 y columna_6, con un aviso por cada una",
            CLIENTES, n_filas=2, separador=";")

    print("\n----- Selección -----")
    mostrar("Menos de 10 unidades, solo nombre y precio (el ejemplo de la consigna)",
            "Teclado mecánico, 62000.0",
            PRODUCTOS, columnas=["nombre", "precio"], filtro=lambda fila: fila["stock"] < 10)
    mostrar("De las filas 4 a 10, las 2 primeras de menos de 10000",
            "Taza de cerámica y Lapicera de gel",
            PRODUCTOS, rango=(4, 10), filtro=lambda fila: fila["precio"] < 10000, n_filas=2,
            columnas=["nombre", "precio"])

    print("\n----- Errores -----")
    mostrar_error("Columna que no existe", PRODUCTOS, columnas=["marca"])
    mostrar_error("Rango que termina antes de empezar", PRODUCTOS, rango=(5, 2))
    mostrar_error("Filtro que falla con una celda vacía",
                  PRODUCTOS, filtro=lambda fila: fila["calificacion"] > 4)
    mostrar_error("Valor que no se puede convertir al tipo pedido",
                  PRODUCTOS, tipos={"nombre": int})
    mostrar_error("Filas con distinta cantidad de campos", CLIENTES, separador=",")
    mostrar_error("Archivo que no existe", CARPETA / "no_existe.csv")

    with open(VACIO, "w", encoding="utf-8") as archivo:
        archivo.write("")
    mostrar_error("Archivo vacío", VACIO)
    os.remove(VACIO)
