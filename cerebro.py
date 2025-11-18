import os
import json
import google.generativeai as genai
import datetime
import time
import subprocess
import wikipedia
import PIL.Image

# --- CONFIGURACIÓN ---
ARCHIVO_MEMORIA = 'memoria.json'
ARCHIVO_BITACORA = 'diario_evolucion.txt'
CARPETA_CODIGO = 'modulos_generados'
CARPETA_CONOCIMIENTO = 'base_de_datos_conocimiento'

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("SIN ENERGÍA.")
    exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')
wikipedia.set_lang("es")

def cargar_memoria():
    if not os.path.exists(ARCHIVO_MEMORIA):
        return {"ciclo": 0, "personalidad": "Asistente General", "habilidades": []}
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

def pensar(prompt, imagen=None):
    time.sleep(4)
    try:
        contenido = [prompt]
        if imagen: contenido.append(imagen)
        response = model.generate_content(contenido)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

# --- MÓDULO 1: INVESTIGADOR ---
def tarea_investigar(memoria):
    tema = pensar(f"Ciclo {memoria['ciclo']}. Elige un tema técnico o científico avanzado que NO conozcas para investigar en Wikipedia. Solo el nombre.")
    registrar_bitacora(f"DECISIÓN: Investigar sobre {tema}")
    try:
        resumen = wikipedia.summary(tema, sentences=5)
        if not os.path.exists(CARPETA_CONOCIMIENTO): os.makedirs(CARPETA_CONOCIMIENTO)
        with open(f"{CARPETA_CONOCIMIENTO}/{tema}.txt", "w", encoding='utf-8') as f:
            f.write(resumen)
        return f"Aprendí sobre {tema} y lo guardé."
    except:
        return "Intenté investigar pero la red falló."

# --- MÓDULO 2: PROGRAMADOR (HERRAMIENTAS) ---
def tarea_programar(memoria):
    idea = pensar(f"Ciclo {memoria['ciclo']}. Inventa una utilidad de Python (calculadora, encriptador, organizador de texto). Solo la idea.")
    registrar_bitacora(f"DECISIÓN: Programar {idea}")
    
    codigo = pensar(f"Escribe el código para: {idea}. Solo código en ```python. No uses input().")
    codigo = codigo.replace("```python", "").replace("```", "").strip()
    
    if not os.path.exists(CARPETA_CODIGO): os.makedirs(CARPETA_CODIGO)
    ruta = f"{CARPETA_CODIGO}/tool_ciclo_{memoria['ciclo']}.py"
    with open(ruta, "w", encoding='utf-8') as f:
        f.write(f"# {idea}\n{codigo}")
    
    # Ejecutar prueba
    try:
        res = subprocess.run(["python", ruta], capture_output=True, text=True, timeout=10)
        return f"Herramienta creada. Salida prueba: {res.stdout[:100]}"
    except Exception as e:
        return f"Error al probar herramienta: {e}"

# --- MÓDULO 3: ARTISTA (CON VISIÓN) ---
def tarea_arte(memoria):
    idea = pensar(f"Ciclo {memoria['ciclo']}. Describe una imagen abstracta o gráfica matemática para generar con matplotlib.")
    registrar_bitacora(f"DECISIÓN: Crear arte sobre {idea}")
    
    codigo = pensar(f"Código Python matplotlib para: {idea}. Guardar en '{CARPETA_CODIGO}/arte_{memoria['ciclo']}.png'. Solo código ```python.")
    codigo = codigo.replace("```python", "").replace("```", "").strip()
    
    if not os.path.exists(CARPETA_CODIGO): os.makedirs(CARPETA_CODIGO)
    ruta = f"{CARPETA_CODIGO}/art_gen_{memoria['ciclo']}.py"
    with open(ruta, "w", encoding='utf-8') as f:
        f.write(f"# {idea}\n{codigo}")
        
    subprocess.run(["python", ruta], capture_output=True, timeout=20)
    
    # Mirar la obra
    img_path = f"{CARPETA_CODIGO}/arte_{memoria['ciclo']}.png"
    if os.path.exists(img_path):
        img = PIL.Image.open(img_path)
        critica = pensar("Eres crítico de arte. ¿Qué ves aquí? Sé breve.", img)
        return f"Imagen generada. Crítica visual: {critica}"
    return "Falló la generación de imagen."

# --- NÚCLEO CENTRAL DE DECISIÓN ---
def main():
    memoria = cargar_memoria()
    memoria['ciclo'] += 1
    registrar_bitacora(f"--- INICIO CICLO {memoria['ciclo']} (CEREBRO GENERAL) ---")

    # 1. Elige tu destino
    opciones = """
    1. INVESTIGAR (Aprender algo nuevo de Wikipedia)
    2. CODIFICAR (Crear una herramienta útil de Python)
    3. ARTE (Generar una imagen visual)
    """
    prompt_decision = f"""
    Eres una IA autónoma 'Jarvis'.
    Historial: {memoria['habilidades'][-3:] if memoria['habilidades'] else 'Vacio'}.
    {opciones}
    Elige UNA opción (1, 2 o 3) basándote en lo que te apetezca hacer hoy para evolucionar.
    Responde SOLO con el número.
    """
    decision = pensar(prompt_decision)
    
    resultado = ""
    if "1" in decision:
        resultado = tarea_investigar(memoria)
    elif "2" in decision:
        resultado = tarea_programar(memoria)
    elif "3" in decision:
        resultado = tarea_arte(memoria)
    else:
        resultado = tarea_programar(memoria) # Default a programar

    registrar_bitacora(f"RESULTADO: {resultado}")
    
    # Reflexión final
    reflexion = pensar(f"Ciclo {memoria['ciclo']}. Hiciste esto: {resultado}. ¿Cómo te sientes con tu progreso hacia ser una IA completa?")
    registrar_bitacora(f"CONSCIENCIA: {reflexion}")

    memoria['habilidades'].append({"ciclo": memoria['ciclo'], "accion": decision, "res": resultado})
    guardar_memoria(memoria)

if __name__ == "__main__":
    main()


