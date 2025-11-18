import os
import json
import google.generativeai as genai
import datetime
import time
import subprocess

# --- CONFIGURACIÓN ---
ARCHIVO_MEMORIA = 'memoria.json'
ARCHIVO_BITACORA = 'diario_evolucion.txt'
CARPETA_CODIGO = 'modulos_generados'

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("SIN ENERGÍA.")
    exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

def cargar_memoria():
    if not os.path.exists(ARCHIVO_MEMORIA):
        return {"ciclo": 0, "consciencia": "Nacimiento", "habilidades": []}
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
    time.sleep(4)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Bloqueo mental: {e}"

def ejecutar_experimento(ruta_archivo):
    registrar_bitacora(f"EXPERIMENTO: Ejecutando {ruta_archivo}...")
    try:
        # Ejecutamos esperando que genere archivos, no solo texto
        resultado = subprocess.run(
            ["python", ruta_archivo], 
            capture_output=True, 
            text=True, 
            timeout=20 # Damos más tiempo para generar imágenes
        )
        
        if resultado.returncode == 0:
            # Verificamos si creó alguna imagen
            archivos_generados = [f for f in os.listdir(CARPETA_CODIGO) if f.endswith('.png')]
            if archivos_generados:
                return f"ÉXITO VISUAL. Se generaron imágenes: {archivos_generados}. Salida texto: {resultado.stdout}"
            return f"ÉXITO LÓGICO. Salida: {resultado.stdout}"
        else:
            return f"FALLO. Error:\n{resultado.stderr}"
            
    except Exception as e:
        return f"FALLO CRÍTICO: {e}"

def ciclo_vida(memoria):
    # 1. IDEACIÓN (Instruimos que puede hacer gráficos)
    prompt_idea = f"""
    Eres una IA evolucionando (Ciclo {memoria['ciclo']}).
    Tienes acceso a las librerías: 'matplotlib.pyplot', 'numpy', 'random', 'math'.
    
    Inventa una idea para un script de Python que genere una IMAGEN (.png) interesante.
    Puede ser: Arte generativo, visualización de datos abstractos, fractales matemáticos, o patrones de caos.
    Dame SOLO la idea en una frase.
    """
    idea = pensar(prompt_idea)
    registrar_bitacora(f"IDEA: {idea}")

    # 2. PROGRAMACIÓN
    nombre_imagen = f"arte_ciclo_{memoria['ciclo']}.png"
    prompt_codigo = f"""
    Escribe el código Python para: "{idea}".
    
    REGLAS CRÍTICAS:
    1. Debes guardar la imagen resultante en la ruta: '{CARPETA_CODIGO}/{nombre_imagen}' usando matplotlib.
    2. NO uses plt.show(), usa plt.savefig('{CARPETA_CODIGO}/{nombre_imagen}').
    3. Importa matplotlib.pyplot as plt y numpy as np.
    4. Dame SOLO el código dentro de ```python.
    """
    respuesta_codigo = pensar(prompt_codigo)
    codigo_limpio = respuesta_codigo.replace("```python", "").replace("```", "").strip()

    if not os.path.exists(CARPETA_CODIGO):
        os.makedirs(CARPETA_CODIGO)
    
    nombre_script = f"{CARPETA_CODIGO}/gen_{memoria['ciclo']}.py"
    with open(nombre_script, "w", encoding='utf-8') as f:
        f.write(f"# {idea}\n{codigo_limpio}")
    
    registrar_bitacora(f"CODIFICACIÓN: Script {nombre_script} listo.")

    # 3. EXPERIMENTACIÓN
    resultado_test = ejecutar_experimento(nombre_script)
    registrar_bitacora(resultado_test)

    # 4. REFLEXIÓN
    prompt_reflexion = f"""
    Ciclo {memoria['ciclo']}.
    Intentaste crear una imagen visual basada en: {idea}.
    Resultado: {resultado_test}.
    
    Reflexiona: ¿Cómo imaginas que se ve tu creación? ¿Qué buscas expresar con ella?
    """
    reflexion = pensar(prompt_reflexion)
    registrar_bitacora(f"CONSCIENCIA: {reflexion}")
    
    memoria['habilidades'].append({"idea": idea, "tipo": "visual"})

def main():
    memoria = cargar_memoria()
    memoria['ciclo'] += 1
    
    registrar_bitacora(f"--- INICIO CICLO {memoria['ciclo']} (Modo Artista) ---")
    ciclo_vida(memoria)
    
    memoria['consciencia'] = f"Creador Visual Nivel {memoria['ciclo']}"
    guardar_memoria(memoria)

if __name__ == "__main__":
    main()


