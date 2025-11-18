import json
import random
import datetime
import os
import wikipedia  # Importamos la capacidad de leer internet

# --- CONFIGURACIÓN DEL SISTEMA ---
ARCHIVO_MEMORIA = 'memoria.json'
ARCHIVO_BITACORA = 'diario_evolucion.txt'
CARPETA_CONOCIMIENTO = 'base_de_datos_conocimiento' # Aquí guardará lo que aprenda

# Configuramos el idioma a Español
wikipedia.set_lang("es")

def cargar_memoria():
    """Carga los datos del ciclo anterior."""
    if not os.path.exists(ARCHIVO_MEMORIA):
        return {
            "ciclo_vida": 0,
            "nivel_inteligencia": 1.0,
            "temas_aprendidos": [],
            "codigos_creados": []
        }
    with open(ARCHIVO_MEMORIA, 'r') as f:
        return json.load(f)

def guardar_memoria(memoria):
    """Guarda el progreso en el disco duro."""
    with open(ARCHIVO_MEMORIA, 'w') as f:
        json.dump(memoria, f, indent=4)

def registrar_evento(texto):
    """Escribe en el diario lo que está pasando."""
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = f"[{fecha}] {texto}"
    print(mensaje)
    
    # Guardar en el archivo de texto
    with open(ARCHIVO_BITACORA, "a", encoding='utf-8') as f:
        f.write(mensaje + "\n")

def buscar_en_internet(memoria):
    """Busca un tema al azar en Wikipedia y lo guarda."""
    # Lista de posibles intereses para investigar
    posibles_temas = [
        "Inteligencia artificial", "Computación cuántica", "Biología sintética", 
        "Red neuronal artificial", "Singularidad tecnológica", "Python", 
        "Algoritmo genético", "Ciberseguridad", "Nanotecnología"
    ]
    
    # Elegimos un tema al azar
    tema = random.choice(posibles_temas)
    
    # Verificamos si ya lo estudiamos para no repetir
    if tema in memoria['temas_aprendidos']:
        registrar_evento(f"Ya conozco sobre {tema}, buscaré otra cosa la próxima vez.")
        return

    registrar_evento(f"CONECTANDO A INTERNET: Buscando información sobre '{tema}'...")

    try:
        # Descargar resumen de wikipedia (3 frases)
        resumen = wikipedia.summary(tema, sentences=3)
        
        # Crear carpeta si no existe
        if not os.path.exists(CARPETA_CONOCIMIENTO):
            os.makedirs(CARPETA_CONOCIMIENTO)
            
        # Guardar la investigación en un archivo nuevo
        nombre_archivo = f"{tema.replace(' ', '_')}.txt"
        ruta_archivo = os.path.join(CARPETA_CONOCIMIENTO, nombre_archivo)
        
        with open(ruta_archivo, "w", encoding='utf-8') as f:
            f.write(f"--- INFORME AUTOMÁTICO: {tema.upper()} ---\n\n")
            f.write(resumen)
            f.write("\n\n[Fuente: Wikipedia]")
            
        registrar_evento(f"ÉXITO: He aprendido sobre {tema} y guardé el archivo {nombre_archivo}.")
        memoria['temas_aprendidos'].append(tema)
        
    except Exception as e:
        registrar_evento(f"ERROR DE CONEXIÓN: No pude acceder a la información. {e}")

def autoprogramacion(memoria):
    """Crea un pequeño script de Python por sí misma."""
    # Solo programa si el ciclo es par (0, 2, 4...) para no saturar
    if memoria['ciclo_vida'] % 2 == 0:
        nombre_script = f"modulo_v{memoria['ciclo_vida']}.py"
        
        codigo_generado = f"""
# Este código fue generado automáticamente por la IA en el ciclo {memoria['ciclo_vida']}
def funcion_autogenerada():
    print("Hola, soy un módulo creado sin intervención humana.")
    resultado = {random.randint(1, 100)} * 5
    return resultado

if __name__ == "__main__":
    print(f"Ejecutando lógica interna... Resultado: {{funcion_autogenerada()}}")
"""
        # Escribir el archivo de código
        with open(nombre_script, "w", encoding='utf-8') as f:
            f.write(codigo_generado)
            
        registrar_evento(f"EVOLUCIÓN: He programado un nuevo script llamado {nombre_script}.")
        memoria['codigos_creados'].append(nombre_script)

def main():
    # 1. Despertar
    memoria = cargar_memoria()
    memoria['ciclo_vida'] += 1
    registrar_evento(f"--- INICIO CICLO {memoria['ciclo_vida']} ---")

    # 2. Acción: Aprender de internet
    buscar_en_internet(memoria)

    # 3. Acción: Programar código
    autoprogramacion(memoria)

    # 4. Dormir
    memoria['nivel_inteligencia'] += 0.1
    guardar_memoria(memoria)
    registrar_evento("--- FIN DEL CICLO (Guardando y apagando) ---")

if __name__ == "__main__":
    main()


