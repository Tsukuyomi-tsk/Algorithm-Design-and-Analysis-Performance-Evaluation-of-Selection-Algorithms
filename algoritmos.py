"""Algoritmos de seleccion (k-esimo menor, k desde 1).

Autor: Vicente Siglic - Tarea Practica RA2, Diseno y Analisis de Algoritmos (UCN)

Cada funcion recibe (A, k) y devuelve (valor, comparaciones).
Se cuentan solo comparaciones entre elementos del arreglo.
"""
import random


def seleccion_ordenamiento(A, k):
    """Ordena con merge sort propio y devuelve la posicion k. O(n log n)."""
    c = 0

    def ms(a):
        nonlocal c
        n = len(a)
        if n <= 1:
            return a
        m = n // 2
        izq, der = ms(a[:m]), ms(a[m:])
        out = []
        i = j = 0
        ni, nj = len(izq), len(der)
        while i < ni and j < nj:
            c += 1
            if der[j] < izq[i]:
                out.append(der[j]); j += 1
            else:
                out.append(izq[i]); i += 1
        out.extend(izq[i:])
        out.extend(der[j:])
        return out

    B = ms(list(A))
    return B[k - 1], c


def quickselect(A, k, pivote="aleatorio"):
    """Quickselect con particion de Hoare, iterativo, sobre una copia.

    pivote: "aleatorio" (O(n) esperado) o "primero" (peor caso O(n^2) en datos ordenados).
    """
    a = list(A)
    c = 0
    lo, hi = 0, len(a) - 1
    k -= 1
    while lo < hi:
        p = random.randint(lo, hi) if pivote == "aleatorio" else lo
        a[p], a[lo] = a[lo], a[p]
        pv = a[lo]
        i, j = lo - 1, hi + 1
        while True:
            i += 1
            c += 1
            while a[i] < pv:
                i += 1
                c += 1
            j -= 1
            c += 1
            while a[j] > pv:
                j -= 1
                c += 1
            if i >= j:
                break
            a[i], a[j] = a[j], a[i]
        if k <= j:
            hi = j
        else:
            lo = j + 1
    return a[lo], c


def bfprt(A, k):
    """Mediana de medianas (BFPRT): grupos de 5, particion en 3 vias. O(n) peor caso."""
    c = 0

    def ordenar_grupo(g):  # insercion, para <= 5 elementos
        nonlocal c
        for i in range(1, len(g)):
            x = g[i]
            j = i - 1
            while j >= 0:
                c += 1
                if g[j] > x:
                    g[j + 1] = g[j]
                    j -= 1
                else:
                    break
            g[j + 1] = x

    def seleccionar(a, k):  # k desde 0
        nonlocal c
        while True:
            n = len(a)
            if n <= 5:
                g = list(a)
                ordenar_grupo(g)
                return g[k]
            medianas = []
            for i in range(0, n, 5):
                g = a[i:i + 5]
                ordenar_grupo(g)
                medianas.append(g[(len(g) - 1) // 2])
            p = seleccionar(medianas, (len(medianas) - 1) // 2)
            menores, mayores, iguales = [], [], 0
            for x in a:
                c += 1
                if x < p:
                    menores.append(x)
                else:
                    c += 1
                    if x > p:
                        mayores.append(x)
                    else:
                        iguales += 1
            if k < len(menores):
                a = menores
            elif k < len(menores) + iguales:
                return p
            else:
                k -= len(menores) + iguales
                a = mayores

    return seleccionar(list(A), k - 1), c


if __name__ == "__main__":
    random.seed(1)
    algs = {
        "ordenamiento": seleccion_ordenamiento,
        "quickselect": quickselect,
        "quickselect_fijo": lambda A, k: quickselect(A, k, "primero"),
        "bfprt": bfprt,
    }
    casos = [[7], [3, 3, 3, 3, 3], [1, 2], [2, 1], list(range(50)), list(range(50, 0, -1))]
    casos += [[random.randint(0, 3) for _ in range(n)] for n in (2, 5, 6, 11, 100)]
    casos += [[random.randint(0, 1000) for _ in range(n)] for n in (3, 10, 57, 500)]
    total = 0
    for A in casos:
        for k in sorted({1, len(A), (len(A) + 1) // 2, *random.sample(range(1, len(A) + 1), min(3, len(A)))}):
            esperado = sorted(A)[k - 1]
            for nombre, f in algs.items():
                v, _ = f(A, k)
                assert v == esperado, (nombre, A, k, v, esperado)
                total += 1
    print(f"OK: {total} pruebas (k=1, k=n, repetidos, n=1) pasaron")
