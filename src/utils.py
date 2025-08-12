# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from geopy.distance import geodesic
from folium.plugins import AntPath
import folium
import time
from IPython.display import display, clear_output

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

def mostrar_ruta_folium(df, nombres, mejor_ruta, peor_ruta, pausa_segundos=1):
    # Centrar el mapa en el inicio de la mejor ruta
    lat_centro = df.loc[mejor_ruta[0], 'lat']
    lng_centro = df.loc[mejor_ruta[0], 'lng']
    mapa = folium.Map(location=[lat_centro, lng_centro], zoom_start=6)

    # Coordenadas de las rutas
    coords_mejor = [(df.loc[i, 'lat'], df.loc[i, 'lng']) for i in mejor_ruta]
    coords_peor = [(df.loc[i, 'lat'], df.loc[i, 'lng']) for i in peor_ruta]



    # ===== Marcadores para peor ruta (rojos) =====
    for idx in peor_ruta:
        folium.Marker(
            location=[df.loc[idx, 'lat'], df.loc[idx, 'lng']],
            popup=f"Peor: {nombres[idx]}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(mapa)



    # ===== Animación peor ruta =====
    for i in range(len(coords_peor) - 1):
        segmento = coords_peor[i:i+2]
        AntPath(
            locations=segmento,
            color='red',
            weight=5,
            delay=1000
        ).add_to(mapa)
        display(mapa)
        time.sleep(pausa_segundos)
        clear_output(wait=True)

    # ===== Dibujar rutas completas =====

    folium.PolyLine(coords_peor, color='red', weight=4, opacity=0.7).add_to(mapa)

    display(mapa)