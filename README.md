<img src="https://raw.githubusercontent.com/ee-unr/programacion-2/main/imgs/serpiente.png" width="60" align="right" alt="serpiente de la cátedra">

# Lector de datos tabulares

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white) ![Programación II, UNR 2026](https://img.shields.io/badge/Programaci%C3%B3n_II-UNR_2026-2b2b2b?style=flat-square)

## Avance

<!-- progreso -->
```text
Lectura    Luca   ██████████████████████████████  100 %   terminado
Tipos      Lucas  ██████████████████████████████  100 %   terminado
Selección  Nino   ██████████████████████░░░░░░░░   75 %   falta: seleccionar, leer_tabla
Total             ████████████████████████████░░   93 %
```

<sub>Actualizado el 28/10/2026.</sub>
<!-- /progreso -->

Trabajo práctico grupal de Programación II. Facultad de Ciencias Económicas y Estadística, UNR, 2026.

Módulo de Python que lee tablas almacenadas en archivos de texto plano (CSV y formatos similares)
y las devuelve como una lista de diccionarios.

| Integrante | Parte | Archivo |
|---|---|---|
| Mengarelli, Luca Franco | Lectura | `lector/lectura.py` |
| Capella, Lucas | Tipos | `lector/tipos.py` |
| Morello, Nino Julián | Selección | `lector/seleccion.py` |

## Entrega

El zip `G17_Capella_Mengarelli_Morello.zip` tiene la misma organización que este repositorio,
sin el README:

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
