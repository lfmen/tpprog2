# Selección

Esta parte junta todo: usa la de lectura (leer el archivo) y la de tipos (convertir los valores) y después se queda solo con lo que pidió el usuario.

Lo que pide la consigna es que se pueda:

1. pedir una cantidad de filas (las primeras 5, por ej)
2. pedir un rango de filas (de la 3 a la 8)
3. elegir qué columnas mostrar
4. filtrar con una función que recibe la fila y devuelve True o False, tipo `filtro=lambda fila: fila["cantidad"] < 10`

Y que todo se pueda combinar. Hay que decidir algunas cosas y después explicarlas:

- si las filas se cuentan desde 0 o desde 1, y si el rango incluye los extremos
- si el rango va antes o después del filtro
- si se piden 10 filas con un filtro, ¿son las primeras 10 del archivo o se sigue leyendo hasta tener 10 que cumplan?
- si se puede filtrar por una columna que después no se muestra
- qué pasa si piden una columna que no existe o si el filtro tira error

En lector.py tiene que estar la función que usa todo el mundo:

```python
leer_tabla(ruta, separador=",", encabezado=True, tipos=None,
           n_filas=None, rango=None, columnas=None, filtro=None)
```

Adentro llama a `leer_filas` (lectura), después a `convertir_filas` (tipos), y aplica las opciones. Devuelve una lista de diccionarios, por ej:

```python
leer_tabla("productos.csv", columnas=["nombre", "precio"], filtro=lambda fila: fila["cantidad"] < 10)
# [{"nombre": "Carpeta", "precio": 3200.0}]
```

Ojo que convertir_filas devuelve cada fila con el número de línea adelante: `(2, {"nombre": "Cuaderno", ...})`. Ese número sirve para decir en qué línea falló el filtro.

También: un pruebas.py con asserts, una carpeta datos/ con csv chiquitos, y un párrafo para el readme con lo que se decidió. Solo cosas que vimos en la materia.
