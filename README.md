<img src="https://raw.githubusercontent.com/ee-unr/programacion-2/main/imgs/serpiente.png" width="60" align="right" alt="serpiente de la cátedra">

# Lector de datos tabulares

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white) ![Programación II, UNR 2026](https://img.shields.io/badge/Programaci%C3%B3n_II-UNR_2026-2b2b2b?style=flat-square)

Trabajo práctico grupal de Programación II. Facultad de Ciencias Económicas y Estadística, UNR, 2026.

Módulo de Python que lee tablas almacenadas en archivos de texto plano (CSV y formatos similares)
y las devuelve como una lista de diccionarios.

| Integrante | Parte | Archivo |
|---|---|---|
| Mengarelli, Luca Franco | Lectura | `lector/lectura.py` |
| Capella, Lucas | Tipos | `lector/tipos.py` |
| Morello, Nino Julián | Selección | `lector/seleccion.py` |

## Cómo se usa

En Positron: File, Open Folder, y elegir la carpeta del TP. Para ver los ejemplos, abrir
`ejemplos.py` y ejecutarlo con el botón ▷ (o Ctrl+Shift+Enter). También anda desde la terminal,
estando en cualquier carpeta:

```bash
python ejemplos.py
```

Para leer cualquier archivo, desde la consola o desde un programa guardado en esta carpeta:

```python
from lector.seleccion import leer_tabla

leer_tabla("productos.csv")
# [{'nombre': 'Auriculares inalámbricos', 'categoria': 'Electrónica', 'precio': 45999.99, ...}, ...]

leer_tabla("productos.csv", columnas=["nombre", "precio"], filtro=lambda fila: fila["stock"] < 10)
# [{'nombre': 'Teclado mecánico', 'precio': 62000.0}]
```

Si el archivo está en otra carpeta, se pasa la ruta completa con `/`:
`leer_tabla("C:/Users/usuario/Downloads/datos.csv")`. Todas las opciones son optativas:

| Opción | Qué hace | Ejemplo |
|---|---|---|
| `separador` | Lo que separa los campos. Por defecto `","`. Puede tener varios caracteres. Con `None`, cualquier cantidad de espacios o tabs. | `separador=";"`, `separador="\t"` |
| `encabezado` | Si la primera fila tiene los nombres. Sin encabezado, las columnas son `columna_1`, `columna_2`... | `encabezado=False` |
| `tipos` | El tipo de una o más columnas. Las demás se adivinan. | `tipos={"codigo": str}` |
| `rango` | Las filas `(desde, hasta)`, contadas desde 1 y con los dos extremos incluidos. `hasta` puede ser `None`. | `rango=(2, 5)` |
| `filtro` | Una función que recibe la fila y devuelve `True` para quedársela. | `filtro=lambda fila: fila["precio"] < 10000` |
| `n_filas` | Cuántas filas devolver. | `n_filas=3` |
| `columnas` | Qué columnas devolver. | `columnas=["nombre", "precio"]` |

Para verlo como tabla, en el programa de la demostración y no en el lector:
`pd.DataFrame(leer_tabla("productos.csv"))`. Hay que mostrar también la lista, porque pandas
muestra los `None` como `NaN`.

## Cómo funciona

`leer_tabla` hace tres pasos, uno por parte. Cada parte recibe lo que devuelve la anterior:

```text
archivo ──> leer_filas ──────────> convertir_filas ─────────> seleccionar ──────> lista de diccionarios
            (lectura)              (tipos)                     (selección)
            columnas y filas       filas como diccionarios     rango, filtro,
            como texto             con cada valor convertido   n_filas, columnas
```

Cada fila viaja con su número de línea del archivo hasta el final, para que cualquier error diga
en qué línea está. En cada archivo las funciones van de la más chica a la principal:

| Archivo | Funciones |
|---|---|
| `lectura.py` | `leer_comillas` → `separar` → `arreglar_encabezado` → `separar_filas` → `leer_texto` → **`leer_filas`** |
| `tipos.py` | `es_nulo`, `es_booleano`, `es_entero`, `es_flotante` → `transformar_a_booleano` → `separar_columnas` → `sacar_nulos` → `inferir_tipo` → `convertir_celda` → **`convertir_filas`** |
| `seleccion.py` | `aplicar_n_filas`, `aplicar_rango`, `aplicar_filtro` → `elegir_columnas` → `seleccionar` → **`leer_tabla`** |

`separar` recorre la línea carácter por carácter (no usa `split`) para no cortar lo que está entre
comillas. Las funciones `aplicar_*` y `separar_filas` son generadores.

## Decisiones

Lo que la consigna pide definir. También está en los docstrings de cada archivo.

**Lectura**

- Separador: lo indica el usuario. Acepta cualquier texto, de uno o más caracteres. `None` corta
  en cualquier cantidad de espacios o tabs.
- Comillas: un campo entre comillas puede tener el separador o saltos de línea adentro, y `""`
  vale como una comilla. Las comillas solo cuentan si abren el campo. A cada campo se le sacan
  los espacios de los costados.
- Líneas vacías: se saltean y no cuentan como fila.
- Encabezado: una columna sin nombre se llama `columna_<posición>` y una repetida `nombre_2`,
  `nombre_3`..., con un aviso `EncabezadoWarning` por cada cambio. Sin encabezado, las columnas
  se llaman `columna_1`, `columna_2`...
- Codificación: primero UTF-8 (sacando el BOM que pone Excel) y, si falla, `cp1252`.

**Tipos**

- Se adivina mirando toda la columna. Se prueba en orden `bool`, `int`, `float` y `str`, y se
  elige el primero que sirve para todos los valores no vacíos.
- Booleanos: `true`, `false`, `verdadero` y `falso`, sin importar mayúsculas.
- Nulos: una celda vacía es `None`. Una columna toda vacía es `str` con todos `None`.
- Números y texto en una misma columna: queda `str`. `10`, `20` y `30.5` dan `float`.
- `nan`, `inf` y números con `_` (`1_000`) se toman como texto.
- El tipo que pide el usuario tiene prioridad. Si un valor no se puede convertir, da
  `ConversionError` y no se cambia por otro tipo. Con `str` se conserva tal cual: `"00123"`.

**Selección**

- Las filas se cuentan desde 1: la primera después del encabezado es la fila 1.
- El rango incluye los dos extremos.
- Orden: rango, filtro, n_filas y al final columnas.
- Con `n_filas` y un filtro, se sigue leyendo hasta tener `n_filas` filas que cumplan.
- El filtro recibe la fila entera, así que se puede filtrar por una columna que no se muestra.
- Las columnas salen en el orden de la tabla.

## Errores

El lector se frena y el mensaje dice qué pasó y, si corresponde, la línea y la columna.

| Error | Cuándo |
|---|---|
| `ArchivoVacioError` | El archivo no tiene nada, o solo líneas en blanco |
| `CantidadCamposError` | Una fila tiene distinta cantidad de campos que la primera (casi siempre, separador equivocado) |
| `ComillasError` | Una comilla abre y no cierra hasta el final del archivo |
| `ConversionError` | Un valor no se puede convertir al tipo que pidió el usuario |
| `ColumnaInexistenteError` | Se pidió en `columnas` una columna que no existe |
| `FiltroError` | La función de filtro falló con una fila (por ejemplo, comparar un `None`) |
| `ValueError` | Separador vacío, rango imposible como `(0, 3)` o `(5, 2)`, `n_filas` negativo, o `tipos` con una columna que no existe o un tipo que no es `bool`, `int`, `float` ni `str` |
| `FileNotFoundError` | El archivo no existe (es el error de Python) |

Un archivo que solo tiene el encabezado no es un error: da `[]`.

## Casos raros y limitaciones

- La única limitación: lee el archivo entero de una vez. Con las tablas del TP no se nota.
- `ab"c` queda `ab"c`, y `"abc"def` queda `abcdef`, igual que con el módulo `csv` de Python.
- Con `separador=None`, una celda vacía se escribe `""`, porque varios espacios cuentan como uno.
- Decimales con coma (`3500,50`) quedan como texto.

## Ejemplos

`ejemplos.py` muestra lo que devuelve el lector y abajo lo que se esperaba. Tiene 6 ejemplos de
lectura y tipos, 2 de selección (uno es el de la consigna) y 7 errores. Encuentra los datos al lado
suyo, así que anda desde cualquier carpeta. No hay que correrlo de a líneas en la consola, porque
ahí no existe `__file__`.

| Archivo | Qué prueba |
|---|---|
| `productos.csv` | Comas, encabezado, una línea vacía, comas entre comillas, una celda vacía |
| `empleados.txt` | Separado por espacios, sin encabezado, campos con espacios entre comillas |
| `clientes.csv` | Punto y coma, guardado por Excel (con BOM), una columna repetida y otra sin nombre |

## Organización

El lector es el paquete `lector`, con un módulo por parte. `ejemplos.py` y los archivos de datos
están al lado:

```text
G17_Capella_Mengarelli_Morello/
├── lector/
│   ├── lectura.py      lee el archivo y separa los campos
│   ├── tipos.py        convierte cada valor a su tipo
│   └── seleccion.py    elige filas y columnas, y tiene leer_tabla
├── ejemplos.py         ejemplos de uso, con los tres archivos de abajo
├── productos.csv       separado por comas, con encabezado
├── empleados.txt       separado por espacios, sin encabezado
└── clientes.csv        separado por punto y coma, guardado con Excel
```
