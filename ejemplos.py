"""Ejemplos de uso del lector. Se corre desde esta carpeta con:

    python ejemplos.py

Usa los tres archivos que están al lado:
    productos.csv  separado por comas, con encabezado, comillas y una celda vacía
    empleados.txt  separado por espacios, sin encabezado, con comillas
    clientes.csv   separado por punto y coma, guardado con Excel, con el encabezado mal armado
"""

import warnings

from lector.seleccion import leer_tabla

PRODUCTOS = "productos.csv"
EMPLEADOS = "empleados.txt"
CLIENTES = "clientes.csv"


def mostrar(titulo, filas):
    print("\n" + titulo)
    for fila in filas:
        print("  ", fila)


def mostrar_error(titulo, lectura):
    # lectura es una función sin argumentos que llama al lector y tiene que fallar
    print("\n" + titulo)
    try:
        lectura()
    except Exception as error:
        print(f"   {type(error).__name__}: {error}")


def main():
    print("=" * 70 + "\nLectura y tipos\n" + "=" * 70)
    mostrar("Las primeras 3 filas, con el tipo de cada columna adivinado",
            leer_tabla(PRODUCTOS, n_filas=3))
    mostrar("Un tipo elegido por el usuario manda sobre el adivinado",
            leer_tabla(PRODUCTOS, tipos={"stock": str}, columnas=["nombre", "stock"], n_filas=3))
    mostrar("Separado por espacios y sin encabezado: las columnas se numeran",
            leer_tabla(EMPLEADOS, separador=None, encabezado=False, n_filas=3))

    with warnings.catch_warnings(record=True) as avisos:
        warnings.simplefilter("always")
        filas = leer_tabla(CLIENTES, separador=";", n_filas=3)
    mostrar("Separado por punto y coma, con una columna repetida y otra sin nombre", filas)
    for aviso in avisos:
        print("   aviso:", aviso.message)

    print("\n" + "=" * 70 + "\nSelección\n" + "=" * 70)
    mostrar("Importados con 4.6 o más (filtra por columnas que no se muestran)",
            leer_tabla(PRODUCTOS, columnas=["nombre", "precio"],
                       filtro=lambda fila: fila["importado"] and fila["calificacion"] >= 4.6))
    mostrar("Filas 4 a 10, solo las de menos de $10000, y de esas las primeras 2",
            leer_tabla(PRODUCTOS, rango=(4, 10), filtro=lambda fila: fila["precio"] < 10000,
                       n_filas=2, columnas=["nombre", "precio"]))
    mostrar("Empleados que trabajan desde su casa",
            leer_tabla(EMPLEADOS, separador=None, encabezado=False,
                       filtro=lambda fila: fila["columna_4"], columnas=["columna_1", "columna_3"]))

    print("\n" + "=" * 70 + "\nErrores\n" + "=" * 70)
    mostrar_error("Una columna que no existe:", lambda: leer_tabla(PRODUCTOS, columnas=["marca"]))
    mostrar_error("Un rango que termina antes de empezar:", lambda: leer_tabla(PRODUCTOS, rango=(5, 2)))
    mostrar_error("Un filtro que falla con la calificación vacía:",
                  lambda: leer_tabla(PRODUCTOS, filtro=lambda fila: fila["calificacion"] > 4))
    mostrar_error("Un tipo que no se puede aplicar:", lambda: leer_tabla(PRODUCTOS, tipos={"nombre": int}))
    mostrar_error("El separador equivocado:", lambda: leer_tabla(CLIENTES, separador=","))
    mostrar_error("Un archivo que no existe:", lambda: leer_tabla("no_existe.csv"))


if __name__ == "__main__":
    main()
