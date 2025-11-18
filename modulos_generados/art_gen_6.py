# ## Imagen Generativa Compleja para Python:  "Entrelazamiento Cósmico"

**Descripción General:**

Esta imagen generativa explorará la interconexión entre elementos cósmicos a través de patrones visuales intrincados y colores vibrantes. Se inspirará en nebulosas, galaxias en espiral y fenómenos cuánticos como el entrelazamiento, pero sin intentar replicar la realidad fotográficamente. La imagen final será abstracta y evocadora, sugiriendo movimiento, energía y la profunda complejidad del universo.

**Elementos Clave:**

* **Nebulosas Abstractas:**  En lugar de reproducir nebulosas reales, utilizaremos gradientes de color suaves y superpuestos para crear formas nebulosas abstractas.  Los colores primarios serán azul, violeta, magenta y naranja, con toques de amarillo y verde para acentos.  La densidad y transparencia de estas nebulosas variarán para dar profundidad y dimensionalidad.
* **Galaxias en Espiral Fractal:** Generaremos galaxias en espiral utilizando principios fractales, como la secuencia de Fibonacci o el conjunto de Mandelbrot, para crear brazos que se curvan y ramifican de forma natural.  Las galaxias serán más sutiles que las nebulosas, con un brillo suave y un núcleo brillante.
* **Líneas de Entrelazamiento Cuántico:** Conectaremos diferentes partes de la imagen (nebulosas y galaxias) con líneas delgadas y onduladas que representan el entrelazamiento cuántico. Estas líneas tendrán un color contrastante (por ejemplo, blanco brillante o cian) y un brillo suave (glow) para que destaquen.  La dirección y la curvatura de las líneas serán aleatorias, pero con una tendencia general a conectar áreas visualmente importantes.
* **Partículas Estelares:**  Esparciremos pequeñas partículas brillantes (como estrellas) por toda la imagen para agregar una sensación de profundidad y dinamismo.  El tamaño, el brillo y el color de las partículas variarán ligeramente de forma aleatoria.
* **Distorsión sutil y Ruido:** Aplicaremos una ligera distorsión general a la imagen, como un efecto de lente o una ligera vibración, para darle una sensación más orgánica y menos perfecta.  También agregaremos un ruido sutil para romper la uniformidad y simular las fluctuaciones del espacio.

**Python y Librerías:**

* **`Pillow (PIL)`:** Para la creación y manipulación de imágenes.
* **`NumPy`:** Para cálculos matemáticos, generación de números aleatorios y manipulación de arrays (útil para datos de píxeles).
* **`random`:** Para generación de números aleatorios utilizados en varios parámetros (color, posición, tamaño, etc.).
* **`math`:** Para funciones matemáticas como seno, coseno y exponentes, que pueden ser útiles para crear patrones curvos y fractales.
* **`colormaps (matplotlib)`:** (Opcional) Permite usar paletas de colores predefinidas de matplotlib para facilitar la creación de gradientes.

**Posibles Pasos del Código:**

1. **Creación de la Lienzo:** Crear una imagen en blanco utilizando Pillow con las dimensiones deseadas.
2. **Generación de Nebulosas:**
    *   Crear múltiples capas de ruido utilizando NumPy.
    *   Aplicar gradientes de color a cada capa.
    *   Superponer las capas con diferentes niveles de transparencia.
    *   Usar filtros de desenfoque (GaussianBlur) para suavizar los bordes.
3. **Generación de Galaxias:**
    *   Implementar una función que genere una galaxia en espiral fractal utilizando la secuencia de Fibonacci o el conjunto de Mandelbrot.
    *   Dibujar varias galaxias en diferentes posiciones y tamaños.
    *   Añadir un brillo suave al núcleo de cada galaxia.
4. **Creación de Líneas de Entrelazamiento:**
    *   Generar puntos de anclaje aleatorios en la imagen.
    *   Conectar los puntos de anclaje con curvas suaves (splines) utilizando funciones como `scipy.interpolate.splprep` (opcional, pero mejora la suavidad).
    *   Aplicar un brillo (glow) a las líneas.
5. **Dispersión de Partículas Estelares:**
    *   Generar un gran número de puntos aleatorios en la imagen.
    *   Dibujar pequeños círculos o cuadrados en cada punto, con variaciones aleatorias en tamaño, brillo y color.
6. **Aplicación de Distorsión y Ruido:**
    *   Implementar una función que distorsione los píxeles de la imagen de forma sutil.
    *   Generar una capa de ruido y superponerla a la imagen con una transparencia muy baja.
7. **Guardar la Imagen:** Guardar la imagen generada en formato PNG o JPG.

**Complejidad y Personalización:**

La complejidad de esta imagen generativa puede variar significativamente.  Se puede comenzar con una implementación básica y luego ir agregando complejidad gradualmente.  Algunas áreas donde se puede experimentar y personalizar:

*   **Fractales:** Explorar diferentes tipos de fractales para las galaxias.
*   **Paletas de Colores:** Experimentar con diferentes paletas de colores para las nebulosas y las partículas.
*   **Algoritmos de Ruido:** Investigar diferentes algoritmos de ruido, como Perlin Noise o Simplex Noise.
*   **Efectos de Iluminación:** Añadir efectos de iluminación más complejos, como halos o destellos.
*   **Interacción del Usuario:** Crear una interfaz que permita al usuario ajustar parámetros como la densidad de las nebulosas, el número de galaxias o la intensidad de las líneas de entrelazamiento.

**Ejemplo de Código Fragmentado (Pseudocódigo):**

```python
import PIL.Image
import PIL.ImageDraw
import numpy as np
import random

# Configuración
ancho = 1024
alto = 1024
imagen = PIL.Image.new("RGB", (ancho, alto), "black")
dibujo = PIL.ImageDraw.Draw(imagen)

# Función para crear un gradiente
def crear_gradiente(ancho, alto, color1, color2):
  # ... (Implementación del gradiente) ...
  return gradiente

# Generar nebulosas
for i in range(3):  # Crear varias nebulosas
  gradiente = crear_gradiente(ancho, alto, (random.randint(0,255),random.randint(0,255),random.randint(0,255)),(random.randint(0,255),random.randint(0,255),random.randint(0,255))  )
  # ... (Posicionar, escalar y rotar el gradiente) ...
  imagen.paste(gradiente, (0,0), gradiente) # La máscara (tercer argumento) es crucial para la transparencia

# Generar galaxias (ejemplo simplificado)
def dibujar_galaxia(x, y, tamaño, brillo):
  # ... (Implementar un patrón en espiral simple) ...
  dibujo.ellipse((x - tamaño, y - tamaño, x + tamaño, y + tamaño), fill=(brillo, brillo, brillo))

for i in range(5):
  dibujar_galaxia(random.randint(0, ancho), random.randint(0, alto), random.randint(20, 50), random.randint(100, 200))

# Generar lineas de entrelazamiento
for _ in range(10):
  x1 = random.randint(0, ancho)
  y1 = random.randint(0, alto)
  x2 = random.randint(0, ancho)
  y2 = random.randint(0, alto)
  dibujo.line((x1, y1, x2, y2), fill="cyan", width=2) # Simplemente dibujar lineas, mejorar con curvas

# Generar partículas estelares
for i in range(1000):
  x = random.randint(0, ancho)
  y = random.randint(0, alto)
  brillo = random.randint(50, 255)
  dibujo.point((x, y), fill=(brillo, brillo, brillo))

# Guardar la imagen
imagen.save("entrelazamiento_cosmico.png")
```

Este es un pseudocódigo para ilustrar los pasos.  La implementación real requerirá una cantidad considerable de código, especialmente para generar las nebulosas y galaxias complejas.  El objetivo principal es crear una imagen que evoque la inmensidad y la belleza del universo a través de formas abstractas y colores vibrantes.
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFilter
import numpy as np
import random
import math

# Configuración
ancho = 1024
alto = 1024
imagen = PIL.Image.new("RGB", (ancho, alto), "black")
dibujo = PIL.ImageDraw.Draw(imagen)

# Función para crear un gradiente radial
def crear_gradiente_radial(ancho, alto, color1, color2, center_x, center_y, radius):
    gradiente = PIL.Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    dibujo_gradiente = PIL.ImageDraw.Draw(gradiente)
    for x in range(ancho):
        for y in range(alto):
            distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            if distance <= radius:
                intensity = 1 - distance / radius
                r = int(color1[0] * intensity + color2[0] * (1 - intensity))
                g = int(color1[1] * intensity + color2[1] * (1 - intensity))
                b = int(color1[2] * intensity + color2[2] * (1 - intensity))
                a = int(255 * intensity) # Transparencia
                dibujo_gradiente.point((x, y), fill=(r, g, b, a))
    return gradiente

# Función para generar ruido
def generar_ruido(ancho, alto):
    return np.random.rand(alto, ancho)

# Generar nebulosas
for i in range(5):  # Crear varias nebulosas
    color1 = (random.randint(50, 200), random.randint(0, 150), random.randint(50, 255))
    color2 = (random.randint(100, 255), random.randint(0, 100), random.randint(100, 255))
    center_x = random.randint(0, ancho)
    center_y = random.randint(0, alto)
    radius = random.randint(100, 400)

    gradiente = crear_gradiente_radial(ancho, alto, color1, color2, center_x, center_y, radius)
    gradiente = gradiente.filter(PIL.ImageFilter.GaussianBlur(radius=15)) # Smooth it

    # Crear una capa de ruido y multiplicar por el gradiente para hacerlo mas irregular.
    ruido = generar_ruido(ancho, alto)
    ruido_image = PIL.Image.fromarray((ruido * 255).astype('uint8')).convert('L')
    ruido_image = ruido_image.resize((ancho, alto), PIL.Image.Resampling.LANCZOS) # Ensure same size as the gradient.
    ruido_mask = PIL.Image.new("L", (ancho, alto))
    ruido_mask.paste(ruido_image)

    imagen.paste(gradiente, (0,0), gradiente) # Usar la imagen de gradiente como mascara de transparencia

# Generar galaxias (ejemplo simplificado - espiral)
def dibujar_galaxia(x, y, tamaño, brillo):
  for i in range(tamaño):
    angle = i * 0.5
    dx = int(i * math.cos(angle))
    dy = int(i * math.sin(angle))
    brightness = max(0, min(255, brillo - i*2))
    dibujo.point((x + dx, y + dy), fill=(brightness, brightness, brightness))
    dibujo.point((x - dx, y - dy), fill=(brightness, brightness, brightness))


for i in range(3):
  x = random.randint(0, ancho)
  y = random.randint(0, alto)
  tamaño = random.randint(20, 70)
  brillo = random.randint(150, 255)
  dibujar_galaxia(x, y, tamaño, brillo)


# Generar lineas de entrelazamiento
for _ in range(15):
  x1 = random.randint(0, ancho)
  y1 = random.randint(0, alto)
  x2 = random.randint(0, ancho)
  y2 = random.randint(0, alto)
  # Dibujar una curva Bézier (implementación sencilla usando líneas)
  num_segments = 10
  for i in range(num_segments):
    t = i / num_segments
    x = int((1 - t)**3 * x1 + 3 * (1 - t)**2 * t * random.randint(x1 -50 , x1+50) + 3 * (1 - t) * t**2 * random.randint(x2-50, x2 +50) + t**3 * x2)
    y = int((1 - t)**3 * y1 + 3 * (1 - t)**2 * t * random.randint(y1-50, y1 + 50) + 3 * (1 - t) * t**2 * random.randint(y2 - 50, y2+50) + t**3 * y2)
    dibujo.line((x,y, x2, y2) , fill="cyan", width=1) # Dibuja lineas que convergen a los puntos.

# Generar partículas estelares
for i in range(2000):
  x = random.randint(0, ancho)
  y = random.randint(0, alto)
  brillo = random.randint(50, 255)
  tamaño = random.randint(1,3)
  dibujo.ellipse((x-tamaño, y-tamaño, x+tamaño, y+tamaño), fill=(brillo, brillo, brillo))

# Aplicar distorsión sutil (onda)
def distorsionar_imagen(imagen, intensidad=2):
  pixeles = imagen.load()
  for x in range(imagen.size[0]):
    for y in range(imagen.size[1]):
      offset_x = int(math.sin(y * 0.02) * intensidad)
      offset_y = int(math.cos(x * 0.02) * intensidad)
      new_x = x + offset_x
      new_y = y + offset_y

      if 0 <= new_x < imagen.size[0] and 0 <= new_y < imagen.size[1]:
        pixeles[x, y] = pixeles[new_x, new_y] # Mover el pixel



distorsionar_imagen(imagen)


# Aplicar ruido general
ruido = generar_ruido(ancho, alto)
ruido_image = PIL.Image.fromarray((ruido * 20).astype('uint8')).convert('L')
imagen = PIL.Image.blend(imagen.convert('RGB'), ruido_image.convert('RGB'), alpha=0.99)


# Guardar la imagen
imagen.save("modulos_generados/arte_6.png")