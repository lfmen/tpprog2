"""Ejemplos de uso del lector.

Se ejecuta con el botón de ejecutar de Positron, o con `python ejemplos.py` desde la terminal.
Cada ejemplo muestra lo que devuelve el lector y, abajo, lo que se esperaba.
"""

import os
from pathlib import Path

from lector.seleccion import leer_tabla

CARPETA = Path(__file__).parent  # la carpeta de este archivo, donde están los datos

CHALLENGES = CARPETA / "challenges.csv"  # separado por comas, con encabezado
EMPLEADOS = CARPETA / "empleados.txt"    # separado por espacios, sin encabezado
LUGARES = CARPETA / "lugares.csv"        # separado por punto y coma, guardado con Excel
VACIO = CARPETA / "vacio.csv"            # se crea y se borra en el ejemplo de archivo vacío


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
    mostrar("Tipos adivinados", "Tier int, Challenge Name y First Clear URL str",
            CHALLENGES, n_filas=2)
    mostrar("Tipo elegido por el usuario", "Tier queda como texto: '13' y '12'",
            CHALLENGES, n_filas=2, tipos={"Tier": str}, columnas=["Tier", "Challenge Name"])
    mostrar("Separado por espacios y sin encabezado",
            "columna_1 a columna_5, columna_4 float (tiene 40 y 37.5) y columna_5 bool",
            EMPLEADOS, n_filas=2, separador=None, encabezado=False)
    mostrar("Línea vacía y espacios entre comillas",
            "Diego López y Elena Martínez, con 'Recursos Humanos' en un solo campo",
            EMPLEADOS, rango=(4, 5), separador=None, encabezado=False)
    mostrar("Encabezado con una columna repetida y otra sin nombre",
            "personaje_2 y columna_7, con un aviso por cada una",
            LUGARES, n_filas=2, separador=";")
    mostrar("Celda vacía", "personaje_2 None",
            LUGARES, rango=(2, 2), separador=";", columnas=["lugar", "personaje_2"])

    print("\n----- Selección -----")
    mostrar("Tier 11 o más, solo nombre y tier (como el ejemplo de la consigna)",
            "The Summit B-Hell Side, Glyph D Side y los tres de tier 11",
            CHALLENGES, columnas=["Challenge Name", "Tier"], filtro=lambda fila: fila["Tier"] >= 11)
    mostrar("De las filas 10 a 40, las 2 primeras con [FC] en el nombre",
            "Destro's Compact Sides y Motivation",
            CHALLENGES, rango=(10, 40), filtro=lambda fila: "[FC]" in fila["Challenge Name"],
            n_filas=2, columnas=["Challenge Name", "Tier"])

    print("\n----- Errores -----")
    mostrar_error("Columna que no existe", CHALLENGES, columnas=["autor"])
    mostrar_error("Rango que termina antes de empezar", CHALLENGES, rango=(5, 2))
    mostrar_error("Filtro que falla con una celda vacía",
                  LUGARES, separador=";", filtro=lambda fila: len(fila["personaje_2"]) > 3)
    mostrar_error("Valor que no se puede convertir al tipo pedido",
                  CHALLENGES, tipos={"Challenge Name": int})
    mostrar_error("Filas con distinta cantidad de campos", LUGARES, separador=",")
    mostrar_error("Archivo que no existe", CARPETA / "no_existe.csv")

    with open(VACIO, "w", encoding="utf-8") as archivo:
        archivo.write("")
    mostrar_error("Archivo vacío", VACIO)
    os.remove(VACIO)
