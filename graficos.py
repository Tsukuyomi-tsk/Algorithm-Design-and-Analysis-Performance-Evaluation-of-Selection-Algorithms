"""Graficos a partir de resultados/resumen.csv.

Autor: Vicente Siglic - Tarea Practica RA2, Diseno y Analisis de Algoritmos (UCN)
"""
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = "resultados"
filas = []
with open(f"{R}/resumen.csv", newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        r["n"], r["k"] = int(r["n"]), int(r["k"])
        r["t"], r["c"] = float(r["tiempo_prom_ms"]), float(r["comparaciones_prom"])
        r["d"] = float(r["desv_est_ms"])
        filas.append(r)

ALGS = ["ordenamiento", "quickselect", "bfprt"]

# 1-4: tiempo vs n por distribucion (k = n/2)
for dist in ["aleatorio", "ascendente", "descendente", "repetidos"]:
    plt.figure(figsize=(6, 4))
    for a in ALGS:
        pts = sorted((r["n"], r["t"], r["d"]) for r in filas
                     if r["algoritmo"] == a and r["tipo_datos"] == dist and r["k"] == r["n"] // 2)
        plt.errorbar([p[0] for p in pts], [p[1] for p in pts], yerr=[p[2] for p in pts],
                     marker="o", capsize=3, label=a)
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("n"); plt.ylabel("Tiempo promedio (ms)")
    plt.title(f"Tiempo vs n - datos {dist}, k = n/2")
    plt.grid(True, which="both", alpha=0.3); plt.legend()
    plt.tight_layout(); plt.savefig(f"{R}/tiempo_{dist}.png", dpi=150); plt.close()

# 5: comparaciones vs k (n = 10^6, aleatorio)
N = 10**6
plt.figure(figsize=(6, 4))
etiquetas = ["k=1", "k=n/2", "k=n"]
ancho = 0.25
for i, a in enumerate(ALGS):
    vals = []
    for kk in (1, N // 2, N):
        vals.append(next(r["c"] for r in filas if r["algoritmo"] == a and r["n"] == N
                         and r["tipo_datos"] == "aleatorio" and r["k"] == kk))
    plt.bar([x + i * ancho for x in range(3)], vals, ancho, label=a)
plt.xticks([x + ancho for x in range(3)], etiquetas)
plt.ylabel("Comparaciones (promedio)"); plt.title("Comparaciones segun k (n = 10^6, aleatorio)")
plt.legend(); plt.tight_layout(); plt.savefig(f"{R}/comparaciones_k.png", dpi=150); plt.close()

# 6: peor caso de Quickselect (ascendente, k = n)
plt.figure(figsize=(6, 4))
for a, et in (("quickselect_fijo", "Quickselect pivote fijo"), ("quickselect", "Quickselect pivote aleatorio")):
    pts = sorted((r["n"], r["t"]) for r in filas
                 if r["algoritmo"] == a and r["tipo_datos"] == "ascendente" and r["k"] == r["n"]
                 and (a == "quickselect_fijo" or r["n"] <= 10**5))
    plt.plot([p[0] for p in pts], [p[1] for p in pts], marker="o", label=et)
fijo = sorted((r["n"], r["t"]) for r in filas if r["algoritmo"] == "quickselect_fijo")
n0, t0 = fijo[0]
ns = [p[0] for p in fijo]
plt.plot(ns, [t0 * (n / n0) ** 2 for n in ns], "k--", alpha=0.5, label="referencia n^2")
plt.xscale("log"); plt.yscale("log")
plt.xlabel("n"); plt.ylabel("Tiempo promedio (ms)")
plt.title("Peor caso de Quickselect (ascendente, k = n)")
plt.grid(True, which="both", alpha=0.3); plt.legend()
plt.tight_layout(); plt.savefig(f"{R}/peor_caso_quickselect.png", dpi=150); plt.close()
print("Graficos generados en", R)
