# Un script que genere una imagen abstracta basada en la simulación de gotas de agua cayendo y expandiéndose en una superficie, con colores y opacidades aleatorias que se superponen para crear un patrón complejo.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random

def generate_abstract_art(width=512, height=512, num_drops=50):
    """
    Generates an abstract image based on simulated water droplets.

    Args:
        width (int): Width of the image in pixels.
        height (int): Height of the image in pixels.
        num_drops (int): Number of simulated water drops.

    Returns:
        None. Saves the image to 'modulos_generados/arte_ciclo_4.png'.
    """

    image = np.zeros((height, width, 4), dtype=float) # RGBA

    for _ in range(num_drops):
        # Random drop parameters
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        radius = random.randint(5, 50)
        color = list(np.random.rand(3))  # Random RGB color
        color.append(random.uniform(0.05, 0.3)) # Random Alpha value
        color = tuple(color)

        # Create a circular mask for the drop
        for i in range(max(0, y - radius), min(height, y + radius + 1)):
            for j in range(max(0, x - radius), min(width, x + radius + 1)):
                distance = np.sqrt((i - y)**2 + (j - x)**2)
                if distance <= radius:
                   # Blend the drop color with the existing pixel color
                   alpha = color[3]
                   image[i, j] = (1 - alpha) * image[i, j] + alpha * np.array(color[:4])


    # Save the image using matplotlib
    plt.imshow(image)
    plt.axis('off')  # Hide axes
    plt.savefig('modulos_generados/arte_ciclo_4.png')


if __name__ == '__main__':
    generate_abstract_art()