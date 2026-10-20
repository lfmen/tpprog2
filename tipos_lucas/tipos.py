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
        self.linea = linea
        self.columna = columna
        self.valor = valor
        self.tipo = tipo
        mensaje = (
            f"Linea {linea}, columna {columna}: {valor} no puede ser convertido a {tipo}"
        )
        super().__init__(mensaje)



def es_nulo(texto):
    # True si la celda está vacía (""), o con varios espacios ("   "), o si es NaN, None, Null, NA, N/A. Y consideramos tambien como celda vacia a ("---", "____")
    texto = texto.replace(" ", "").replace("-", "").replace("_", "")
    texto = texto.lower()
    return (texto == "" or texto == "nan" or texto == "na" or texto == "n/a" or texto == "null" or texto == "none")


def es_booleano(texto):
    # Criterio seleccionado: True si es true, false, verdadero o falso, SIN TENER EN CUENTA MAYUSCULAS NI ESPACIOS
    texto = texto.replace(" ", "")
    texto_minuscula = texto.lower()
    return (texto_minuscula == "true" or texto_minuscula == "false" or texto_minuscula == "verdadero" or texto_minuscula == "falso")
   


def es_entero(texto):
    # True si es un número sin coma: "10", "-3", "+7", "00123"
    # False para "", "1.5", "diez"
    try:
        int(texto)
        return True
    except ValueError:
        return False


def es_flotante(texto):
    # True si es un número con decimales: "2.5", "-0.25", "1e3" (los enteros también valen)
    # float() acepta "nan" e "inf", y esos tienen que dar False. "nan" no va a aparecer porque primero vemos si es nulo (usando 'es_nulo()') en 'convertir_filas()'
    if texto == "inf":
        return False
        try:
            float(texto)
            return True
        except ValueError:
            return False



class FilaIncompletaError(Exception):
    # Se usa solo al separar las columnas en la funcion 'separar_columnas()'
    # El error aparece cuando una fila tiene más, o menos celdas que columnas en su encabezado.
    # Guarda la línea, la cantidad esperada y la encontrada, y transmite el error con su respectivo mensaje.
    def __init__(self, linea, filas_esperadas, filas_encontradas):
        self.linea = linea
        self.filas_esperadas = filas_esperadas
        self.filas_encontradas = filas_encontradas
        mensaje = (
            f" ERROR en Linea {linea}: Se esperaba encontrar {filas_esperadas} filas. Se encontraron {filas_encontradas}"
        )
        super().__init__(mensaje)




def separar_columnas(filas, columnas): # -> Se encarga de separar las columnas. Devuelve una lista que contiene adentro otras listas con los valores de las columnas
                                       # -> Luego, esa lista se usara para inferir los tipos en la funcion 'inferir_tipos()'
    cantidad_columnas = len(columnas)
    
    for numero_linea, celdas in filas:
        if len(celdas) != cantidad_columnas:
            raise FilaIncompletaError(numero_linea, cantidad_columnas, len(celdas))

    columnas_separadas = []
    for j in range(cantidad_columnas):
        columna = []
        for numero_linea, celdas in filas:
            columna.append(celdas[j])
        columnas_separadas.append(columna)


    return columnas_separadas


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
