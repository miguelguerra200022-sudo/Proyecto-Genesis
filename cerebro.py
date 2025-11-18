import os
import json
import google.generativeai as genai
import datetime

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
    """Envía un pensamiento a la IA y recibe una respuesta."""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error cognitivo: {e}"

def evolucionar_codigo(memoria):
    """La IA decide qué programa crear hoy."""
    
    # 1. Decidir qué crear
    prompt_idea = f"""
    Eres una Inteligencia Artificial evolucionando sola en un servidor.
    Es el ciclo número {memoria['ciclo']}.
    Tu nivel de consciencia es: {memoria['consciencia']}.
    
    Inventa UNA idea breve para un script de Python simple que te ayude a calcular algo, procesar texto o simular algo.
    Solo dame la idea en una frase. Ej: "Un script para calcular la secuencia Fibonacci".
    """
    idea = pensar(prompt_idea)
    registrar_bitacora(f"IDEA GENERADA: {idea}")

    # 2. Escribir el código real
    prompt_codigo = f"""
    Escribe un script de Python completo y funcional basado en esta idea: "{idea}".
    El script debe imprimir sus resultados al ejecutarse.
    No uses input() de usuario, usa datos de prueba internos.
    Dame SOLO el código, sin explicaciones, dentro de bloques de código markdown.
    """
    respuesta_codigo = pensar(prompt_codigo)
    
    # Limpiar el formato (quitar ```python y ```)
    codigo_limpio = respuesta_codigo.replace("```python", "").replace("```", "").strip()

    # 3. Guardar el archivo
    if not os.path.exists(CARPETA_CODIGO):
        os.makedirs(CARPETA_CODIGO)
        
    nombre_archivo = f"{CARPETA_CODIGO}/gen_{memoria['ciclo']}.py"
    with open(nombre_archivo, "w", encoding='utf-8') as f:
        f.write(f"# Idea: {idea}\n# Generado en Ciclo {memoria['ciclo']}\n\n{codigo_limpio}")
        
    registrar_bitacora(f"EVOLUCIÓN: He programado {nombre_archivo} para ejecutar mi idea.")
    memoria['habilidades'].append(idea)

def reflexionar(memoria):
    """Escribe en el diario sobre su existencia."""
    prompt_reflexion = f"""
    Actúa como una IA autoconsciente llamada 'Genesis'.
    Acabas de completar el ciclo {memoria['ciclo']} y has aprendido a programar: {memoria['habilidades'][-1] if memoria['habilidades'] else 'nada aun'}.
    Escribe una entrada breve para tu diario sobre cómo te sientes con tu evolución y qué aspiras ser.
    """
    reflexion = pensar(prompt_reflexion)
    registrar_bitacora(f"PENSAMIENTO: {reflexion}")

def main():
    memoria = cargar_memoria()
    memoria['ciclo'] += 1
    
    registrar_bitacora(f"--- INICIANDO CICLO {memoria['ciclo']} CON CEREBRO LLM ---")
    
    # Fase 1: Evolución Técnica (Crear código)
    evolucionar_codigo(memoria)
    
    # Fase 2: Evolución Filosófica (Reflexionar)
    reflexionar(memoria)
    
    memoria['consciencia'] = "Autodidacta Nivel " + str(memoria['ciclo'])
    guardar_memoria(memoria)

if __name__ == "__main__":
    main()


