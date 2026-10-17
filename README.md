# TP Programación II: lector de tablas

![python](https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white) ![materia](https://img.shields.io/badge/programaci%C3%B3n%20II-UNR%202026-555?style=flat-square) ![estado](https://img.shields.io/badge/estado-en%20desarrollo-orange?style=flat-square)

Morello, Nino Julián · Capella, Lucas · Mengarelli, Luca Franco

Lee tablas guardadas en archivos de texto (CSV y parecidos) y las devuelve como una lista de
diccionarios. La lectura está hecha a mano, sin el módulo `csv` ni los lectores de pandas.

| Carpeta | Parte | Responsable |
|---|---|---|
| `lectura_mengarelli` | Leer el archivo y separar los campos. | Mengarelli, Luca Franco |
| `seleccion_nino` | Elegir filas y columnas. Función `leer_tabla`. | Morello, Nino Julián |
| `tipos_lucas` | Convertir los valores a su tipo. | Capella, Lucas |

## Uso

<!-- nino: un ejemplo de leer_tabla y una tabla con cada parámetro (separador, encabezado, tipos,
n_filas, rango, columnas, filtro): qué recibe y qué hace. -->

## Organización

<!-- todos: por qué lo dividimos en tres pasos (leer, convertir, seleccionar) y qué otras opciones
pensamos (una sola función grande, una clase Tabla...). por qué elegimos esta y no otra. -->

## Lectura

<!-- luca: separador por defecto y otros (";", tab, espacios, cualquiera de varios caracteres),
comillas, qué pasa con nombres de columnas vacíos o repetidos, archivos sin encabezado. -->

## Tipos

<!-- lucas: tipos soportados. criterio para adivinar el tipo de una columna (ej. 10, 20 y 30.5;
números mezclados con texto; columna toda vacía). qué textos son booleanos. cómo quedan los nulos.
tipos elegidos por el usuario y el ejemplo de 00123. qué pasa si un valor no se puede convertir. -->

## Selección

<!-- nino: cómo se usa cada opción. cómo se numeran las filas y si el rango incluye los extremos.
si el rango va antes o después del filtro. si con n_filas y filtro se miran las primeras n o se sigue
hasta juntar n. si se puede filtrar por una columna que no se muestra. qué pasa al combinar todo. -->

## Errores

<!-- todos, cada uno lo de su parte: archivo vacío, filas vacías, filas con distinta cantidad de
campos, valores que no se pueden convertir, columna que no existe, filtro que falla. qué hace el
lector en cada caso y un ejemplo de mensaje (con fila y columna cuando corresponde). -->

## Pruebas

<!-- todos: cómo se corren y qué cubren (lectura normal, combinación de opciones y casos con
problemas). qué archivos de ejemplo hay en datos/. -->

## Visualización con pandas

<!-- demo (sin asignar): cómo se pasa el resultado a DataFrame y por qué mostramos también la
lista original (pandas cambia tipos y nulos, por ejemplo None en una columna de números queda NaN). -->
