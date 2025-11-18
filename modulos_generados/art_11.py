import numpy as np
import matplotlib.pyplot as plt

# Inspirado en el Número 11: Dualidad y Equilibrio
# Dos formas abstractas idénticas pero con sutiles diferencias, que interactúan entre sí.

# Definir el tamaño de la imagen
width, height = 512, 512

# Crear un lienzo en blanco
img = np.zeros((height, width, 3), dtype=np.uint8)  # 3 para RGB

# Definir colores
color1 = [255, 100, 0]  # Naranja
color2 = [0, 100, 255]  # Azul

# Función para dibujar una forma abstracta (elipse)
def draw_abstract_shape(img, center_x, center_y, radius_x, radius_y, color, angle=0):
    for y in range(height):
        for x in range(width):
            #Transformar coordenadas al sistema de coordenadas de la elipse
            x_rel = x - center_x
            y_rel = y - center_y

            #Rotar las coordenadas
            x_rot = x_rel * np.cos(np.radians(angle)) - y_rel * np.sin(np.radians(angle))
            y_rot = x_rel * np.sin(np.radians(angle)) + y_rel * np.cos(np.radians(angle))


            if ((x_rot**2) / (radius_x**2) + (y_rot**2) / (radius_y**2)) < 1:
                img[y, x] = color

# Dibujar dos formas abstractas (elipses) con sutiles diferencias
draw_abstract_shape(img, width // 4, height // 2, 80, 60, color1, angle=15)
draw_abstract_shape(img, 3 * width // 4, height // 2, 85, 65, color2, angle=-10) # Ligeramente diferente radio y ángulo


# Crear una figura y mostrar la imagen
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(img)
ax.axis('off')  # Ocultar los ejes

# Guardar la imagen en un archivo
plt.savefig('modulos_generados/art_11.png')
plt.close(fig)