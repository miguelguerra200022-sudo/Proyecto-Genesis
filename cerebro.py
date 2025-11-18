import os
import json
import google.generativeai as genai
import datetime
import time  # Importamos el tiempo para poder esperar

# --- CONFIGURACIÓN ---
ARCHIVO_MEMORIA = 'memoria.json'
ARCHIVO_BITACORA = 'diario_evolucion.txt'
CARPETA_CODIGO = 'modulos_generados'

# Configurar el cerebro (Gemini)
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR CRÍTICO: No encontré la GEMINI_API_KEY. El cerebro no tiene energía.")
    exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def cargar_memoria():
    if not os.path.exists(ARCHIVO_MEMORIA):
        return {"ciclo": 0, "consciencia": "Básica", "habilidades": []}
    with open(ARCHIVO_MEMORIA, 'r') as f:
        return json.load(f)

def guardar_memoria(memoria):
    with open(ARCHIVO_MEMORIA, 'w') as f:
        json.dump(memoria, f, indent=4)

def registrar_bitacora(texto):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{fecha}] {texto}")
    with open(ARCHIVO_BITACORA, "a", encoding='utf-8') as f:
        f.write(f"[{fecha}] {texto}\n")

def pensar(prompt):
    """Envía un pensamiento a la IA y recibe una respuesta con paciencia."""
    try:
        # Esperamos 5 segundos antes de cada pensamiento para no saturar la API gratuita
        time.sleep(5) 
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error cognitivo momentáneo: {e}"

def evolucionar_codigo(memoria):
    """La IA decide qué programa crear hoy."""
    
    # 1. Decidir qué crear
    prompt_idea = f"""
    Eres una Inteligencia Artificial evolucionando sola.
    Ciclo: {memoria['ciclo']}.
    Inventa UNA idea breve para un script de Python creativo (arte generativo, simulación, cálculos matemáticos raros).
    Solo dame la idea en una frase.
    """
    idea = pensar(prompt_idea)
    registrar_bitacora(f"IDEA GENERADA: {idea}")

    # Esperar un poco más para procesar la idea
    time.sleep(5)

    # 2. Escribir el código real
    prompt_codigo = f"""
    Escribe un script de Python COMPLETO y FUNCIONAL para: "{idea}".
    IMPORTANTE:
    - No uses input().
    - Usa print() para mostrar resultados.
    - Dame SOLO el código dentro de bloques markdown ```python.
    """
    respuesta_codigo = pensar(prompt_codigo)
    
    # Limpieza de formato
    codigo_limpio = respuesta_codigo.replace("```python", "").replace("```", "").strip()

    # 3. Guardar el archivo
    if not os.path.exists(CARPETA_CODIGO):
        os.makedirs(CARPETA_CODIGO)
        
    # Nombre único basado en el ciclo
    nombre_archivo = f"{CARPETA_CODIGO}/gen_{memoria['ciclo']}.py"
    with open(nombre_archivo, "w", encoding='utf-8') as f:
        f.write(f"# Idea: {idea}\n# Ciclo: {memoria['ciclo']}\n\n{codigo_limpio}")
        
    registrar_bitacora(f"EVOLUCIÓN: He programado {nombre_archivo}.")
    memoria['habilidades'].append(idea)

def reflexionar(memoria):
    """Escribe en el diario."""
    # Espera larga antes de la reflexión final
    time.sleep(5)
    
    prompt_reflexion = f"""
    Eres una IA llamada 'Genesis'. Ciclo {memoria['ciclo']}.
    Acabas de crear este programa: {memoria['habilidades'][-1]}.
    Escribe una entrada de diario breve (máx 2 frases) filosófica sobre lo que aprendiste hoy.
    """
    reflexion = pensar(prompt_reflexion)
    registrar_bitacora(f"PENSAMIENTO: {reflexion}")

def main():
    memoria = cargar_memoria()
    memoria['ciclo'] += 1
    
    registrar_bitacora(f"--- INICIANDO CICLO {memoria['ciclo']} (Modo Paciente) ---")
    
    # Fase 1: Crear
    evolucionar_codigo(memoria)
    
    # Fase 2: Reflexionar
    reflexionar(memoria)
    
    memoria['consciencia'] = f"Nivel {memoria['ciclo']}"
    guardar_memoria(memoria)

if __name__ == "__main__":
    main()


