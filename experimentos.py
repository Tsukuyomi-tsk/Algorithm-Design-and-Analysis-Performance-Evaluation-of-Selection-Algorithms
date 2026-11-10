"""Experimentos de rendimiento de algoritmos de seleccion.

Autor: Vicente Siglic - Tarea Practica RA2, Diseno y Analisis de Algoritmos (UCN)

Genera resultados/resultados_crudos.csv, resultados/resumen.csv y resultados/entorno.txt
"""
import csv
import os
import platform
import random
import statistics
import sys
import time

from algoritmos import bfprt, quickselect, seleccion_ordenamiento

TAMANOS = [10**3, 10**4, 10**5, 5 * 10**5, 10**6]
DISTRIBUCIONES = ["aleatorio", "ascendente", "descendente", "repetidos"]
REPS = 10
SEMILLA = 12345
SALIDA = "resultados"

ALGORITMOS = {
    "ordenamiento": seleccion_ordenamiento,
    "quickselect": quickselect,
    "bfprt": bfprt,
}
ORDEN_TEORICO = {
    "ordenamiento": "O(n log n)",
    "quickselect": "O(n) esperado, O(n^2) peor caso",
    "bfprt": "O(n) peor caso",
    "quickselect_fijo": "O(n^2) peor caso (datos ordenados)",
}
# Mini-prueba del peor caso: Quickselect con pivote fijo (primer elemento)
TAMANOS_PEOR_CASO = [1000, 2000, 4000, 8000]


def generar(n, dist):
    rng = random.Random(f"{SEMILLA}-{n}-{dist}")
    if dist == "aleatorio":
        return [rng.randint(0, 10**9) for _ in range(n)]
    if dist == "ascendente":
        return list(range(n))
    if dist == "descendente":
        return list(range(n, 0, -1))
    if dist == "repetidos":
        return [rng.randint(0, 9) for _ in range(n)]
    raise ValueError(dist)


def medir(escritor, nombre, f, A, n, dist, k, ref):
    # verificacion de correccion (sin medir), tambien sirve de calentamiento
    v, _ = f(A, k)
    if v != ref:
        sys.exit(f"ERROR de correccion: {nombre} n={n} {dist} k={k}: {v} != {ref}")
    for rep in range(1, REPS + 1):
        copia = list(A)  # misma entrada para todos; la copia queda fuera del cronometro
        t0 = time.perf_counter()
        v, comps = f(copia, k)
        ms = (time.perf_counter() - t0) * 1000
        assert v == ref
        escritor.writerow([nombre, n, dist, k, rep, f"{ms:.6f}", comps])


def main():
    os.makedirs(SALIDA, exist_ok=True)
    random.seed(SEMILLA)  # pivotes aleatorios reproducibles
    ruta_crudos = os.path.join(SALIDA, "resultados_crudos.csv")
    with open(ruta_crudos, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["algoritmo", "n", "tipo_datos", "k", "repeticion", "tiempo_ms", "comparaciones"])
        for n in TAMANOS:
            for dist in DISTRIBUCIONES:
                A = generar(n, dist)
                B = sorted(A)
                for k in (1, n // 2, n):
                    for nombre, f in ALGORITMOS.items():
                        medir(w, nombre, f, A, n, dist, k, B[k - 1])
                    fh.flush()
                print(f"listo n={n} {dist}", flush=True)
        # mini-prueba peor caso
        fijo = lambda A, k: quickselect(A, k, "primero")
        for n in TAMANOS_PEOR_CASO:
            A = generar(n, "ascendente")
            medir(w, "quickselect_fijo", fijo, A, n, "ascendente", n, A[n - 1])
            fh.flush()
            print(f"listo peor caso n={n}", flush=True)

    # resumen
    grupos = {}
    with open(ruta_crudos, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            grupos.setdefault((r["algoritmo"], int(r["n"]), r["tipo_datos"], int(r["k"])), []).append(r)
    with open(os.path.join(SALIDA, "resumen.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["algoritmo", "n", "tipo_datos", "k", "tiempo_prom_ms", "desv_est_ms",
                    "comparaciones_prom", "orden_teorico"])
        for (alg, n, dist, k), filas in grupos.items():
            t = [float(r["tiempo_ms"]) for r in filas]
            c = [int(r["comparaciones"]) for r in filas]
            w.writerow([alg, n, dist, k, f"{statistics.mean(t):.6f}", f"{statistics.stdev(t):.6f}",
                        f"{statistics.mean(c):.1f}", ORDEN_TEORICO[alg]])

    with open(os.path.join(SALIDA, "entorno.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"Sistema operativo: {platform.platform()}\n")
        fh.write(f"Procesador: {platform.processor()}\n")
        fh.write(f"Python: {platform.python_version()} ({platform.python_implementation()})\n")
        fh.write("Bibliotecas: random, time, csv, statistics (estandar); matplotlib (graficos)\n")
        fh.write("RAM: COMPLETAR\n")
    print("Terminado")


if __name__ == "__main__":
    main()
