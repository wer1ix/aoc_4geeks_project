# -*- coding: utf-8 -*-
import random
import numpy as np
import pandas as pd
from utils import dist_matrix_euclidea, mostrar_ruta_folium

# ===================== Datos y distancias =====================

URL = "https://raw.githubusercontent.com/it-ces/GA-OPTA-PUJ/main/cities.csv"
df = pd.read_csv(URL)
distancias, nombres = dist_matrix_euclidea(df, n=20)

# ===================== Núcleo ACO =====================

def pick_move(actual, visitados, dist, pher, alpha, beta):
    """Elige el siguiente nodo según (tau^alpha) * (eta^beta)."""
    n = dist.shape[0]
    candidatos = [j for j in range(n) if j not in visitados]
    if not candidatos:
        return None

    tau = np.array([pher[actual, j] for j in candidatos]) ** alpha
    eta = (1.0 / np.array([dist[actual, j] for j in candidatos])) ** beta
    w = tau * eta

    if not np.isfinite(w).any() or w.sum() == 0:
        return random.choice(candidatos)

    p = w / w.sum()
    return random.choices(candidatos, weights=p, k=1)[0]

def gen_path(start, dist, pher, alpha, beta):
    """Construye un tour cerrado y devuelve (path, costo)."""
    n = dist.shape[0]
    path = [start]
    visitados = {start}
    actual = start

    for _ in range(n - 1):
        nxt = pick_move(actual, visitados, dist, pher, alpha, beta)
        path.append(nxt)
        visitados.add(nxt)
        actual = nxt

    path.append(start)  # cerrar ciclo

    # costo total del tour
    costo = float(np.sum([dist[path[i], path[i+1]] for i in range(len(path) - 1)]))
    return path, costo

def generar_paths_y_costos(n_ants, dist, pher, alpha, beta):
    """Genera tours para n_ants hormigas. Retorna lista de dicts con path y cost."""
    n = dist.shape[0]
    res = []
    for _ in range(n_ants):
        start = random.randrange(n)
        path, cost = gen_path(start, dist, pher, alpha, beta)
        res.append({"path": path, "cost": cost})
    return res

def update_feromonas(pher, hormigas, Q, decay, n_best=3, tau_min=1e-9, tau_max=None):
    """Evaporación + refuerzo con las n_best hormigas."""
    pher *= (1.0 - decay)

    top = sorted(hormigas, key=lambda h: h["cost"])[:n_best]
    for h in top:
        delta = Q / h["cost"]
        camino = h["path"]
        for i in range(len(camino) - 1):
            a, b = camino[i], camino[i+1]
            pher[a, b] += delta
            pher[b, a] += delta  # simétrico

    # Acotar o asegurar mínimo
    if tau_max is not None:
        np.clip(pher, tau_min, tau_max, out=pher)
    else:
        np.maximum(pher, tau_min, out=pher)

    return pher

def run_aco(n_iterations, n_ants, dist, pher_init, alpha=1.0, beta=2.0, Q=10.0, decay=0.5,
            n_best=3, guardar_historia=False, verbose=True):
    """
    Ejecuta ACO y retorna:
      - pheromone: matriz final de feromonas
      - mejor_costo / mejor_camino
      - peor_costo / peor_camino
      - historiales opcionales
    """
    n = dist.shape[0]
    pher = np.full((n, n), pher_init, dtype=float)
    np.fill_diagonal(pher, 0.0)

    mejor_cost, mejor_path = float('inf'), None
    peor_cost, peor_path = float('-inf'), None
    hist_cost_min, hist_cost_max, hist_pher = [], [], []

    for it in range(1, n_iterations + 1):
        hormigas = generar_paths_y_costos(n_ants, dist, pher, alpha, beta)

        costs = [h["cost"] for h in hormigas]
        paths = [h["path"] for h in hormigas]
        cmin_idx, cmax_idx = int(np.argmin(costs)), int(np.argmax(costs))
        cmin, pmin = costs[cmin_idx], paths[cmin_idx]
        cmax, pmax = costs[cmax_idx], paths[cmax_idx]

        if cmin < mejor_cost:
            mejor_cost, mejor_path = cmin, pmin
        if cmax > peor_cost:
            peor_cost, peor_path = cmax, pmax

        hist_cost_min.append(cmin)
        hist_cost_max.append(cmax)

        pher = update_feromonas(pher, hormigas, Q=Q, decay=decay, n_best=n_best)
        if guardar_historia:
            hist_pher.append(pher.copy())

        if verbose and (it % 10 == 0 or it == 1):
            print(f"Iter {it}/{n_iterations}  best_it={cmin:.4f}  best_glob={mejor_cost:.4f}")

    return {
        "pheromone": pher,
        "mejor_costo": mejor_cost,
        "mejor_camino": mejor_path,
        "peor_costo": peor_cost,
        "peor_camino": peor_path,
        "hist_cost_min": hist_cost_min,
        "hist_cost_max": hist_cost_max,
        "hist_feromonas": hist_pher if guardar_historia else None
    }

# ===================== Ejecución directa =====================

if __name__ == "__main__":
    feromona_inicial = 0.1
    resultados = run_aco(
        n_iterations=100,
        n_ants=100,
        dist=distancias,
        pher_init=feromona_inicial,
        alpha=1.0,
        beta=2.0,
        Q=10.0,
        decay=0.5,
        n_best=3,
        guardar_historia=False,
        verbose=True
    )

    mejor_ruta = resultados["mejor_camino"]
    peor_ruta = resultados["mejor_camino"]

    print("\nMejor camino:", resultados["mejor_camino"])
    print("Costo total:", resultados["mejor_costo"])

    mostrar_ruta_folium(df, nombres, mejor_ruta, pausa_segundos=1)
