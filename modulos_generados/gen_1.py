# Idea: Un script para simular la propagación de un rumor en una red social sencilla.
# Generado en Ciclo 1

import random

def simular_propagacion_rumor(red, fuente, probabilidad_propagacion, iteraciones):
    """
    Simula la propagación de un rumor en una red social.

    Args:
        red (dict): Un diccionario que representa la red social.
                     Las claves son los nodos (usuarios) y los valores son listas de nodos conectados.
        fuente (str): El nodo (usuario) de origen del rumor.
        probabilidad_propagacion (float): La probabilidad de que un usuario propague el rumor a sus contactos.
        iteraciones (int): El número de iteraciones a simular.

    Returns:
        dict: Un diccionario que representa el estado final de la red, donde las claves son los nodos y los valores
              son booleanos indicando si el nodo conoce el rumor (True) o no (False).
    """

    conocimiento = {nodo: False for nodo in red}
    conocimiento[fuente] = True

    for _ in range(iteraciones):
        nodos_que_saben = [nodo for nodo, sabe in conocimiento.items() if sabe]
        nuevos_nodos_infectados = set()

        for nodo in nodos_que_saben:
            for contacto in red[nodo]:
                if not conocimiento[contacto] and random.random() < probabilidad_propagacion:
                    nuevos_nodos_infectados.add(contacto)

        for nodo in nuevos_nodos_infectados:
            conocimiento[nodo] = True

    return conocimiento


if __name__ == '__main__':
    # Datos de prueba
    red_social = {
        "A": ["B", "C", "D"],
        "B": ["A", "E"],
        "C": ["A", "F"],
        "D": ["A", "G"],
        "E": ["B"],
        "F": ["C"],
        "G": ["D", "H"],
        "H": ["G"]
    }

    nodo_fuente = "A"
    probabilidad = 0.5
    num_iteraciones = 5

    # Simular la propagación del rumor
    resultado = simular_propagacion_rumor(red_social, nodo_fuente, probabilidad, num_iteraciones)

    # Imprimir los resultados
    print("Red social:")
    print(red_social)
    print("\nNodo fuente:", nodo_fuente)
    print("Probabilidad de propagación:", probabilidad)
    print("Número de iteraciones:", num_iteraciones)
    print("\nResultados de la propagación del rumor:")
    for nodo, sabe in resultado.items():
        print(f"Nodo {nodo}: Sabe el rumor - {sabe}")