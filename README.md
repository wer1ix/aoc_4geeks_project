# Algoritmo de Colonia de Hormigas (ACO) + Documento en LaTeX

Este repositorio contiene:

- **Código Python** para la implementación del algoritmo ACO (Ant Colony Optimization) con distancias euclidianas, incluyendo funciones optimizadas para:
  - Generar matriz de distancias a partir de coordenadas (lat/lng)
  - Construir recorridos de hormigas y calcular sus c

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

Ejemplo de extracción de coordenadas en orden a partir de una lista de índices:

```python
def extraer_coords(df, lista_indices, col_lat='lat', col_lng='lng'):
    """Devuelve un DataFrame con lat/lng en el orden dado por lista_indices."""
    return df.iloc[lista_indices][[col_lng, col_lat]].reset_index(drop=True)

# Ejemplo
coords = extraer_coords(df, [1, 4, 2, 0, 3])
print(coords)
```

## 👩‍💻 Autoras

- **Maria Florencia Colombo** – [GitHub](https://github.com/usuario1)
- **Judith** – [GitHub](https://github.com/usuario2)
- **Monserrat Zermeño** – [GitHub](https://github.com/usuario3)
- **Mirsha Ramírez** – [GitHub](https://github.com/usuario3)
- **Ilse Zubieta** – [GitHub](https://github.com/wer1ix)

