"""Lectura: abre el archivo y separa cada línea en campos.

Todos los campos quedan como texto: convertirlos es tarea de tipos.py. Las funciones van de la
más chica a la principal, leer_filas, que usa a todas las de arriba:

    columnas, filas = leer_filas("challenges.csv")
"""

import warnings


class ArchivoVacioError(Exception):
    """El archivo no tiene ninguna fila con datos."""

    def __init__(self, ruta):
        super().__init__(f"El archivo {ruta} está vacío")


class CantidadCamposError(Exception):
    """Una fila tiene distinta cantidad de campos que la primera (el encabezado, si hay)."""

    def __init__(self, linea, esperados, encontrados):
        self.linea = linea
        super().__init__(f"Línea {linea}: tiene {encontrados} campos y la primera fila tiene {esperados}")


class ComillasError(Exception):
    """Una comilla abre y no cierra hasta el final del archivo."""

    def __init__(self, linea):
        self.linea = linea
        super().__init__(f"Línea {linea}: hay una comilla que abre y no cierra")


class EncabezadoWarning(UserWarning):
    """Se le cambió el nombre a una columna del encabezado."""


def leer_comillas(linea, i):
    """Lee un campo entre comillas, desde la posición i hasta la comilla que cierra.

    Dos comillas seguidas dentro del campo valen como una comilla.

    Parameters
    ----------
    linea : str
        La línea entera.
    i : int
        Posición donde empieza el campo, justo después de la comilla que abre.

    Returns
    -------
    tuple of (str, int) or None
        Lo leído y la posición después de la comilla que cierra, o None si no cierra.
        leer_comillas('"a ""b"", c",d', 1) -> ('a "b", c', 12)
    """
    leido = ""
    while i < len(linea):
        if linea[i:i + 2] == '""':
            leido += '"'
            i += 2
        elif linea[i] == '"':
            return leido, i + 1
        else:
            leido += linea[i]
            i += 1
    return None


def separar(linea, separador):
    """Parte una línea en campos sin cortar lo que está entre comillas.

    A cada campo se le sacan los espacios de los costados, venga o no entre comillas.

    Parameters
    ----------
    linea : str
        La línea a partir.
    separador : str or None
        Lo que separa los campos. Con None corta en cualquier cantidad de espacios.

    Returns
    -------
    list of str or None
        Los campos, o None si una comilla queda abierta (la fila sigue en la línea de abajo).
        separar(' a ,"b, c"', ",") -> ["a", "b, c"]
    """
    campos = []
    actual = ""
    con_comillas = False  # si el campo actual vino entre comillas
    i = 0
    while i <= len(linea):  # la vuelta de más, con caracter "", cierra el último campo
        caracter = linea[i:i + 1]
        if separador:
            es_corte = caracter == "" or linea[i:i + len(separador)] == separador
        else:
            es_corte = caracter.strip() == ""  # un espacio, un tab o el fin de la línea

        if es_corte:
            if separador or actual or con_comillas:  # sin separador, muchos espacios cuentan como uno
                campos.append(actual.strip())
            actual = ""
            con_comillas = False
            i += len(separador) if separador else 1
        elif caracter == '"' and not con_comillas and not actual.strip():
            leido = leer_comillas(linea, i + 1)
            if leido is None:
                return None
            actual, i = leido
            con_comillas = True
        else:
            actual += caracter
            i += 1
    return campos


def arreglar_encabezado(nombres):
    """Nombra las columnas vacías y numera las repetidas, con un aviso por cada cambio.

    Parameters
    ----------
    nombres : list of str
        Los nombres tal cual vienen en la primera fila.

    Returns
    -------
    list of str
        Los nombres arreglados.
        ["area", "", "herramienta", "herramienta"] -> ["area", "columna_2", "herramienta", "herramienta_2"]
    """
    resultado = []
    usados = set()  # sets y no listas porque buscar en un set es más rápido
    originales = set(nombres)
    for i, nombre in enumerate(nombres):
        if nombre == "":
            nombre = f"columna_{i + 1}"
            warnings.warn(f"La columna {i + 1} no tiene nombre, se va a llamar {nombre}", EncabezadoWarning)
        if nombre in usados:
            numero = 2
            while f"{nombre}_{numero}" in usados or f"{nombre}_{numero}" in originales:
                numero += 1
            nuevo = f"{nombre}_{numero}"
            warnings.warn(f"La columna {nombre} está repetida, se va a llamar {nuevo}", EncabezadoWarning)
            nombre = nuevo
        resultado.append(nombre)
        usados.add(nombre)
    return resultado


def separar_filas(texto, separador):
    """Da las filas del texto de a una, salteando las líneas vacías.

    Si un campo entre comillas tiene un salto de línea adentro, junta las líneas y la fila queda
    con el número de la línea donde empieza.

    Parameters
    ----------
    texto : str
        Todo el contenido del archivo.
    separador : str or None
        Lo que separa los campos (ver separar).

    Yields
    ------
    tuple of (int, list of str)
        El número de línea y los campos de la fila.
    """
    pendiente = ""  # fila con una comilla abierta, que sigue en la línea de abajo
    for i, linea in enumerate(texto.split("\n")):
        if pendiente:
            linea = pendiente + "\n" + linea
        elif not linea.strip() and not (separador and separador in linea):  # "\t\t" sí es una fila
            continue
        else:
            numero = i + 1  # enumerate cuenta desde 0 y las líneas del archivo desde 1
        valores = separar(linea, separador)
        if valores is None:
            pendiente = linea
        else:
            pendiente = ""
            yield numero, valores
    if pendiente:
        raise ComillasError(numero)


def leer_texto(ruta):
    """Devuelve el contenido del archivo.

    Excel guarda en utf-8 con BOM (utf-8-sig lo saca) o en cp1252, así que si no es utf-8 se
    prueba con cp1252.
    """
    try:
        with open(ruta, encoding="utf-8-sig") as archivo:
            return archivo.read()
    except UnicodeDecodeError:
        with open(ruta, encoding="cp1252") as archivo:
            return archivo.read()


def leer_filas(ruta, separador=",", encabezado=True):
    """Lee el archivo y devuelve las columnas y las filas, todo como texto.

    Parameters
    ----------
    ruta : str
        Ruta del archivo.
    separador : str or None, optional
        Lo que separa los campos. Por defecto es ",". Con None, cualquier cantidad de espacios.
    encabezado : bool, optional
        Si la primera fila tiene los nombres de las columnas. Por defecto es True. Sin
        encabezado, las columnas se llaman columna_1, columna_2...

    Returns
    -------
    tuple of (list of str, list of tuple of (int, list of str))
        Los nombres de las columnas y las filas, cada una con su número de línea para ubicar errores.
        (["nombre", "precio"], [(2, ["Cuaderno", "2500.5"]), (3, ["Lapicera", "800.0"])])
    """
    if separador == "":
        raise ValueError("El separador no puede estar vacío")
    filas = list(separar_filas(leer_texto(ruta), separador))
    if not filas:
        raise ArchivoVacioError(ruta)

    if encabezado:
        columnas = arreglar_encabezado(filas[0][1])
        filas = filas[1:]
    else:
        columnas = [f"columna_{j}" for j in range(1, len(filas[0][1]) + 1)]

    for numero, valores in filas:
        if len(valores) != len(columnas):
            raise CantidadCamposError(numero, len(columnas), len(valores))
    return columnas, filas
