"""Selección: se queda con las filas y columnas que pidió el usuario, y tiene leer_tabla.

Recibe la tabla que da tipos.py, ya convertida. Las funciones van de la más chica a la
principal, leer_tabla, que junta las tres partes:

    filas = leer_tabla("productos.csv", columnas=["nombre"], filtro=lambda fila: fila["stock"] < 10)

Decisiones:
    - Las filas se cuentan desde 1: la primera después del encabezado es la fila 1.
    - Los rangos incluyen los dos extremos: el rango (2, 3) da la fila 2 y la 3.
    - El orden es siempre rango, filtro, n_filas y al final columnas.
    - Si se piden 10 filas con un filtro, se sigue leyendo hasta tener 10 que cumplan.
    - El filtro recibe la fila entera, así que se puede filtrar por una columna que no se muestra.
    - Las columnas elegidas salen en el orden en que están en la tabla.
"""

from lector.lectura import leer_filas
from lector.tipos import convertir_filas


class ColumnaInexistenteError(Exception):
    """Se pidió una columna que la tabla no tiene."""

    def __init__(self, columna):
        self.columna = columna
        self.mensaje = f"No existe la columna {columna}"
        super().__init__(self.mensaje)


class FiltroError(Exception):
    """El filtro del usuario falló con una fila."""

    def __init__(self, linea, error):
        self.linea = linea
        self.error = error
        self.mensaje = f"Línea {linea}: falló el filtro {error}"
        super().__init__(self.mensaje)


def aplicar_n_filas(filas, n_filas):
    """Da las primeras n_filas filas.

    Es un generador: entrega las filas de a una y no sigue recorriendo cuando ya dio las que se
    pidieron, así que un filtro anterior se deja de evaluar.

    Parameters
    ----------
    filas : iterable of tuple of (int, dict)
        Las filas, cada una con su número de línea.
    n_filas : int
        Cuántas filas dar.

    Yields
    ------
    tuple of (int, dict)
        Las primeras n_filas filas.
    """
    if n_filas <= 0:
        return
    contador = 1
    for fila in filas:
        yield fila
        contador += 1
        if contador > n_filas:
            break


def aplicar_rango(filas, desde, hasta):
    """Da las filas desde la número desde hasta la número hasta, las dos incluidas.

    Parameters
    ----------
    filas : iterable of tuple of (int, dict)
        Las filas, cada una con su número de línea.
    desde : int
        La primera fila que se da, contando desde 1.
    hasta : int or None
        La última fila que se da. Con None, sigue hasta el final.

    Yields
    ------
    tuple of (int, dict)
        Las filas del rango.
    """
    contador = 1
    for fila in filas:
        if contador < desde:
            contador += 1
            continue

        if hasta is not None and contador > hasta:
            break
        yield fila
        contador += 1


def aplicar_filtro(filas, filtro):
    """Da las filas para las que el filtro devuelve True.

    Parameters
    ----------
    filas : iterable of tuple of (int, dict)
        Las filas, cada una con su número de línea.
    filtro : function
        Recibe una fila como diccionario y devuelve True o False.

    Yields
    ------
    tuple of (int, dict)
        Las filas que cumplen el filtro.
    """
    for numero_linea, fila in filas:
        try:
            cumple = filtro(fila)
        except Exception as error:  # el filtro lo escribe el usuario y puede fallar con cualquier error
            raise FiltroError(numero_linea, error) from error
        if cumple:
            yield numero_linea, fila


def elegir_columnas(filas, columnas):
    """Arma la lista final, con solo las columnas pedidas y sin los números de línea.

    Parameters
    ----------
    filas : iterable of tuple of (int, dict)
        Las filas, cada una con su número de línea.
    columnas : list of str
        Las columnas que se quieren.

    Returns
    -------
    list of dict
        Una fila por diccionario, con las columnas pedidas en el orden de la tabla.
    """
    return [{k: v for k, v in d[1].items() if k in columnas} for d in filas]


def seleccionar(filas, columnas_tabla, n_filas=None, rango=None, columnas=None, filtro=None):
    """Aplica lo que pidió el usuario, en orden: rango, filtro, n_filas y columnas.

    Antes de recorrer las filas revisa lo pedido: una columna que no existe da
    ColumnaInexistenteError, y un n_filas negativo o un rango imposible, como (0, 3) o (5, 2),
    dan ValueError.

    Parameters
    ----------
    filas : list of tuple of (int, dict)
        Las filas que da convertir_filas.
    columnas_tabla : list of str
        Todas las columnas de la tabla.
    n_filas : int, optional
        Cuántas filas dar. Por defecto es None (todas).
    rango : tuple of (int, int or None), optional
        Las filas (desde, hasta), las dos incluidas. hasta puede ser None. Por defecto es None.
    columnas : list of str, optional
        Las columnas que se quieren. Por defecto es None (todas).
    filtro : function, optional
        Recibe una fila y devuelve True para conservarla. Por defecto es None.

    Returns
    -------
    list of dict
        Las filas elegidas, con las columnas elegidas.
        seleccionar(filas, ["nombre", "precio"], columnas=["nombre"],
                    filtro=lambda fila: fila["precio"] > 1000)
        -> [{"nombre": "Cuaderno"}, {"nombre": "Carpeta"}]
    """
    if columnas is None:
        columnas = columnas_tabla
    else:
        for columna in columnas:
            if columna not in columnas_tabla:
                raise ColumnaInexistenteError(columna)

    if n_filas is not None and n_filas < 0:
        raise ValueError("n_filas no puede ser negativo")

    skip = False
    if n_filas is None:
        skip = True

    if rango is None:
        rango = (1, None)

    if rango[0] < 1 or (rango[1] is not None and rango[0] > rango[1]):
        raise ValueError("rango solicitado incompatible")

    if filtro is None:
        filtro = lambda x: x

    filas = aplicar_rango(filas, rango[0], rango[1])
    filas = aplicar_filtro(filas, filtro)
    if not skip:
        filas = aplicar_n_filas(filas, n_filas)

    filas = elegir_columnas(filas, columnas)

    return filas


def leer_tabla(ruta, separador=",", encabezado=True, tipos=None,
               n_filas=None, rango=None, columnas=None, filtro=None):
    """Lee una tabla de un archivo de texto y la devuelve como lista de diccionarios.

    Es la función principal: lee con leer_filas, convierte con convertir_filas y elige lo pedido
    con seleccionar.

    Parameters
    ----------
    ruta : str
        Ruta del archivo.
    separador : str or None, optional
        Lo que separa los campos. Por defecto es ",". Con None, cualquier cantidad de espacios.
    encabezado : bool, optional
        Si la primera fila tiene los nombres de las columnas. Por defecto es True.
    tipos : dict, optional
        Los tipos que elige el usuario, como {"precio": float}. El resto se adivina.
    n_filas, rango, columnas, filtro : optional
        Lo que se quiere de la tabla (ver seleccionar).

    Returns
    -------
    list of dict
        Una fila por diccionario.
        leer_tabla("productos.csv", columnas=["nombre", "precio"], filtro=lambda fila: fila["stock"] < 10)
        -> [{"nombre": "Teclado mecánico", "precio": 62000.0}]
    """
    columnas_tabla, filas = leer_filas(ruta, separador, encabezado)
    filas = convertir_filas(columnas_tabla, filas, tipos)
    return seleccionar(filas, columnas_tabla, n_filas, rango, columnas, filtro)
