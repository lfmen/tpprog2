# tipos: pasar los valores de texto a int, float, bool, str o None
#
# le llega lo que devuelve leer_filas (lectura), donde todo es texto,
# y tiene que devolver cada fila como diccionario con los valores ya convertidos.
# el orden que conviene: primero las funciones chicas (es_...), después
# inferir_tipo y convertir, y al final convertir_filas.
# se prueba con: python -m tipos_lucas.pruebas


class ConversionError(Exception):
    # cuando el usuario pidió un tipo para una columna y un valor no se puede convertir.
    # tiene que guardar la línea y la columna, y el mensaje decir algo como:
    # "Línea 3, columna 'precio': 'ochocientos' no se puede convertir a float"
    def __init__(self, linea, columna, valor, tipo):
        pass


def es_nulo(texto):
    # True si la celda está vacía ("")
    pass


def es_booleano(texto):
    # True si es true, false, verdadero o falso, sin importar mayúsculas
    pass


def es_entero(texto):
    # True si es un número sin coma: "10", "-3", "+7", "00123"
    # False para "", "1.5", "diez"
    pass


def es_flotante(texto):
    # True si es un número con decimales: "2.5", "-0.25", "1e3" (los enteros también valen)
    # ojo que float() acepta "nan" e "inf", y esos tienen que dar False
    pass


def inferir_tipo(valores):
    # recibe los valores de una columna (sin los vacíos) y devuelve el tipo que sirve para todos:
    # ["10", "20", "30"] -> int
    # ["10", "20", "30.5"] -> float
    # ["10", "hola"] -> str
    # [] -> str (columna toda vacía)
    pass


def convertir(texto, tipo):
    # pasa un valor al tipo que le digan (int, float, bool o str)
    # convertir("10", float) -> 10.0
    # convertir("", int) -> None
    # si no se puede, raise ValueError
    pass


def convertir_filas(columnas, filas, tipos=None):
    # la principal, la usa leer_tabla. no cambiarle el nombre ni lo que recibe/devuelve.
    #
    # recibe:
    #   columnas = ["nombre", "precio"]
    #   filas = [(2, ["Cuaderno", "2500.5"]), (3, ["Lapicera", "800"])]
    #   tipos = {"precio": float}   (opcional, lo que eligió el usuario; eso manda)
    #
    # devuelve:
    #   [(2, {"nombre": "Cuaderno", "precio": 2500.5}),
    #    (3, {"nombre": "Lapicera", "precio": 800.0})]
    #
    # para las columnas que no están en tipos, el tipo se adivina con inferir_tipo
    # mirando todas las filas. si un valor no se puede convertir -> ConversionError
    pass
