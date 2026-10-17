# selección: elegir filas y columnas, y leer_tabla, que junta todo
#
# leer_tabla es la función que usa cualquiera que use el lector.
# adentro llama a leer_filas (lectura), después a convertir_filas (tipos)
# y al final a seleccionar.
# el orden que conviene: primero las funciones aplicar_..., después
# elegir_columnas, seleccionar y al final leer_tabla.
# se prueba con: python -m seleccion_nino.pruebas
#
# mientras lectura y tipos no estén, se puede probar seleccionar pasándole
# filas armadas a mano, por ejemplo:
#   filas = [(2, {"nombre": "Cuaderno", "cantidad": 10}), (3, {"nombre": "Carpeta", "cantidad": 8})]

from lectura_mengarelli.lectura import leer_filas
from tipos_lucas.tipos import convertir_filas


class ColumnaInexistenteError(Exception):
    # cuando piden una columna que no está en la tabla.
    # mensaje tipo: "No existe la columna 'stock'"
    def __init__(self, columna):
        pass


class FiltroError(Exception):
    # cuando el filtro tira error con alguna fila (por ejemplo comparar None con un número).
    # tiene que guardar la línea y el mensaje decir algo como:
    # "Línea 9: falló el filtro (...)"
    def __init__(self, linea, error):
        pass


def aplicar_rango(filas, desde, hasta):
    # deja pasar solo las filas entre desde y hasta (contando desde 1, los dos incluidos).
    # hasta puede ser None, que es "hasta el final".
    # va con yield (generador)
    pass


def aplicar_filtro(filas, filtro):
    # deja pasar solo las filas para las que filtro(fila) da True.
    # si el filtro tira cualquier error -> FiltroError con el número de línea
    # va con yield
    pass


def aplicar_n_filas(filas, n_filas):
    # deja pasar como mucho n_filas filas y corta
    # va con yield
    pass


def elegir_columnas(filas, columnas):
    # arma la lista final de diccionarios, solo con las columnas pedidas y en ese orden
    # (acá ya se saca el número de línea)
    pass


def seleccionar(filas, columnas_tabla, n_filas=None, rango=None, columnas=None, filtro=None):
    # primero revisa lo que pidió el usuario:
    #   - columna que no existe -> ColumnaInexistenteError
    #   - n_filas negativo o un rango imposible -> ValueError
    # después aplica en orden: rango, filtro, n_filas y columnas
    # si columnas es None, van todas
    pass


def leer_tabla(ruta, separador=",", encabezado=True, tipos=None,
               n_filas=None, rango=None, columnas=None, filtro=None):
    # la principal. no cambiarle el nombre ni los parámetros.
    #
    # leer_tabla("productos.csv", columnas=["nombre", "precio"],
    #            filtro=lambda fila: fila["cantidad"] < 10)
    # -> [{"nombre": "Carpeta", "precio": 3200.0}]
    pass
