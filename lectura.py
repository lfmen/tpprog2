"""Lectura: abre el archivo y separa cada línea en campos, todo como texto (convertir es tarea de tipos).

    columnas, filas = leer_filas("datos/productos.csv")

Las funciones van de la general a las más chicas: leer_filas usa a las de abajo.
"""

import warnings


class ArchivoVacioError(Exception):
    def __init__(self, ruta):
        super().__init__(f"El archivo {ruta} está vacío")


class CantidadCamposError(Exception):
    def __init__(self, linea, esperados, encontrados):
        self.linea = linea
        super().__init__(f"Línea {linea}: tiene {encontrados} campos y el encabezado tiene {esperados}")


class ComillasError(Exception):
    def __init__(self, linea):
        self.linea = linea
        super().__init__(f"Línea {linea}: hay una comilla que abre y no cierra")


class EncabezadoWarning(UserWarning):
    """Aviso de que se le cambió el nombre a una columna del encabezado."""


def leer_filas(ruta, separador=",", encabezado=True):
    """Devuelve las columnas y las filas, cada fila con su número de línea para ubicar errores.

    (["nombre", "precio"], [(2, ["Cuaderno", "2500.5"]), (3, ["Lapicera", "800.0"])])
    Sin encabezado, las columnas se llaman columna_1, columna_2...
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


def leer_texto(ruta):
    """Devuelve el contenido del archivo. Excel guarda en utf-8 con BOM (el -sig lo saca) o en cp1252."""
    try:
        with open(ruta, encoding="utf-8-sig") as archivo:
            return archivo.read()
    except UnicodeDecodeError:
        with open(ruta, encoding="cp1252") as archivo:
            return archivo.read()


def separar_filas(texto, separador):
    """Da (numero de línea, campos) por cada fila, salteando las líneas vacías.

    Si una fila tiene un campo entre comillas con un salto de línea adentro, junta las líneas
    y la fila queda con el número de la línea donde empieza.
    """
    pendiente = ""  # fila con una comilla abierta, que sigue en la línea de abajo
    for i, linea in enumerate(texto.split("\n"), 1):
        if pendiente:
            linea = pendiente + "\n" + linea
        elif not linea.strip():
            continue
        else:
            numero = i
        valores = separar(linea, separador)
        if valores is None:
            pendiente = linea
        else:
            pendiente = ""
            yield numero, valores
    if pendiente:
        raise ComillasError(numero)


def arreglar_encabezado(nombres):
    """Nombra las columnas vacías y numera las repetidas, con un aviso por cada cambio.

    ["area", "", "herramienta", "herramienta"] -> ["area", "columna_2", "herramienta", "herramienta_2"]
    """
    resultado, usados, originales = [], set(), set(nombres)  # sets: buscar en ellos es directo
    for i, nombre in enumerate(nombres, 1):
        if nombre == "":
            nombre = f"columna_{i}"
            warnings.warn(f"La columna {i} no tiene nombre, se va a llamar {nombre}", EncabezadoWarning)
        if nombre in usados:
            numero = 2
            while f"{nombre}_{numero}" in usados or f"{nombre}_{numero}" in originales:
                numero += 1
            warnings.warn(f"La columna {nombre} está repetida, se va a llamar {nombre}_{numero}", EncabezadoWarning)
            nombre = f"{nombre}_{numero}"
        resultado.append(nombre)
        usados.add(nombre)
    return resultado


def separar(linea, separador):
    """Parte una línea en campos sin cortar lo que está entre comillas.

    Con separador None corta en cualquier cantidad de espacios. Si una comilla queda abierta
    devuelve None, porque la fila sigue en la línea de abajo.
    """
    campos, actual, con_comillas = [], "", False  # con_comillas: el campo vino entre comillas y no se recorta
    i = 0
    while i <= len(linea):  # la vuelta de más, con caracter "", cierra el último campo
        caracter = linea[i:i + 1]
        if caracter == "" or (linea.startswith(separador, i) if separador else caracter.isspace()):
            if separador or actual or con_comillas:  # sin separador, muchos espacios cuentan como uno
                campos.append(actual if con_comillas else actual.strip())
            actual, con_comillas = "", False
            i += len(separador or " ")
        elif caracter == '"' and not con_comillas and not actual.strip():
            leido = leer_comillas(linea, i + 1)
            if leido is None:
                return None
            actual, i = leido
            con_comillas = True
        else:
            if not (con_comillas and caracter.isspace()):  # los espacios después de cerrar se ignoran
                actual += caracter
            i += 1
    return campos


def leer_comillas(linea, i):
    """Lee desde la posición i hasta la comilla que cierra. Dos comillas seguidas son una comilla.

    Devuelve (lo leído, posición después de la comilla que cierra), o None si no cierra.
    leer_comillas('"a ""b"", c",d', 1) -> ('a "b", c', 12)
    """
    leido = ""
    while i < len(linea):
        if linea.startswith('""', i):
            leido += '"'
            i += 2
        elif linea[i] == '"':
            return leido, i + 1
        else:
            leido += linea[i]
            i += 1
    return None
