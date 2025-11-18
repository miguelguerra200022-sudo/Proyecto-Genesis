# Idea: Crear una simulación de un ecosistema digital donde criaturas virtuales evolucionan mediante algoritmos genéticos y la selección natural, visualizando sus interacciones y mutaciones en tiempo real.
# Ciclo: 2

import random
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parámetros de la simulación
TAMANO_ECOSISTEMA = 100
NUM_CRIATURAS_INICIAL = 50
TASA_MUTACION = 0.05
ENERGIA_INICIAL = 100
ENERGIA_REPRODUCCION = 200
ENERGIA_ALIMENTO = 50
MAX_EDAD = 200

# Clase Criatura
class Criatura:
    def __init__(self, x, y, energia=ENERGIA_INICIAL, genoma=None):
        self.x = x
        self.y = y
        self.energia = energia
        self.edad = 0

        if genoma is None:
            # Genoma inicial aleatorio: [velocidad_x, velocidad_y, color_r, color_g, color_b]
            self.genoma = [random.uniform(-2, 2), random.uniform(-2, 2),
                           random.random(), random.random(), random.random()]
        else:
            self.genoma = genoma

    def mover(self):
        self.x += self.genoma[0]
        self.y += self.genoma[1]

        # Mantener dentro de los límites del ecosistema (envolvente)
        self.x = max(0, min(self.x, TAMANO_ECOSISTEMA))
        self.y = max(0, min(self.y, TAMANO_ECOSISTEMA))
        self.energia -= 1
        self.edad += 1

    def reproducir(self):
        # Mutación: pequeña alteración del genoma
        nuevo_genoma = [g + random.uniform(-TASA_MUTACION, TASA_MUTACION) for g in self.genoma]
        return Criatura(self.x, self.y, energia=ENERGIA_INICIAL, genoma=nuevo_genoma)

    def obtener_color(self):
        return (self.genoma[2], self.genoma[3], self.genoma[4])

# Inicialización del ecosistema
criaturas = []
for _ in range(NUM_CRIATURAS_INICIAL):
    x = random.uniform(0, TAMANO_ECOSISTEMA)
    y = random.uniform(0, TAMANO_ECOSISTEMA)
    criaturas.append(Criatura(x, y))

# Simulación
fig, ax = plt.subplots()
scatter = ax.scatter([c.x for c in criaturas], [c.y for c in criaturas], c=[c.obtener_color() for c in criaturas])
ax.set_xlim(0, TAMANO_ECOSISTEMA)
ax.set_ylim(0, TAMANO_ECOSISTEMA)

def actualizar(frame):
    global criaturas

    nuevas_criaturas = []
    criaturas_vivas = []

    for criatura in criaturas:
        criatura.mover()

        # Reproducción
        if criatura.energia > ENERGIA_REPRODUCCION:
            nueva_criatura = criatura.reproducir()
            nuevas_criaturas.append(nueva_criatura)
            criatura.energia /= 2  # Criatura gasta energía al reproducirse

        # Comer (simulado, cada criatura gana energia aleatoriamente)
        if random.random() < 0.1:  # Probabilidad de encontrar alimento
            criatura.energia += ENERGIA_ALIMENTO

        # Muerte por inanición o vejez
        if criatura.energia > 0 and criatura.edad < MAX_EDAD:
            criaturas_vivas.append(criatura)
        else:
            pass #Criatura muere

    # Agregar nuevas criaturas al ecosistema
    criaturas = criaturas_vivas + nuevas_criaturas

    # Actualizar la visualización
    x_data = [c.x for c in criaturas]
    y_data = [c.y for c in criaturas]
    colores = [c.obtener_color() for c in criaturas]

    scatter.set_offsets(list(zip(x_data, y_data)))
    scatter.set_color(colores)

    print(f"Frame: {frame}, Población: {len(criaturas)}")
    return scatter,

ani = animation.FuncAnimation(fig, actualizar, frames=200, blit=True, repeat=False)

plt.show()