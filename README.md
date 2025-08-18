# Algoritmo de Colonia de Hormigas (ACO) + Documento en LaTeX

Presentación de Prezi: https://prezi.com/view/ufEpddeufqBfDl3K8yIG/?referral_token=8hMEbElnB3FN

Este repositorio contiene:

- **Código** para la implementación del algoritmo ACO (Ant Colony Optimization) con distancias euclidianas, incluyendo funciones optimizadas para:
  - Generar matriz de distancias a partir de coordenadas (lat/lng)
  - Construir recorridos de hormigas y calcular su costo óptimo y ruta ideal y peor
  - Visuales con mapa de mejor y peor ruta
- **LaTeX**
  - Código en LaTeX
  - PPT

## 📂 Estructura del proyecto
```
.
├── src/ # Código Python
│ ├── aco.py # Implementación del ACO
│ └── utils.py # Funciones auxiliares (mapear índices, etc.)
├── docs/
│ ├── paper.tex # Documento LaTeX
│ └── paper.pdf # Documento compilado
└── README.md # Este archivo
```

## 🚀 Uso

Para ejecutar directo:

```python
python main.py
```
Si quieres importar en un notebook o en otro script:
```
from src import run_aco, dist_matrix_euclidea
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/it-ces/GA-OPTA-PUJ/main/cities.csv")
distancias, nombres = dist_matrix_euclidea(df, n=20)
resultados = run_aco(50, 50, distancias, 0.1)
print(resultados["mejor_camino"])
```

## 👩‍💻 Autoras

- **Maria Florencia Colombo** – [GitHub](https://github.com/usuario1)
- **Judit Garzón García** – [GitHub](https://github.com/usuario2)
- **Monserrat Zermeño** – [GitHub](https://github.com/usuario3)
- **Mirsha Ramírez Garcia** – [GitHub](https://github.com/usuario3)
- **Ilse Zubieta Martínez** – [GitHub](https://github.com/wer1ix)

