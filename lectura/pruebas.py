# pruebas de lectura
# correr desde la carpeta tpprog2: python -m lectura.pruebas

import warnings

from lectura.lectura import (ArchivoVacioError, CantidadCamposError, ComillasError,
                                        arreglar_encabezado, leer_filas, separar)

DATOS = "lectura/datos/"


def prueba_separar():
    assert separar("a,b,c", ",") == ["a", "b", "c"]
    assert separar(" a , b ,c ", ",") == ["a", "b", "c"]
    assert separar("a,,c", ",") == ["a", "", "c"]
    assert separar("a||b||c", "||") == ["a", "b", "c"]
    assert separar("a   b  c", None) == ["a", "b", "c"]


def prueba_juegos():
    columnas, filas = leer_filas(DATOS + "juegos.csv")
    assert columnas == ["titulo", "anio", "desarrolladora", "exclusivo_playstation"]
    assert filas[0] == (2, ["The Last of Us", "2013", "Naughty Dog", "true"])
    assert len(filas) == 29


def prueba_otros_separadores():
    # tienen que dar lo mismo que con coma
    esperado = leer_filas(DATOS + "juegos.csv")
    assert leer_filas(DATOS + "juegos_punto_y_coma.csv", ";") == esperado
    assert leer_filas(DATOS + "juegos_tab.tsv", "\t") == esperado
    assert leer_filas(DATOS + "juegos_barras.txt", "||") == esperado


def prueba_espacios():
    columnas, filas = leer_filas(DATOS + "lenguajes_espacios.txt", None)
    assert columnas == ["lenguaje", "anio", "tipado"]
    assert filas[0] == (2, ["Python", "1991", "dinámico"])
    assert len(filas) == 10


def prueba_archivos_largos():
    assert len(leer_filas(DATOS + "peliculas.csv")[1]) == 73
    assert len(leer_filas(DATOS + "titulos_independiente.csv")[1]) == 34


def prueba_sin_encabezado():
    columnas, filas = leer_filas(DATOS + "sin_encabezado.csv", encabezado=False)
    assert columnas == ["columna_1", "columna_2", "columna_3"]
    assert filas[0] == (1, ["Gustavo Cerati", "Argentina", "solista"])
    assert len(filas) == 7


def prueba_encabezado_raro():
    with warnings.catch_warnings(record=True) as avisos:
        warnings.simplefilter("always")
        columnas, filas = leer_filas(DATOS + "encabezado_raro.csv")
    assert columnas == ["area", "columna_2", "herramienta", "herramienta_2"]
    assert len(avisos) == 2


def prueba_arreglar_encabezado():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert arreglar_encabezado(["a", "a", "a"]) == ["a", "a_2", "a_3"]
        assert arreglar_encabezado(["a", "a", "a_2"]) == ["a", "a_3", "a_2"]


def prueba_filas_vacias():
    columnas, filas = leer_filas(DATOS + "filas_vacias.csv")
    # los numeros son las lineas del archivo, contando las vacias
    assert [numero for numero, _ in filas] == [2, 4, 6, 8]


def prueba_comillas():
    assert separar('"x||y"||z', "||") == ["x||y", "z"]
    columnas, filas = leer_filas(DATOS + "comillas.csv")
    assert filas[0][1] == ["Nvidia", "1993", "Santa Clara, California", "GPUs GeForce, CUDA y chips para centros de datos"]
    assert filas[2][1][3] == 'fundada por Guillermo Rauch, antes se llamaba "ZEIT"'


def prueba_comillas_y_espacios():
    assert separar('" a ",b', ",") == [" a ", "b"]  # entre comillas no se recorta
    assert separar('"Santa Clara" 1990', None) == ["Santa Clara", "1990"]
    assert separar('"" x', None) == ["", "x"]


def prueba_varias_lineas():
    columnas, filas = leer_filas(DATOS + "varias_lineas.csv")
    assert filas[0] == (2, ["El secreto de sus ojos", "2009",
                            "Un empleado judicial retirado\nescribe una novela sobre un caso viejo"])
    assert filas[1][0] == 4


def prueba_comillas_sin_cerrar():
    try:
        leer_filas(DATOS + "comillas_sin_cerrar.csv")
        assert False
    except ComillasError as error:
        assert error.linea == 2


def prueba_csv_de_excel():
    columnas, filas = leer_filas(DATOS + "con_bom.csv")
    assert columnas == ["ciudad", "provincia", "departamento"]
    assert filas[0][1][0] == "Cañada de Gómez"


def prueba_excel_windows():
    columnas, filas = leer_filas(DATOS + "excel_windows.csv")  # guardado en cp1252
    assert filas[0][1][0] == "Soda Stéreo"
    assert filas[1][1][1] == "El Palomar, Buenos Aires"


def prueba_archivo_vacio():
    try:
        leer_filas(DATOS + "vacio.csv")
        assert False
    except ArchivoVacioError:
        pass


def prueba_falta_un_campo():
    try:
        leer_filas(DATOS + "falta_un_campo.csv")
        assert False
    except CantidadCamposError as error:
        assert error.linea == 3


PRUEBAS = [
    prueba_separar,
    prueba_juegos,
    prueba_otros_separadores,
    prueba_espacios,
    prueba_archivos_largos,
    prueba_sin_encabezado,
    prueba_encabezado_raro,
    prueba_arreglar_encabezado,
    prueba_filas_vacias,
    prueba_comillas,
    prueba_comillas_y_espacios,
    prueba_varias_lineas,
    prueba_comillas_sin_cerrar,
    prueba_csv_de_excel,
    prueba_excel_windows,
    prueba_archivo_vacio,
    prueba_falta_un_campo,
]

if __name__ == "__main__":
    for prueba in PRUEBAS:
        prueba()
        print("ok", prueba.__name__)
