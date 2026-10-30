"""Ejemplos de uso del lector.

Se ejecuta con el botón ▷ de Positron, o con `python ejemplos.py` desde la terminal.
Cada ejemplo muestra lo que devuelve el lector y, abajo, lo que se esperaba.
"""

import os
from pathlib import Path

from lector.seleccion import leer_tabla

CARPETA = Path(__file__).parent  # la carpeta de este archivo, donde están los datos

NIVELES = CARPETA / "niveles.csv"      # separado por comas, con encabezado
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
    mostrar("Tipos adivinados", "oficial bool, tier int, full_clear bool, condicion None",
            NIVELES, n_filas=2)
    mostrar("Tipo elegido por el usuario", "tier queda como texto: '13' y '12'",
            NIVELES, n_filas=2, tipos={"tier": str}, columnas=["nombre", "tier"])
    mostrar("Línea vacía y coma entre comillas",
            "Superposition, Kero Summit y Last Night con 'sin morir, todos los lados'",
            NIVELES, rango=(4, 6), columnas=["nombre", "condicion"])
    mostrar("Celda vacía", "personaje_2 None",
            LUGARES, rango=(2, 2), separador=";", columnas=["lugar", "personaje_2"])
    mostrar("Separado por espacios y sin encabezado", "columnas columna_1 a columna_4",
            EMPLEADOS, n_filas=2, separador=None, encabezado=False)
    mostrar("Encabezado con una columna repetida y otra sin nombre",
            "personaje_2 y columna_7, con un aviso por cada una",
            LUGARES, n_filas=2, separador=";")

    print("\n----- Selección -----")
    mostrar("Tier 10 o más, solo nombre y tier (como el ejemplo de la consigna)",
            "The Summit B-Hell Side, Glyph D Side, Forsaken Undercity y Superposition",
            NIVELES, columnas=["nombre", "tier"], filtro=lambda fila: fila["tier"] >= 10)
    mostrar("De las filas 5 a 15, las 2 primeras oficiales",
            "The Summit C-Side y Core C-Side",
            NIVELES, rango=(5, 15), filtro=lambda fila: fila["oficial"], n_filas=2,
            columnas=["nombre", "tier"])

    print("\n----- Errores -----")
    mostrar_error("Columna que no existe", NIVELES, columnas=["autor"])
    mostrar_error("Rango que termina antes de empezar", NIVELES, rango=(5, 2))
    mostrar_error("Filtro que falla con una celda vacía",
                  NIVELES, filtro=lambda fila: "sin morir" in fila["condicion"])
    mostrar_error("Valor que no se puede convertir al tipo pedido",
                  NIVELES, tipos={"nombre": int})
    mostrar_error("Filas con distinta cantidad de campos", LUGARES, separador=",")
    mostrar_error("Archivo que no existe", CARPETA / "no_existe.csv")

    with open(VACIO, "w", encoding="utf-8") as archivo:
        archivo.write("")
    mostrar_error("Archivo vacío", VACIO)
    os.remove(VACIO)
