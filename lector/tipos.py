"""Tipos: convierte los textos que da lectura.py a int, float, bool, str o None.

Las funciones van de la más chica a la principal, convertir_filas, que usa a todas las de arriba:

    filas = convertir_filas(["nombre", "precio"], [(2, ["Cuaderno", "2500.5"])])
"""


class ConversionError(Exception):
    """ConversionError es un error para aportar contexto.

    Sucede cuando el usuario pidió un tipo para una columna y un valor no se puede convertir.
    """

    def __init__(self, linea, columna, valor, tipo):
        self.linea = linea
        self.columna = columna
        self.valor = valor
        self.tipo = tipo
        mensaje = (
            f"Línea {linea}, columna {columna}: {valor} no puede ser convertido a {tipo.__name__}"
        )
        super().__init__(mensaje)


def es_nulo(texto):
    """Revisa si el argumento dado es una celda vacía, lo cual implica que es un valor nulo (None).

    True si la celda está vacía ("").
    False para cualquier otro caso.

    Parameters
    ----------
    texto : str
        Un dato de una celda.

    Returns
    -------
    bool
        Si el argumento es, o no es nulo.
    """
    texto = texto.replace(" ", "")
    texto = texto.lower()
    return (texto == "")


def es_booleano(texto):
    """Revisa si el argumento dado es un booleano (True o False).

    Criterio seleccionado: la revisión devolverá True si el argumento es true, false, verdadero
    o falso, SIN TENER EN CUENTA MAYÚSCULAS NI ESPACIOS de los costados.

    Parameters
    ----------
    texto : str
        Un dato de una celda.

    Returns
    -------
    bool
        Si el argumento es, o no es booleano.
    """
    texto = texto.strip()
    texto_minuscula = texto.lower()
    return (texto_minuscula == "true" or texto_minuscula == "false" or texto_minuscula == "verdadero" or texto_minuscula == "falso")


def es_entero(texto):
    """Revisa si el argumento dado es un valor entero (int).

    True si es un número sin coma (algunos ejemplos: "10", "-3", "+7", "00123").
    False para cualquier otro caso (algunos ejemplos: "", "1.5", "diez").

    Parameters
    ----------
    texto : str
        Un dato de una celda.

    Returns
    -------
    bool
        Si el argumento es, o no es entero.
    """
    if "_" in texto:  # int() acepta "1_000", que en una tabla no es un número
        return False

    try:
        int(texto)
        return True
    except ValueError:
        return False


def es_flotante(texto):
    """Revisa si el argumento dado es un valor flotante (float).

    True si es un número con decimales (algunos ejemplos: "2.5", "-0.25", "1e3"; los enteros
    también valen).
    False para cualquier caso contrario (float acepta "nan" e "inf", pero acá tiene que dar False).

    Parameters
    ----------
    texto : str
        Un dato de una celda.

    Returns
    -------
    bool
        Si el argumento es, o no es flotante.
    """
    if "_" in texto:  # float() acepta "1_000.5", que en una tabla no es un número
        return False

    try:
        numero = float(texto)
    except ValueError:
        return False

    # Para esta parte, analizamos la posibilidad de que el valor sea "+-inf" o "nan" (valores que
    # acepta float). El único valor que no es igual a sí mismo es nan, por eso lo comparamos
    es_infinito = numero == float("inf") or numero == float("-inf")

    es_nan = numero != numero

    return not (es_infinito or es_nan)


def transformar_a_booleano(texto):
    """Transforma los datos "verdadero" y "true" a True, y "falso" y "false" a False.

    Sin tener en cuenta mayúsculas ni espacios de los costados.

    Parameters
    ----------
    texto : str
        Un dato de una celda que ya pasó por la revisión de es_booleano(), y su resultado fue True
        (ahora se lo transforma según cuál sea).

    Returns
    -------
    bool
        True si el argumento es "verdadero" o "true", False si es "falso" o "false".
    """
    texto_limpio = texto.strip().lower()
    return (texto_limpio == "true" or texto_limpio == "verdadero")


def separar_columnas(filas, columnas):
    """Se encarga de separar las celdas por sus respectivas columnas.

    Parameters
    ----------
    filas : list of tuple of (int, list of str)
        Filas del archivo. Es una lista de tuplas, donde el primer elemento de las mismas es el
        número de línea (int), y el segundo elemento es otra lista, que contiene las celdas de esa
        fila (strings). Ejemplo:
            filas = [(2, ["Cuaderno", "2500.5"]), (3, ["Lapicera", "800"])]
    columnas : list of str
        Nombres de las columnas, tomados del encabezado del archivo. Su orden coincide con el de
        las celdas de cada fila. Ejemplo:
            columnas = ["nombre", "precio"]

    Returns
    -------
    list of list of str
        Una lista de listas, donde cada lista contiene las celdas agrupadas por sus columnas.
        Ejemplo:
            columnas_separadas = [["Cuaderno", "Lapicera"], ["2500.5", "800"]]
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
    """Quita los valores vacíos de una columna.

    Parameters
    ----------
    valores : list of str
        Es una lista que contiene las celdas de una columna (incluyendo sus vacíos). Ejemplo:
            valores = ["10", "20", "30", ""]

    Returns
    -------
    list of str
        Lista que contiene a las celdas de una columna sin sus vacíos.
    """
    sin_nulos = []
    for valor in valores:
        if not es_nulo(valor):
            sin_nulos.append(valor)
    return sin_nulos


def inferir_tipo(valores):
    """Intenta adivinar/inferir el tipo de los valores que le pasaron.

    Parameters
    ----------
    valores : list of str
        Es una lista que contiene las celdas de una columna. Ejemplo:
            valores = ["10", "20", "30"]

    Returns
    -------
    type
        El tipo que sirve para todos los valores no nulos: bool, int, float o str. Se elige el
        primero que cumplen todos, en ese orden. Devuelve str si ningún otro tipo sirve para todos,
        o si no quedan valores después de sacar los nulos. Ejemplos:
            ["10", "20", "30.5"] -> float
            ["10", "hola"] -> str
            [] -> str (columna toda vacía)
    """
    sin_nulos = (sacar_nulos(valores))

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
    """Convierte el texto de una celda al tipo indicado.

    Si la celda está vacía devuelve None. Para bool, int y float valida antes de convertir, así
    "1_000" da error aunque int() lo acepte. Cualquier otro tipo se trata como texto.

    Parameters
    ----------
    texto : str
        Contenido de una sola celda, tal cual vino del archivo.
    tipo : type
        Tipo al que hay que convertir la celda: bool, int, float o str. Lo recibe de
        convertir_filas, desde el tipo elegido por el usuario o el inferido para esa columna.
    linea : int
        Número de línea de la celda en el archivo. No interviene en la conversión, solo se usa
        para armar el mensaje de ConversionError.
    columna : str
        Nombre de la columna a la que pertenece la celda. Igual que linea, solo se usa para el
        mensaje de error.

    Returns
    -------
    bool or int or float or str or None
        El valor convertido al tipo pedido, o None si la celda está vacía.
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
        return texto.strip()
    except ValueError:
        raise ConversionError(linea, columna, texto, tipo)


def convertir_filas(columnas, filas, tipos=None):
    """Convierte las celdas de cada fila a su tipo correspondiente. Es la función principal.

    Para cada columna usa el tipo elegido por el usuario; si no eligió ninguno, lo infiere
    mirando los valores de toda la columna. Si el usuario nombra una columna que no existe o un
    tipo que no es bool, int, float ni str, da ValueError.

    Parameters
    ----------
    columnas : list of str
        Nombres de las columnas, tomados del encabezado del archivo. Su orden coincide con el de
        las celdas de cada fila.
    filas : list of tuple of (int, list of str)
        Filas del archivo. Es una lista de tuplas, donde el primer elemento de las mismas es el
        número de línea (int), y el segundo elemento es otra lista, que contiene las celdas de esa
        fila (strings).
    tipos : dict, optional
        Tipos elegidos por el usuario, con el formato {nombre_de_columna: tipo}. Por defecto es
        None (se infiere todo si el usuario no provee tipo). Ejemplo:
            tipos = {"precio": float}

    Returns
    -------
    list of tuple of (int, dict)
        Una tupla por cada fila de entrada que contiene el número de línea y un diccionario que
        contiene como key el nombre de la columna, y como valor la celda que pertenece a esa
        columna y a esa línea correspondiente. Ejemplo:
            resultado = [
                (2, {"nombre": "Cuaderno", "precio": 2500.5}),
                (3, {"nombre": "Lapicera", "precio": 800.0}),
            ]
    """
    if tipos is None:
        tipos = {}

    for nombre in tipos:  # si no, un nombre mal escrito o un tipo raro se ignorarían sin avisar
        if nombre not in columnas:
            raise ValueError(f"No existe la columna {nombre} para elegirle el tipo")
        if tipos[nombre] not in [bool, int, float, str]:
            raise ValueError(f"El tipo de la columna {nombre} tiene que ser bool, int, float o str")

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
            fila_convertida[nombre] = convertir_celda(celdas[posicion], tipos_finales[posicion], numero_linea, nombre)
        resultado.append((numero_linea, fila_convertida))

    return resultado
