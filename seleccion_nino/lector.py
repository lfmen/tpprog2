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

    # se lanza cuando el usuario pide una columna que no está en la tabla.
    #
    # recibe: columna, el nombre que pidió (por ejemplo "stock")
    # tiene que:
    #   - guardarlo en self.columna
    #   - armar el mensaje "No existe la columna 'stock'" y pasárselo a super().__init__(mensaje)
    #
    # es igual a las excepciones de lectura/lectura.py, se puede copiar el patrón de ahí.
    # repasar: U2, excepciones -> "Excepciones a medida" y "Agregar información a la excepción"

    def __init__(self, columna):
        self.columna = columna
        self.mensaje = f"No existe la columna {columna}"
        super().__init__(self.mensaje)


class FiltroError(Exception):
    
    # se lanza cuando la función de filtro tira un error con alguna fila
    # (por ejemplo pide fila["stock"] y no existe, o compara None < 10).
    #
    # recibe:
    #   linea: el número de línea de la fila donde falló (por ejemplo 9)
    #   error: el error original que tiró el filtro
    # tiene que:
    #   - guardar la línea en self.linea
    #   - armar el mensaje "Línea 9: falló el filtro (...)", con el error adentro del paréntesis,
    #     y pasárselo a super().__init__(mensaje)

    def __init__(self, linea, error):
        self.linea = linea
        self.error = error
        self.mensaje = f"Línea {linea}: falló el filtro {error}"
        super().__init__(self.mensaje)


def aplicar_n_filas(filas, n_filas):
    # LA MÁS FÁCIL, empezar por esta.
    #
    # recibe:
    #   filas: las filas (lista de tuplas como la de arriba)
    #   n_filas: un entero, cuántas filas quiere el usuario
    # hace: deja pasar las filas de a una hasta llegar a n_filas, y ahí corta
    # devuelve (con yield, de a una): esas filas, sin tocarlas
    #
    # ejemplos:
    #   list(aplicar_n_filas(filas, 2))   -> Cuaderno y Lapicera
    #   list(aplicar_n_filas(filas, 0))   -> []
    #   list(aplicar_n_filas(filas, 10))  -> las 3 (no hay más)
    #
    # ojo: con 0 no tiene que dar ninguna. y hay que cortar apenas llega al número (break),
    # no seguir recorriendo el resto.
    # pista: un for, un contador y break.
    # repasar: U3, generadores -> "Funciones generadoras". U1, ejecución repetitiva -> "La sentencia break"
    counter = 1
    for fila in filas:
        yield fila
        counter += 1
        if counter > n_filas:
            break


def aplicar_rango(filas, desde, hasta):
    # recibe:
    #   filas: las filas
    #   desde: número de la primera fila que se quiere
    #   hasta: número de la última fila que se quiere, o None (que quiere decir "hasta el final")
    # hace: deja pasar solo las filas cuya posición está entre desde y hasta.
    #       se cuenta desde 1 y los dos extremos se incluyen.
    # devuelve (con yield, de a una): esas filas, sin tocarlas
    #
    # ejemplos:
    #   list(aplicar_rango(filas, 2, 3))     -> Lapicera y Carpeta
    #   list(aplicar_rango(filas, 2, None))  -> Lapicera y Carpeta (de la 2 hasta el final)
    #   list(aplicar_rango(filas, 1, 1))     -> solo Cuaderno
    #
    # ojo: la posición NO es el número de línea. Cuaderno está en la línea 2 pero es la fila 1.
    # la posición sale de ir contando mientras se recorren.
    # pista: enumerate (empieza en 0, hay que sumarle 1). cuando se pasa de hasta, break.
    # repasar: U1, colecciones de datos -> "Secuencias" (enumerate)
    pass


def aplicar_filtro(filas, filtro):
    # recibe:
    #   filas: las filas
    #   filtro: una función que recibe UNA fila (el diccionario, sin el número de línea)
    #           y devuelve True o False. ejemplo: lambda fila: fila["cantidad"] < 10
    # hace: deja pasar solo las filas para las que filtro(fila) da True
    # devuelve (con yield, de a una): esas filas, con su número de línea como venían
    #
    # ejemplo:
    #   list(aplicar_filtro(filas, lambda fila: fila["cantidad"] < 10))
    #   -> [(4, {"nombre": "Carpeta", "precio": 3200.0, "cantidad": 8})]
    #
    # ojo: el filtro lo escribe el usuario y puede fallar con cualquier error.
    # no hay que dejar que salga ese error suelto: se atrapa con try / except Exception
    # y se lanza FiltroError(numero_linea, error) con raise ... from error.
    # repasar: U3, fundamentos -> "Funciones anónimas" (lambda) y "Ciudadanos de primera clase".
    #          U2, excepciones -> "Manejo de excepciones" y "Propagación avanzada" (raise ... from ...)
    pass


def elegir_columnas(filas, columnas):
    # recibe:
    #   filas: las filas
    #   columnas: lista con los nombres de las columnas que se quieren, en el orden en que se quieren.
    #             ejemplo: ["nombre", "precio"]
    # hace: de cada fila se queda solo con esas columnas y le saca el número de línea
    # devuelve (una lista normal, NO yield): la lista final de diccionarios, lo que ve el usuario
    #
    # ejemplo:
    #   elegir_columnas(filas, ["nombre", "precio"])
    #   -> [{"nombre": "Cuaderno", "precio": 2500.5},
    #       {"nombre": "Lapicera", "precio": 800.0},
    #       {"nombre": "Carpeta", "precio": 3200.0}]
    #
    # pista: sale en una línea, con una lista por comprensión que adentro tiene
    # un diccionario por comprensión.
    # repasar: U3, funciones de orden superior -> "Comprehensions"
    pass


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
