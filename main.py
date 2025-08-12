# main.py
import pandas as pd
from src import run_aco, dist_matrix_euclidea

# Datos
url = "https://raw.githubusercontent.com/it-ces/GA-OPTA-PUJ/main/cities.csv"
df = pd.read_csv(url)
distancias, nombres = dist_matrix_euclidea(df, n=20)

# Parámetros
feromona_inicial = 0.1

# Ejecución
resultados = run_aco(
    n_iterations=50,
    n_ants=50,
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

# Resultados
print("\nMejor camino:", resultados["mejor_camino"])
print("Costo total:", resultados["mejor_costo"])
