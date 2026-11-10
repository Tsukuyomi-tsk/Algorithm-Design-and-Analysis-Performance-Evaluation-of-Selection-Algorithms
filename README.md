# Tarea Práctica RA2 – Evaluación del rendimiento de algoritmos de selección

Autor: Vicente Siglic — Diseño y Análisis de Algoritmos, UCN.

Algoritmos implementados (Python puro): selección por ordenamiento (merge sort), Quickselect (Hoare) y mediana de medianas (BFPRT).

## Requisitos
- Python 3.13 (probado con 3.13)
- `pip install matplotlib` (solo para los gráficos; el resto usa la librería estándar)

## Uso (desde esta carpeta, en orden)
```bash
python algoritmos.py     # pruebas de correctitud (k=1, k=n, repetidos, n=1)
python experimentos.py   # corre todos los experimentos (~20-30 min)
python graficos.py       # genera los gráficos
```

## Archivos
- `algoritmos.py` – los tres algoritmos (+ Quickselect con pivote fijo para la mini-prueba del peor caso).
- `experimentos.py` – generación de datos, verificación contra `sorted(A)[k-1]`, mediciones.
- `graficos.py` – gráficos a partir de `resumen.csv`.
- `resultados/resultados_crudos.csv` – una fila por repetición (datos crudos).
- `resultados/resumen.csv` – una fila por combinación (promedio, desviación estándar, comparaciones, orden teórico).
- `resultados/entorno.txt` – hardware/software usado.
- `resultados/*.png` – gráficos.
- `informe.md` – borrador del informe (exportar a PDF).

## Cómo reproducir los resultados
1. Instalar dependencias: `pip install matplotlib`.
2. Ejecutar `python algoritmos.py`: corre las pruebas de correctitud (deben pasar todas).
3. Ejecutar `python experimentos.py`: genera los datos con semilla fija (12345), verifica cada resultado contra `sorted(A)[k-1]`, mide 10 repeticiones por combinación y **sobrescribe** `resultados/resultados_crudos.csv`, `resultados/resumen.csv` y `resultados/entorno.txt`. Demora ~20–30 min; el avance se imprime en consola.
4. Ejecutar `python graficos.py`: regenera los PNG en `resultados/` a partir de `resumen.csv`.
5. Completar a mano la RAM en `resultados/entorno.txt` (el script no la detecta).

Notas:
- Los datos de entrada son idénticos en cada corrida (semilla fija). Los **tiempos** variarán según el equipo y la carga del sistema; las comparaciones de ordenamiento y BFPRT salen iguales, y las de Quickselect (pivote aleatorio) pueden variar levemente.
- Si se vuelve a correr, los números de `informe.md` (secciones 5 y 6 y Anexo A) deben actualizarse con los nuevos `resumen.csv`.
- Para una prueba rápida, bajar `TAMANOS` y `REPS` al inicio de `experimentos.py`.
