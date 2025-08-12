# -*- coding: utf-8 -*-
"""
Paquete src: contiene la implementación del Algoritmo de Colonia de Hormigas (ACO) 
y utilidades para el cálculo de distancias y manejo de datos.
"""

from .aco import run_aco
from .utils import dist_matrix_euclidea

__all__ = [
    "run_aco",
    "dist_matrix_euclidea"
]
