import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Idea: Degradado de color que avanza gradualmente a través de 14 pasos.

# Define una paleta de colores
colors = list(mcolors.TABLEAU_COLORS.values())
num_colors = len(colors)

# Asegura que haya al menos 14 colores para el degradado
if num_colors < 2:
    print("Error: Se necesitan al menos 2 colores en la paleta.")
    exit()

n_steps = 14

# Crea una figura y ejes
fig, ax = plt.subplots(figsize=(10, 1))  # Ajusta el tamaño según sea necesario

# Crea el degradado de color
cmap = mcolors.LinearSegmentedColormap.from_list("my_cmap", colors[:2], N=n_steps)

# Crea una secuencia de valores para el mapa de colores
x = np.linspace(0, 1, n_steps)

# Crea una imagen para mostrar el degradado
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

# Muestra el degradado en el eje
ax.imshow(gradient, aspect='auto', cmap=cmap)

# Elimina las marcas del eje
ax.set_axis_off()

# Guarda la imagen
plt.savefig('modulos_generados/art_14.png')

plt.close(fig)  # Cierra la figura para liberar memoria