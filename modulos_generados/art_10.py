import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def generar_arte_abstracto(nombre_archivo="art_abstracto.png"):
    """Genera una imagen abstracta inspirada en la descripción proporcionada."""

    # Configuración de la imagen
    ancho, alto = 1024, 1024
    imagen = np.zeros((alto, ancho, 3))

    # Paleta de colores
    colores = {
        "azul_profundo": np.array([0.1, 0.2, 0.5]),
        "turquesa_brillante": np.array([0.2, 0.8, 0.9]),
        "naranja_quemado": np.array([0.8, 0.3, 0.1]),
        "magenta_electrico": np.array([0.9, 0.1, 0.8]),
    }

    # Función para crear un fractal deformado (simulado)
    def fractal_deformado(x, y, escala=100, iteraciones=5):
        """Crea una forma fractal deformada.  Simula un fractal sin usar la ecuación real para mejorar la velocidad."""
        valor = 0
        for i in range(iteraciones):
            x_offset = np.sin(x / escala * i) * escala / 10
            y_offset = np.cos(y / escala * i) * escala / 10
            valor += np.sin(np.sqrt((x + x_offset)**2 + (y + y_offset)**2) / (escala / (i + 1)))
        return valor

    # Generar la imagen pixel por pixel
    for y in range(alto):
        for x in range(ancho):
            # Calcular un valor fractal deformado
            valor_fractal = fractal_deformado(x, y, escala=200) + fractal_deformado(x, y, escala=50)

            # Mapear el valor fractal a colores
            r = (colores["azul_profundo"][0] + colores["turquesa_brillante"][0] * valor_fractal) % 1
            g = (colores["naranja_quemado"][1] + colores["magenta_electrico"][1] * valor_fractal) % 1
            b = (colores["turquesa_brillante"][2] + colores["azul_profundo"][2] * valor_fractal) % 1

            # Añadir ruido para la textura
            ruido = np.random.rand() * 0.05
            r = np.clip(r + ruido, 0, 1)
            g = np.clip(g + ruido, 0, 1)
            b = np.clip(b + ruido, 0, 1)


            imagen[y, x] = [r, g, b]

    # Convertir a formato de imagen matplotlib
    plt.imsave(nombre_archivo, imagen)



# Generar y guardar la imagen
generar_arte_abstracto(nombre_archivo="modulos_generados/art_10.png")