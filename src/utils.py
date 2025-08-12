# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from geopy.distance import geodesic

# Original
def generar_coordenadas(df, n=20):
    required_columns = {'city', 'lat', 'lng'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"El DataFrame debe contener las columnas: {required_columns}")

    ciudades = df.head(n).reset_index(drop=True)
    nombres = ciudades['city'].tolist()
    num_ciudades = len(ciudades)
    distancias = np.zeros((num_ciudades, num_ciudades))

    for i in range(num_ciudades):
        coord_i = (ciudades.loc[i, 'lat'], ciudades.loc[i, 'lng'])
        for j in range(i + 1, num_ciudades):
            coord_j = (ciudades.loc[j, 'lat'], ciudades.loc[j, 'lng'])
            distancia = geodesic(coord_i, coord_j).kilometers
            distancias[i][j] = distancia
            distancias[j][i] = distancia

    return np.round(distancias, 2), nombres

# Euclidiana
def dist_matrix_euclidea(df: pd.DataFrame, n: int = 20, col_lat: str = 'lat', col_lng: str = 'lng'):
    df_ = df[['city', col_lat, col_lng]].head(n).reset_index(drop=True)
    coords = df_[[col_lat, col_lng]].to_numpy(dtype=float)  # (n, 2)
    dif = coords[:, None, :] - coords[None, :, :]           # (n, n, 2)
    dist = np.sqrt((dif ** 2).sum(axis=2))                  # (n, n)
    np.fill_diagonal(dist, np.inf)                          # evita 1/0 al calcular η=1/d
    return dist, df_['city'].tolist()
