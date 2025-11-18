# Generar una imagen abstracta basada en el diagrama de bifurcación de la función logística, coloreando cada punto según el valor correspondiente de la variable y la iteración.
import numpy as np
import matplotlib.pyplot as plt

def logistica(r, x):
    return r * x * (1 - x)

def diagrama_bifurcacion(r_valores, x0, n_descarte, n_iteraciones):
    """
    Genera el diagrama de bifurcación para la función logística.

    Args:
        r_valores: Un array de valores de r para los cuales generar el diagrama.
        x0: El valor inicial de x.
        n_descarte: El número de iteraciones para descartar antes de plotear.
        n_iteraciones: El número de iteraciones para plotear para cada valor de r.
    """

    resultados_x = []
    resultados_r = []
    resultados_iter = []

    for r in r_valores:
        x = x0
        # Descartar las primeras iteraciones
        for _ in range(n_descarte):
            x = logistica(r, x)

        # Guardar los resultados para las iteraciones restantes
        for i in range(n_iteraciones):
            x = logistica(r, x)
            resultados_x.append(x)
            resultados_r.append(r)
            resultados_iter.append(i) # Guardar la iteración para colorear

    return resultados_r, resultados_x, resultados_iter


# Parámetros
r_min = 2.5
r_max = 4.0
num_r = 1000
x0 = 0.5
n_descarte = 500
n_iteraciones = 100

# Generar valores de r
r_valores = np.linspace(r_min, r_max, num_r)

# Generar el diagrama de bifurcación
r_resultados, x_resultados, iter_resultados = diagrama_bifurcacion(r_valores, x0, n_descarte, n_iteraciones)

# Crear el gráfico
plt.figure(figsize=(12, 8))
plt.scatter(r_resultados, x_resultados, c=iter_resultados, s=0.1, cmap='viridis') # Colorear por iteración
plt.xlabel("r")
plt.ylabel("x")
plt.title("Diagrama de Bifurcación de la Función Logística")
plt.colorbar(label="Iteración")  # Añadir barra de color para la iteración
plt.savefig('modulos_generados/arte_ciclo_5.png')