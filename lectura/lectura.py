"""Lectura: abre el archivo y separa cada línea en campos.

Todo queda como texto. La conversión a números, booleanos y nulos la hace tipos.

Uso:
    from lectura.lectura import leer_filas
    columnas, filas = leer_filas("lectura/datos/juegos.csv")
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


def separar(linea, separador, numero_linea=None):
    """Parte una línea en campos.

    Con separador None separa cualquier cantidad de espacios o tabulaciones.
    Lo que está entre comillas no se corta ni se recorta: separar('"Santa Clara, CA",1971', ",")
    da ["Santa Clara, CA", "1971"]. Si una comilla abre y no cierra, lanza ComillasError.
    """
    # se recorre caracter por caracter porque split no sabe de comillas
    campos = []
    actual = ""
    con_comillas = False  # lo que estaba entre comillas no se recorta
    entre_comillas = False
    i = 0
    while i < len(linea):
        caracter = linea[i]
        if entre_comillas:
            if linea[i:i + 2] == '""':  # comilla escapada
                actual += '"'
                i += 1  # con el i += 1 del final saltea las dos comillas
            elif caracter == '"':
                entre_comillas = False
            else:
                actual += caracter
        elif separador is None and caracter in " \t":
            if actual != "" or con_comillas:
                campos.append(actual)
                actual = ""
                con_comillas = False
        elif separador is not None and linea[i:i + len(separador)] == separador:
            campos.append(actual if con_comillas else actual.strip())
            actual = ""
            con_comillas = False
            i += len(separador) - 1  # con el i += 1 del final saltea todo el separador
        elif caracter == '"' and actual.strip() == "" and not con_comillas:
            entre_comillas = True
            con_comillas = True
            actual = ""
        elif not (con_comillas and caracter in " \t"):  # los espacios despues de cerrar se ignoran
            actual += caracter
        i += 1

    if entre_comillas:
        raise ComillasError(numero_linea)
    if separador is not None:
        campos.append(actual if con_comillas else actual.strip())
    elif actual != "" or con_comillas:
        campos.append(actual)
    return campos


def arreglar_encabezado(nombres):
    """Les pone nombre a las columnas vacías y numera las repetidas, con un aviso por cada cambio.

    ["area", "", "herramienta", "herramienta"] -> ["area", "columna_2", "herramienta", "herramienta_2"]
    """
    # sets porque buscar en un set es directo y en una lista hay que recorrerla
    resultado = []
    usados = set()
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


def leer_filas(ruta, separador=",", encabezado=True):
    """Lee el archivo y devuelve las columnas y las filas, todo como texto.

    Cada fila viene con su número de línea, para que los errores digan dónde está el problema:
    (["nombre", "precio"], [(2, ["Cuaderno", "2500.5"]), (3, ["Lapicera", "800.0"])])

    Con encabezado=False las columnas se llaman columna_1, columna_2...
    """
    if separador == "":
        raise ValueError("El separador no puede estar vacío")
    try:
        with open(ruta, encoding="utf-8-sig") as archivo:  # -sig por el caracter raro que pone excel
            texto = archivo.read()
    except UnicodeDecodeError:  # excel en windows guarda en cp1252
        with open(ruta, encoding="cp1252") as archivo:
            texto = archivo.read()

    # un solo recorrido: separa, arma el encabezado y controla la cantidad de campos
    columnas = None
    filas = []
    pendiente = ""  # una fila con un campo entre comillas que sigue en la linea de abajo
    for i, linea in enumerate(texto.split("\n")):
        if pendiente != "":
            linea = pendiente + "\n" + linea  # numero queda en la linea donde empezo la fila
        elif linea.strip() == "":  # las lineas vacias se saltean
            continue
        else:
            numero = i + 1

        try:
            valores = separar(linea, separador, numero)
        except ComillasError:
            pendiente = linea
            continue
        pendiente = ""

        if columnas is None:
            if encabezado:
                columnas = arreglar_encabezado(valores)
                continue
            columnas = [f"columna_{j + 1}" for j in range(len(valores))]

        if len(valores) != len(columnas):
            raise CantidadCamposError(numero, len(columnas), len(valores))
        filas.append((numero, valores))

    if pendiente != "":
        raise ComillasError(numero)
    if columnas is None:
        raise ArchivoVacioError(ruta)
    return columnas, filas
