"""Ejemplos de uso del lector.

Se ejecuta con el botón de ejecutar de Positron, o con `python ejemplos.py` desde la terminal.
Cada ejemplo muestra lo que devuelve el lector y, abajo, lo que se esperaba.
"""

import os
from pathlib import Path

from lector.seleccion import leer_tabla

CARPETA = Path(__file__).parent  # la carpeta de este archivo, donde están los datos

RETOS = CARPETA / "retos.csv"          # separado por comas, con encabezado
EMPLEADOS = CARPETA / "empleados.txt"  # separado por espacios, sin encabezado
LUGARES = CARPETA / "lugares.csv"      # separado por punto y coma, guardado con Excel
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
    mostrar("Tipos adivinados", "tier int, etiquetas str y None donde está vacía",
            RETOS, n_filas=2)
    mostrar("Tipo elegido por el usuario", "tier queda como texto: '13' y '12'",
            RETOS, n_filas=2, tipos={"tier": str}, columnas=["reto", "tier"])
    mostrar("Línea vacía y coma entre comillas",
            "The Summit C-Side y Destro's Compact Sides con 'All Chapters, FC'",
            RETOS, rango=(8, 9), columnas=["reto", "etiquetas"])
    mostrar("Celda vacía", "etiquetas None",
            RETOS, rango=(2, 2), columnas=["reto", "etiquetas"])
    mostrar("Separado por espacios y sin encabezado",
            "columnas columna_1 a columna_5, columna_4 float porque tiene 40 y 37.5, columna_5 bool",
            EMPLEADOS, n_filas=2, separador=None, encabezado=False)
    mostrar("Encabezado con una columna repetida y otra sin nombre",
            "personaje_2 y columna_7, con un aviso por cada una",
            LUGARES, n_filas=2, separador=";")

    print("\n----- Selección -----")
    mostrar("Tier 10 o más, solo reto y tier (como el ejemplo de la consigna)",
            "The Summit B-Hell Side, Glyph D Side, Forsaken Undercity y Superposition",
            RETOS, columnas=["reto", "tier"], filtro=lambda fila: fila["tier"] >= 10)
    mostrar("De las filas 5 a 15, las 2 primeras de tier 5 o menos",
            "Reflection C-Side y Mirror Temple C-Side",
            RETOS, rango=(5, 15), filtro=lambda fila: fila["tier"] <= 5, n_filas=2,
            columnas=["reto", "tier"])

    print("\n----- Errores -----")
    mostrar_error("Columna que no existe", RETOS, columnas=["autor"])
    mostrar_error("Rango que termina antes de empezar", RETOS, rango=(5, 2))
    mostrar_error("Filtro que falla con una celda vacía",
                  RETOS, filtro=lambda fila: "FC" in fila["etiquetas"])
    mostrar_error("Valor que no se puede convertir al tipo pedido",
                  RETOS, tipos={"reto": int})
    mostrar_error("Filas con distinta cantidad de campos", LUGARES, separador=",")
    mostrar_error("Archivo que no existe", CARPETA / "no_existe.csv")

    with open(VACIO, "w", encoding="utf-8") as archivo:
        archivo.write("")
    mostrar_error("Archivo vacío", VACIO)
    os.remove(VACIO)
