# Vale, aquí tienes una descripción de imagen para generar, pensada para ser visualmente interesante y posiblemente evocar una sensación específica:

**Descripción de la Imagen:**

**Tema:** Un Jardín Botánico Etéreo y Surrealista

**Elementos Clave:**

*   **Entorno:** Un jardín botánico decadente pero bello, con estructuras victorianas de vidrio y hierro parcialmente cubiertas de enredaderas y musgo. La iluminación es suave y difusa, casi como si estuviera bajo el agua o en una nube.
*   **Vegetación:** Plantas exóticas y bioluminiscentes que no existen en la realidad. Imaginemos orquídeas que emiten un suave resplandor azul, helechos con hojas translúcidas y flores que levitan ligeramente del suelo. Algunas plantas parecen estar en estado de floración exuberante, mientras que otras se marchitan elegantemente, creando un contraste de vida y muerte.
*   **Criaturas:** Presencia sutil de pequeñas criaturas fantásticas. Mariposas con alas iridiscentes, colibríes con plumas hechas de cristal o incluso pequeños espíritus de la naturaleza translúcidos que interactúan con las plantas. No deben ser el foco principal, sino sutiles detalles que añaden magia.
*   **Atmosfera:** Niebla ligera que se arremolina alrededor de las estructuras y las plantas, creando una sensación de misterio y ensueño. Gotas de rocío brillantes que cuelgan de las hojas.
*   **Paleta de Colores:** Predominantemente tonos fríos como verdes esmeralda, azules aguamarina, púrpuras lavanda y grises suaves. Acentos de colores cálidos como dorado pálido o rosa fucsia en las plantas bioluminiscentes.
*   **Perspectiva:** Un ángulo de visión ligeramente elevado, como si el espectador estuviera observando el jardín desde una plataforma oculta o un balcón distante. Esto ayuda a abarcar la escala del jardín y su atmósfera.
*   **Estilo Artístico:**  Punto medio entre fotorrealismo y arte conceptual. Detalle suficiente para que sea visualmente atractivo, pero con una cualidad etérea y onírica que lo distinga de una fotografía ordinaria. Se puede inspirar en la obra de artistas como Alphonse Mucha o algunos paisajistas románticos, pero con un toque de ciencia ficción.

**Notas Adicionales para IA (opcional):**

*   **Keywords:** surrealismo, jardín botánico, bioluminiscencia, fantasía, etéreo, niebla, decadencia, victorianismo, criaturas fantásticas, luz suave, Alphonse Mucha.
*   **Enfatizar:** La atmósfera misteriosa y onírica, el contraste entre vida y muerte, la belleza de la decadencia.

**El objetivo es crear una imagen que invite a la contemplación y la imaginación, transportando al espectador a un mundo de fantasía botánica.**

¿Qué te parece?  ¿Quieres que refinemos algún aspecto? Por ejemplo, podríamos enfocarnos en un tipo específico de criatura o en un estilo artístico diferente.
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as pe

# Configuración inicial
plt.figure(figsize=(12, 8), facecolor='black')
ax = plt.axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Paleta de colores
verde_esmeralda = '#287233'
azul_aguamarina = '#70db93'
purpura_lavanda = '#e6e6fa'
gris_suave = '#a9a9a9'
dorado_palido = '#eee8aa'
rosa_fucsia = '#ff69b4'

# Función para crear una planta bioluminiscente (orquídea)
def crear_orquidea(x, y, escala=1.0, color_base=azul_aguamarina, color_brillo=rosa_fucsia):
    num_petalos = 5
    for i in range(num_petalos):
        angulo = 2 * np.pi * i / num_petalos
        x_petalo = x + escala * 0.05 * np.cos(angulo)
        y_petalo = y + escala * 0.05 * np.sin(angulo)
        petalo = plt.Circle((x_petalo, y_petalo), escala * 0.03, color=color_base, ec=color_brillo, lw=1.5, alpha=0.8, zorder=2)
        ax.add_patch(petalo)

    # Centro brillante
    centro = plt.Circle((x, y), escala * 0.02, color=color_brillo, alpha=0.9, zorder=3)
    ax.add_patch(centro)

# Función para crear helechos translúcidos
def crear_helecho(x, y, altura=0.1, ancho=0.02, angulo=0, color=verde_esmeralda, alpha=0.6):
    num_hojas = 7
    for i in range(num_hojas):
        offset = i * ancho / (num_hojas - 1) - ancho / 2
        x_hoja = x + offset * np.cos(np.radians(angulo + 90))
        y_hoja = y + offset * np.sin(np.radians(angulo + 90))
        dx = altura * 0.8
        dy = 0
        ax.arrow(x_hoja, y_hoja, dx, dy, width=0.001, head_width=0.005, head_length=0.01, fc=color, ec=color, alpha=alpha, zorder=1)
        
#Función para crear enredadera en estructura
def crear_enredadera(x,y, largo = 0.2, num_hojas = 10, color = verde_esmeralda):
    for i in range(num_hojas):
        offset = largo * i / num_hojas
        x_hoja = x
        y_hoja = y - offset
        dx = 0.01
        dy = 0.01
        ax.arrow(x_hoja, y_hoja, dx, dy, width = 0.0005, head_width = 0.002, head_length = 0.004, fc = color, ec = color, alpha = 0.5)

# Estructuras (simples para este ejemplo)
ax.add_patch(plt.Rectangle((0.1, 0.1), 0.2, 0.5, color=gris_suave, alpha=0.3))
ax.add_patch(plt.Rectangle((0.7, 0.2), 0.15, 0.4, color=gris_suave, alpha=0.3))

#Enredaderas en estructura
crear_enredadera(0.1, 0.6, largo = 0.4)
crear_enredadera(0.7, 0.6, largo = 0.3)

# Vegetación principal
crear_orquidea(0.3, 0.2, escala=1.2)
crear_orquidea(0.75, 0.3, escala=0.8, color_base=purpura_lavanda, color_brillo=dorado_palido)
crear_helecho(0.2, 0.7, altura=0.15, ancho=0.03, angulo=20)
crear_helecho(0.8, 0.8, altura=0.1, ancho=0.02, angulo=-10, color = '#3cb371')
crear_orquidea(0.5,0.5, escala = 0.6, color_base = '#87ceeb', color_brillo = '#dda0dd')


# Niebla (simulación con círculos transparentes)
num_circulos_niebla = 50
for _ in range(num_circulos_niebla):
    x_niebla = np.random.uniform(0, 1)
    y_niebla = np.random.uniform(0, 1)
    radio_niebla = np.random.uniform(0.01, 0.05)
    alpha_niebla = np.random.uniform(0.05, 0.15)
    niebla = plt.Circle((x_niebla, y_niebla), radio_niebla, color=gris_suave, alpha=alpha_niebla, zorder=0)
    ax.add_patch(niebla)

# Mariposas (simples, solo puntos con color)
num_mariposas = 15
for _ in range(num_mariposas):
    x_mariposa = np.random.uniform(0, 1)
    y_mariposa = np.random.uniform(0, 1)
    color_mariposa = np.random.choice([dorado_palido, rosa_fucsia])
    ax.plot(x_mariposa, y_mariposa, marker='o', markersize=2, color=color_mariposa, alpha=0.7, zorder=4)

# Guardar la imagen
plt.savefig('modulos_generados/arte_7.png', facecolor=fig.get_facecolor())
plt.close()