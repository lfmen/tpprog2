"""Tipos: convierte los textos que da lectura.py a int, float, bool, str o None.

Las funciones van de la más chica a la principal, convertir_filas, que usa a todas las de arriba:

    filas = convertir_filas(["nombre", "precio"], [(2, ["Cuaderno", "2500.5"])])
"""

TIPOS = [bool, int, float, str]


class ConversionError(Exception):
    """Un valor no se puede convertir al tipo de su columna."""

    def __init__(self, linea, columna, valor, tipo):
        self.linea = linea
        self.columna = columna
        self.valor = valor
        self.tipo = tipo
        super().__init__(f"Línea {linea}, columna '{columna}': '{valor}' no se puede convertir a {tipo.__name__}")


def es_nulo(texto):
    """Revisa si la celda está vacía (o tiene solo espacios), que es como se representa un nulo.

    Parameters
    ----------
    texto : str
        El contenido de una celda.

    Returns
    -------
    bool
        True si la celda está vacía.
    """
    return texto.strip() == ""


def es_booleano(texto):
    """Revisa si el texto es un booleano: true, false, verdadero o falso.

    No se tienen en cuenta las mayúsculas ni los espacios de los costados.

    Parameters
    ----------
    texto : str
        El contenido de una celda.

    Returns
    -------
    bool
        True si el texto es un booleano.
    """
    texto_minuscula = texto.strip().lower()
    return (texto_minuscula == "true" or texto_minuscula == "false"
            or texto_minuscula == "verdadero" or texto_minuscula == "falso")


def es_entero(texto):
    """Revisa si el texto es un número entero, sin coma.

    Parameters
    ----------
    texto : str
        El contenido de una celda.

    Returns
    -------
    bool
        True para "10", "-3", "+7" o "00123". False para "", "1.5" o "diez".
    """
    if "_" in texto:  # int() acepta "1_000", que en una tabla no es un número
        return False
    try:
        int(texto)
        return True
    except ValueError:
        return False


def es_flotante(texto):
    """Revisa si el texto es un número con decimales. Los enteros también valen.

    Parameters
    ----------
    texto : str
        El contenido de una celda.

    Returns
    -------
    bool
        True para "2.5", "-0.25", "1e3" o "10". False para "inf", "nan" o "diez".
    """
    if "_" in texto:  # float() acepta "1_000.5", que en una tabla no es un número
        return False
    try:
        numero = float(texto)
    except ValueError:
        return False

    # float() también acepta "inf" y "nan", que en una tabla son texto.
    # nan es el único valor que no es igual a sí mismo, por eso se compara así
    es_infinito = numero == float("inf") or numero == float("-inf")
    es_nan = numero != numero
    return not (es_infinito or es_nan)


def transformar_a_booleano(texto):
    """Convierte un texto que ya pasó por es_booleano en True o False.

    Parameters
    ----------
    texto : str
        Un booleano escrito como texto.

    Returns
    -------
    bool
        True para "true" o "verdadero", False para "false" o "falso".
    """
    texto_limpio = texto.strip().lower()
    return texto_limpio == "true" or texto_limpio == "verdadero"


def separar_columnas(filas, columnas):
    """Agrupa las celdas por columna, para poder mirar cada columna entera.

    Parameters
    ----------
    filas : list of tuple of (int, list of str)
        Las filas que da leer_filas: el número de línea y las celdas.
        [(2, ["Cuaderno", "2500.5"]), (3, ["Lapicera", "800"])]
    columnas : list of str
        Los nombres de las columnas, en el mismo orden que las celdas.

    Returns
    -------
    list of list of str
        Una lista por columna, con sus celdas.
        [["Cuaderno", "Lapicera"], ["2500.5", "800"]]
    """
    cantidad_columnas = len(columnas)

    columnas_separadas = []
    for posicion in range(cantidad_columnas):
        columna = []
        for numero_linea, celdas in filas:
            columna.append(celdas[posicion])
        columnas_separadas.append(columna)
    return columnas_separadas


def sacar_nulos(valores):
    """Quita las celdas vacías de una columna.

    Parameters
    ----------
    valores : list of str
        Las celdas de una columna, por ejemplo ["10", "20", "30", ""].

    Returns
    -------
    list of str
        Las mismas celdas sin las vacías.
    """
    sin_nulos = []
    for valor in valores:
        if not es_nulo(valor):
            sin_nulos.append(valor)
    return sin_nulos


def inferir_tipo(valores):
    """Adivina el tipo de una columna mirando todos sus valores.

    Se elige el primero de bool, int y float que sirva para todos los valores que no son nulos.
    Si ninguno sirve, o si la columna está toda vacía, es str.

    Parameters
    ----------
    valores : list of str
        Las celdas de una columna.

    Returns
    -------
    type
        bool, int, float o str.
        ["10", "20", "30.5"] -> float, ["10", "hola"] -> str, [] -> str
    """
    sin_nulos = sacar_nulos(valores)

    if len(sin_nulos) == 0:
        return str

    todos_bool = True
    todos_int = True
    todos_float = True

    for valor in sin_nulos:
        if not es_booleano(valor):
            todos_bool = False
        if not es_entero(valor):
            todos_int = False
        if not es_flotante(valor):
            todos_float = False

    if todos_bool:
        return bool
    if todos_int:
        return int
    if todos_float:
        return float
    return str


def convertir_celda(texto, tipo, linea, columna):
    """Convierte una celda al tipo indicado.

    Parameters
    ----------
    texto : str
        El contenido de la celda, tal cual vino del archivo.
    tipo : type
        bool, int, float o str: el que eligió el usuario o el que se adivinó para la columna.
    linea : int
        El número de línea de la celda, solo para el mensaje de error.
    columna : str
        El nombre de la columna, solo para el mensaje de error.

    Returns
    -------
    bool or int or float or str or None
        El valor convertido, o None si la celda está vacía.
    """
    if es_nulo(texto):
        return None

    try:
        if tipo is bool:
            if not es_booleano(texto):
                raise ValueError
            return transformar_a_booleano(texto)
        if tipo is int:
            if not es_entero(texto):
                raise ValueError
            return int(texto)
        if tipo is float:
            if not es_flotante(texto):
                raise ValueError
            return float(texto)
        return texto  # lectura ya recortó lo que no vino entre comillas
    except ValueError:
        raise ConversionError(linea, columna, texto, tipo)


def convertir_filas(columnas, filas, tipos=None):
    """Convierte las celdas de cada fila a su tipo. Es la función principal.

    Cada columna usa el tipo que eligió el usuario y, si no eligió ninguno, el que se adivina
    mirando toda la columna.

    Parameters
    ----------
    columnas : list of str
        Los nombres de las columnas, en el mismo orden que las celdas.
    filas : list of tuple of (int, list of str)
        Las filas que da leer_filas: el número de línea y las celdas.
    tipos : dict, optional
        Los tipos que eligió el usuario, como {"precio": float}. Por defecto es None (se
        adivinan todos).

    Returns
    -------
    list of tuple of (int, dict)
        Por cada fila, su número de línea y un diccionario {columna: valor}.
        [(2, {"nombre": "Cuaderno", "precio": 2500.5}), (3, {"nombre": "Lapicera", "precio": 800.0})]
    """
    if tipos is None:
        tipos = {}

    for nombre in tipos:  # si no, un nombre mal escrito o un tipo raro se ignorarían sin avisar
        if nombre not in columnas:
            raise ValueError(f"No existe la columna '{nombre}' para elegirle el tipo")
        if tipos[nombre] not in TIPOS:
            raise ValueError(f"El tipo de la columna '{nombre}' tiene que ser bool, int, float o str")

    columnas_separadas = separar_columnas(filas, columnas)

    tipos_finales = []
    for posicion in range(len(columnas)):
        nombre = columnas[posicion]
        if nombre in tipos:
            tipos_finales.append(tipos[nombre])
        else:
            tipos_finales.append(inferir_tipo(columnas_separadas[posicion]))

    resultado = []
    for numero_linea, celdas in filas:
        fila_convertida = {}
        for posicion in range(len(columnas)):
            nombre = columnas[posicion]
            fila_convertida[nombre] = convertir_celda(celdas[posicion], tipos_finales[posicion],
                                                      numero_linea, nombre)
        resultado.append((numero_linea, fila_convertida))
    return resultado
