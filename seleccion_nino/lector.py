# selección: elegir filas y columnas, y leer_tabla, que junta todo
#
# la idea: lectura lee el archivo y tipos convierte los valores. esta parte agarra esa tabla
# ya convertida y se queda solo con lo que pidió el usuario: algunas filas, algunas columnas
# o las filas que cumplen una condición.
#
# en cada función de abajo dice qué recibe, qué tiene que devolver y un ejemplo.
# conviene hacerlas en el orden en que aparecen: de la más fácil a la que junta todo.
#
# decisiones (ya están tomadas, hay que respetarlas):
#   - las filas se cuentan desde 1: la primera después del encabezado es la fila 1
#   - los rangos incluyen los dos extremos: el rango (2, 3) da la fila 2 y la 3
#   - el orden es siempre: rango, filtro, n_filas y al final columnas
#   - si se piden 10 filas con un filtro, se sigue leyendo hasta tener 10 que cumplan
#   - el filtro recibe la fila entera, así que se puede filtrar por una columna que no se muestra
#
# las tres aplicar_... son generadores: no devuelven una lista, van entregando las filas
# de a una con yield. para ver lo que dan en una prueba hay que pasarlas a lista:
#   list(aplicar_n_filas(filas, 2))
#
# todas las funciones reciben las filas así (es la tabla de datos/productos.csv).
# mientras convertir_filas (tipos) no esté terminada, se prueba con esta lista armada a mano:
#
#   filas = [
#       (2, {"nombre": "Cuaderno", "precio": 2500.5, "cantidad": 10}),
#       (3, {"nombre": "Lapicera", "precio": 800.0, "cantidad": 25}),
#       (4, {"nombre": "Carpeta", "precio": 3200.0, "cantidad": 8}),
#   ]
#
# cada fila es una tupla: (número de línea del archivo, fila como diccionario).
# el número de línea solo sirve para avisar dónde falló algo, al final se saca.
# para recorrerlas: for numero_linea, fila in filas:
#
# pruebas: en seleccion_nino/pruebas.py, una función por caso con assert, igual que
# lectura/pruebas.py. se corre parado en la carpeta del tp: python -m seleccion_nino.pruebas
# casos que conviene probar:
#   - cada aplicar_... sola, con la lista de arriba
#   - n_filas=0, un rango de una sola fila y un rango con hasta=None
#   - un filtro que no deja pasar ninguna fila (tiene que dar [])
#   - rango, filtro y n_filas a la vez
#   - filtrar por una columna que no se muestra
#   - cada error: columna que no existe, n_filas negativo, rango imposible y filtro que falla
# para probar que algo tira error:
#   try:
#       seleccionar(filas, ["nombre", "precio", "cantidad"], columnas=["stock"])
#       assert False  # si llega acá, no tiró el error
#   except ColumnaInexistenteError:
#       pass
#
# para el readme: un párrafo corto con las decisiones de arriba.

from lectura.lectura import leer_filas
from tipos_lucas.tipos import convertir_filas


class ColumnaInexistenteError(Exception):

    def __init__(self, columna):
        self.columna = columna
        self.mensaje = f"No existe la columna {columna}"
        super().__init__(self.mensaje)


class FiltroError(Exception):
    
    def __init__(self, linea, error):
        self.linea = linea
        self.error = error
        self.mensaje = f"Línea {linea}: falló el filtro {error}"
        super().__init__(self.mensaje)


def aplicar_n_filas(filas, n_filas):

    if n_filas <= 0:
        return []
    contador = 1
    for fila in filas:
        yield fila
        contador += 1
        if contador > n_filas:
            break


def aplicar_rango(filas, desde, hasta):
    
    contador = 1
    for fila in filas:
        if contador < desde:
            contador +=1
            continue
            
        if hasta is not None and contador > hasta:
            break
        yield fila
        contador += 1


def aplicar_filtro(filas, filtro):

    for numero_linea, fila in filas:
        try:
            cumple = filtro(fila)
        except Exception as error:  # el filtro lo escribe el usuario y puede fallar con cualquier error
            raise FiltroError(numero_linea, error) from error
        if cumple:
            yield numero_linea, fila


def elegir_columnas(filas, columnas):

    return [{columna: fila[columna] for columna in columnas} for numero_linea, fila in filas]


def seleccionar(filas, columnas_tabla, n_filas=None, rango=None, columnas=None, filtro=None):
    # junta las cuatro anteriores.
    #
    # recibe:
    #   filas: las filas
    #   columnas_tabla: todas las columnas que tiene la tabla, ej ["nombre", "precio", "cantidad"]
    #   n_filas: entero o None
    #   rango: tupla (desde, hasta) o None. hasta puede ser None
    #   columnas: lista de nombres o None (None quiere decir todas)
    #   filtro: función o None
    #   (None en cualquiera quiere decir "el usuario no lo pidió")
    #
    # hace, en este orden:
    #   1. si columnas es None, usa columnas_tabla
    #   2. revisa lo que pidió el usuario, ANTES de recorrer nada:
    #      - alguna columna pedida no está en columnas_tabla -> ColumnaInexistenteError(columna)
    #      - n_filas negativo -> ValueError
    #      - rango que empieza antes de 1, o que termina antes de empezar, como (5, 2) -> ValueError
    #   3. aplica solo lo que se pidió, en este orden: aplicar_rango, aplicar_filtro, aplicar_n_filas.
    #      cada paso recibe lo que devolvió el anterior (filas = aplicar_rango(filas, ...), etc)
    #   4. al final, elegir_columnas
    # devuelve: la lista final de diccionarios
    #
    # ejemplo:
    #   seleccionar(filas, ["nombre", "precio", "cantidad"],
    #               columnas=["nombre"], filtro=lambda fila: fila["precio"] > 1000)
    #   -> [{"nombre": "Cuaderno"}, {"nombre": "Carpeta"}]
    #
    # ojo: como las aplicar_... son generadores, no se recorre nada hasta elegir_columnas.
    # por eso si se piden 2 filas con filtro, el filtro se deja de evaluar cuando ya hay 2.
    # repasar: U3, generadores -> "Iterables e iteradores". U2, excepciones -> "Lanzamiento de excepciones"
    pass


def leer_tabla(ruta, separador=",", encabezado=True, tipos=None,
               n_filas=None, rango=None, columnas=None, filtro=None):
    # la principal, la que usa cualquiera que use el lector. no cambiarle el nombre ni los parámetros.
    #
    # recibe: la ruta del archivo y todas las opciones del usuario
    # hace tres pasos, uno por cada parte del grupo:
    #   1. columnas_tabla, filas = leer_filas(ruta, separador, encabezado)     (lectura)
    #   2. filas = convertir_filas(columnas_tabla, filas, tipos)               (tipos)
    #   3. seleccionar con lo que pidió el usuario                             (esta parte)
    # devuelve: lo que devuelve seleccionar
    #
    # ejemplo:
    #   leer_tabla("seleccion_nino/datos/productos.csv", columnas=["nombre", "precio"],
    #              filtro=lambda fila: fila["cantidad"] < 10)
    #   -> [{"nombre": "Carpeta", "precio": 3200.0}]
    #
    # son tres líneas. solo se puede probar cuando convertir_filas (tipos) esté terminada.
    pass
