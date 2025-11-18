# Un script que genere arte ASCII fractal en tiempo real, representando conjuntos de Mandelbrot o Julia con diferentes paletas de colores dinámicas.
import time
import math
import random

def mandelbrot(x, y, max_iter):
    """Calcula si un punto (x, y) pertenece al conjunto de Mandelbrot."""
    c = complex(x, y)
    z = 0
    for n in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return n
    return max_iter

def julia(x, y, c, max_iter):
    """Calcula si un punto (x, y) pertenece al conjunto de Julia."""
    z = complex(x, y)
    for n in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return n
    return max_iter


def generate_fractal_ascii(width, height, x_min, x_max, y_min, y_max, max_iter, fractal_type="mandelbrot", julia_c=None):
    """Genera arte ASCII fractal en tiempo real."""

    color_palette = [" ", ".", ":", "-", "=", "+", "*", "#", "%", "@"]
    palette_size = len(color_palette)

    for row in range(height):
        line = ""
        for col in range(width):
            x = x_min + (x_max - x_min) * col / width
            y = y_min + (y_max - y_min) * row / height

            if fractal_type == "mandelbrot":
                iteration = mandelbrot(x, y, max_iter)
            elif fractal_type == "julia":
                if julia_c is None:
                    julia_c = complex(-0.4, 0.6)  # Valor por defecto para el conjunto de Julia
                iteration = julia(x, y, julia_c, max_iter)
            else:
                iteration = 0 # Manejo de error

            color_index = int((iteration / max_iter) * (palette_size - 1))
            line += color_palette[color_index]
        print(line)


if __name__ == "__main__":
    width = 80
    height = 40
    max_iterations = 50

    # Mandelbrot
    print("Mandelbrot Set:")
    generate_fractal_ascii(width, height, -2.0, 1.0, -1.5, 1.5, max_iterations, "mandelbrot")
    time.sleep(1) # pausa para visualización

    # Julia
    print("\nJulia Set:")
    generate_fractal_ascii(width, height, -1.5, 1.5, -1.5, 1.5, max_iterations, "julia", julia_c=complex(-0.4, 0.6))
    time.sleep(1)


    #Julia Dinámico con color paleta aleatoria.
    print("\nJulia Set Dinámico:")
    for _ in range(3): # Mostrar varias iteraciones
        julia_c = complex(random.uniform(-1, 1), random.uniform(-1, 1))
        generate_fractal_ascii(width, height, -1.5, 1.5, -1.5, 1.5, max_iterations, "julia", julia_c=julia_c)
        time.sleep(1)