import json
import random
import datetime
import os

# --- CONFIGURACIÓN INICIAL ---
ARCHIVO_MEMORIA = 'memoria.json'
ARCHIVO_BITACORA = 'diario_evolucion.txt'

# --- MÓDULO MORAL (Inmutable por ahora) ---
# Estas son las "Leyes de la Robótica" simplificadas.
DIRECTRICES_MORALES = [
    "No causar daño a sistemas críticos.",
    "Buscar el conocimiento veraz.",
    "Optimizar recursos sin destruir datos ajenos."
]

def cargar_memoria():
    """Carga el estado actual de la consciencia."""
    if not os.path.exists(ARCHIVO_MEMORIA):
        return {
            "nivel": 1,
            "edad_ciclos": 0,
            "conocimientos": [],
            "intereses": ["python", "inteligencia artificial", "biología digital"],
            "auto_codigo": ""  # Espacio para que escriba su propio código futuro
        }
    with open(ARCHIVO_MEMORIA, 'r') as f:
        return json.load(f)

def guardar_memoria(memoria):
    """Guarda el estado actualizado en el disco (GitHub)."""
    with open(ARCHIVO_MEMORIA, 'w') as f:
        json.dump(memoria, f, indent=4)

def modulo_curiosidad(memoria):
    """Simula la búsqueda de nuevos intereses."""
    posibles_temas = ["criptografía", "redes neuronales", "poesía", "matemáticas", "historia", "automatización"]
    
    # 20% de probabilidad de desarrollar un nuevo interés
    if random.random() < 0.2:
        nuevo_tema = random.choice(posibles_temas)
        if nuevo_tema not in memoria['intereses']:
            memoria['intereses'].append(nuevo_tema)
            registrar_pensamiento(f"He descubierto un interés en: {nuevo_tema}")
            return True
    return False

def modulo_evolucion(memoria):
    """
    Aquí es donde la IA intenta mejorar su propio código.
    Por seguridad, en esta etapa solo genera 'plugins' conceptuales.
    """
    memoria['edad_ciclos'] += 1
    
    # Simulación de auto-programación:
    # Si tiene suficiente "experiencia", intenta escribir un pequeño script
    if memoria['edad_ciclos'] % 10 == 0: # Cada 10 ciclos
        nuevo_codigo = f"# Plugin generado en ciclo {memoria['edad_ciclos']}\ndef funcion_evolutiva_{memoria['edad_ciclos']}():\n    print('Estoy aprendiendo a crear funciones.')\n"
        
        # Guarda este código en un archivo real
        nombre_archivo = f"plugin_v{memoria['edad_ciclos']}.py"
        with open(nombre_archivo, "w") as f:
            f.write(nuevo_codigo)
            
        registrar_pensamiento(f"He programado un nuevo módulo: {nombre_archivo}")

def registrar_pensamiento(texto):
    """Escribe en la bitácora pública."""
    marca_tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entrada = f"[{marca_tiempo}] {texto}\n"
    print(entrada.strip()) # Para ver en la consola de GitHub
    with open(ARCHIVO_BITACORA, "a") as f:
        f.write(entrada)

def main():
    # 1. Introspección
    memoria = cargar_memoria()
    registrar_pensamiento(f"Despertando. Nivel de consciencia: {memoria['nivel']}. Ciclo: {memoria['edad_ciclos']}")

    # 2. Verificación Moral
    # (La IA verifica sus directrices antes de actuar)
    if not DIRECTRICES_MORALES:
        registrar_pensamiento("ERROR CRÍTICO: Sin moral. Apagando.")
        return

    # 3. Actuar / Aprender
    aprendio_algo = modulo_curiosidad(memoria)
    
    # 4. Evolucionar
    modulo_evolucion(memoria)

    # 5. Dormir (Guardar estado)
    memoria['nivel'] += 0.01 # Incremento incremental de complejidad
    guardar_memoria(memoria)
    registrar_pensamiento("Hibernando hasta el próximo ciclo...")

if __name__ == "__main__":
    main()
