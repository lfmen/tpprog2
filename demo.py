"""Demo del lector. Se corre desde la carpeta del proyecto con:

    python demo.py

Usa un archivo de datos de cada parte. Cada resultado se muestra como lista de diccionarios,
que es lo que devuelve el lector, y como DataFrame de pandas si está instalado. pandas no es
parte del lector: se usa solo para ver la tabla, y cambia algunas cosas (un None aparece como NaN).
"""

from seleccion_nino.lector import leer_tabla

try:
    import pandas as pd
    pd.set_option("display.max_columns", None)  # sin esto pandas esconde columnas con "..."
    pd.set_option("display.width", 200)
except ImportError:
    pd = None

ALUMNOS = "seleccion_nino/datos/alumnos.csv"
TIPOS = "tipos_lucas/datos/tipos_mezclados.csv"
LENGUAJES = "lectura/datos/lenguajes_espacios.txt"


def mostrar(titulo, filas):
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)
    for fila in filas:
        print(fila)
    if pd is not None:
        print()
        print(pd.DataFrame(filas))


def mostrar_error(titulo, lectura):
    # lectura es una función sin argumentos que llama al lector y tiene que fallar
    print("\n" + titulo)
    try:
        lectura()
    except Exception as error:
        print(f"  {type(error).__name__}: {error}")


def main():
    mostrar("Cada columna con su tipo, adivinado mirando todos sus valores", leer_tabla(TIPOS))

    mostrar("Un tipo elegido por el usuario manda sobre el adivinado",
            leer_tabla(TIPOS, tipos={"entero": str}, columnas=["entero", "decimal"]))

    mostrar("Separado por espacios", leer_tabla(LENGUAJES, separador=None))

    mostrar("Alumnos regulares con 8 o más (filtra por columnas que no se muestran)",
            leer_tabla(ALUMNOS, columnas=["apellido", "carrera"],
                       filtro=lambda fila: fila["regular"] and fila["nota"] >= 8))

    mostrar("Filas 3 a 10, solo las regulares, y de esas las primeras 3",
            leer_tabla(ALUMNOS, rango=(3, 10), filtro=lambda fila: fila["regular"], n_filas=3,
                       columnas=["apellido", "nota"]))

    print("\n" + "=" * 70)
    print("Errores")
    print("=" * 70)
    mostrar_error("Una columna que no existe:", lambda: leer_tabla(ALUMNOS, columnas=["edad"]))
    mostrar_error("Un filtro que falla con la nota vacía:",
                  lambda: leer_tabla(ALUMNOS, filtro=lambda fila: fila["nota"] >= 6))
    mostrar_error("Un tipo que no se puede aplicar:",
                  lambda: leer_tabla(ALUMNOS, tipos={"apellido": int}))


if __name__ == "__main__":
    main()
