# Tipos

La parte de lectura lee el archivo pero deja todo como texto, o sea el precio llega como "2500.5" y no como 2500.5. Acá hay que pasar cada valor a lo que es: int, float, bool, str, o None si la celda está vacía.

Lo que pide la consigna para esta parte:

- adivinar el tipo de cada columna mirando todos sus valores. Si hay 10, 20 y 30.5 tiene que quedar todo float. Hay que ver qué pasa si se mezclan números con texto o si la columna está toda vacía
- decidir qué cuenta como booleano (true/false, verdadero/falso...)
- que el usuario pueda decir de qué tipo es una columna y que eso tenga prioridad. Ej: si dice que codigo es str, "00123" tiene que quedar "00123" y no 123
- si el usuario pidió int y aparece "hola", no cambiarle el tipo, tirar un error que diga la línea y la columna

Para que encaje con las otras partes, en tipos.py tiene que haber una función `convertir_filas(columnas, filas, tipos=None)`.

Le llega lo que devuelve `leer_filas` (lectura), algo así:

```python
columnas = ["nombre", "precio"]
filas = [(2, ["Cuaderno", "2500.5"]), (3, ["Lapicera", "800"])]
```

(el número de adelante es la línea del archivo, para los mensajes de error). `tipos` es opcional, por ej `{"precio": float}`.

Y tiene que devolver:

```python
[(2, {"nombre": "Cuaderno", "precio": 2500.5}),
 (3, {"nombre": "Lapicera", "precio": 800.0})]
```

También: un pruebas.py con asserts, una carpeta datos/ con csv chiquitos para probar, y un párrafo para el readme explicando lo que se decidió. Solo cosas que vimos en la materia.
