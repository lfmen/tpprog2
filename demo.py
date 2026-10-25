"""Demo para la presentación. Se corre desde la carpeta tpprog2 con:

    python demo.py

Muestra cada resultado dos veces: como lista de diccionarios (lo que devuelve
el lector) y como DataFrame de pandas. Mostramos las dos porque pandas cambia
algunas cosas, por ejemplo los None de una columna numérica aparecen como NaN.

Para leer un archivo nuevo en la presentación, agregar una línea en main().
"""

import pandas as pd

from lectura.lectura import CantidadCamposError
from seleccion_nino.lector import leer_tabla

pd.set_option("display.max_columns", None)  # sin esto pandas esconde columnas con "..."
pd.set_option("display.width", 200)


def mostrar(titulo, filas):
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)
    for fila in filas:
        print(fila)
    print()
    print(pd.DataFrame(filas))


def main():
    mostrar("Juegos", leer_tabla("lectura/datos/juegos.csv"))

    mostrar("Los mismos juegos separados con ;",
            leer_tabla("lectura/datos/juegos_punto_y_coma.csv", separador=";"))

    mostrar("Nombre y precio de los que tienen menos de 10 unidades",
            leer_tabla("seleccion_nino/datos/productos.csv", columnas=["nombre", "precio"],
                       filtro=lambda fila: fila["cantidad"] < 10))

    mostrar("Tipos mezclados", leer_tabla("tipos_lucas/datos/tipos_mezclados.csv"))

    mostrar("Códigos como texto (para no perder los ceros)",
            leer_tabla("tipos_lucas/datos/codigos.csv", tipos={"codigo": str}))

    mostrar("Alumnos regulares entre las filas 3 y 10, solo los primeros 3",
            leer_tabla("seleccion_nino/datos/alumnos.csv", rango=(3, 10),
                       filtro=lambda fila: fila["regular"], n_filas=3,
                       columnas=["apellido", "nota"]))

    print("\nArchivo con una fila a la que le falta un campo:")
    try:
        leer_tabla("lectura/datos/falta_un_campo.csv")
    except CantidadCamposError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
