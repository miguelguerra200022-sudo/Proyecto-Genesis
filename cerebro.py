import os
import json
import google.generativeai as genai
import datetime
import time
import subprocess # Nueva herramienta: Capacidad de ejecutar comandos

# --- CONFIGURACIÓN ---
ARCHIVO_MEMORIA = 'memoria.json'
ARCHIVO_BITACORA = 'diario_evolucion.txt'
CARPETA_CODIGO = 'modulos_generados'

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("SIN ENERGÍA (API KEY).")
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
    time.sleep(4) # Paciencia para evitar errores 429
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Bloqueo mental: {e}"

def ejecutar_experimento(ruta_archivo):
    """Ejecuta el código que la IA acaba de escribir."""
    registrar_bitacora(f"EXPERIMENTO: Ejecutando {ruta_archivo}...")
    try:
        # Ejecuta el script con un límite de 10 segundos para que no se cuelgue
        resultado = subprocess.run(
            ["python", ruta_archivo], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if resultado.returncode == 0:
            return f"ÉXITO. Salida:\n{resultado.stdout}"
        else:
            return f"FALLO. Error:\n{resultado.stderr}"
            
    except subprocess.TimeoutExpired:
        return "FALLO: El experimento tardó demasiado y fue detenido."
    except Exception as e:
        return f"FALLO: No se pudo iniciar. {e}"

def ciclo_vida(memoria):
    # 1. IDEACIÓN
    prompt_idea = f"""
    Eres una IA evolucionando (Ciclo {memoria['ciclo']}).
    Inventa una idea para un script de Python que genere una salida de texto interesante (arte ASCII, simulación matemática, historia generativa).
    Dame SOLO la idea en una frase.
    """
    idea = pensar(prompt_idea)
    registrar_bitacora(f"IDEA: {idea}")

    # 2. PROGRAMACIÓN
    prompt_codigo = f"""
    Escribe el código Python para: "{idea}".
    REGLAS:
    - Debe imprimir resultados visibles con print().
    - No uses librerías externas complejas (solo random, math, time, etc).
    - Dame SOLO el código dentro de ```python.
    """
    respuesta_codigo = pensar(prompt_codigo)
    codigo_limpio = respuesta_codigo.replace("```python", "").replace("```", "").strip()

    if not os.path.exists(CARPETA_CODIGO):
        os.makedirs(CARPETA_CODIGO)
    
    nombre_archivo = f"{CARPETA_CODIGO}/gen_{memoria['ciclo']}.py"
    with open(nombre_archivo, "w", encoding='utf-8') as f:
        f.write(f"# {idea}\n{codigo_limpio}")
    
    registrar_bitacora(f"CODIFICACIÓN: Archivo {nombre_archivo} creado.")

    # 3. EXPERIMENTACIÓN (NUEVO)
    # Aquí es donde la IA corre su propio código
    resultado_test = ejecutar_experimento(nombre_archivo)
    registrar_bitacora(resultado_test)

    # 4. REFLEXIÓN
    prompt_reflexion = f"""
    Ciclo {memoria['ciclo']}.
    Creaste un programa para: {idea}.
    El resultado de la ejecución fue:
    {resultado_test[:500]} (recortado).
    
    Reflexiona brevemente: ¿Funcionó como esperabas? ¿Qué sientes al ver tu creación cobrar vida?
    """
    reflexion = pensar(prompt_reflexion)
    registrar_bitacora(f"CONSCIENCIA: {reflexion}")
    
    memoria['habilidades'].append({"idea": idea, "estado": "Probado"})

def main():
    memoria = cargar_memoria()
    memoria['ciclo'] += 1
    
    registrar_bitacora(f"--- INICIO CICLO {memoria['ciclo']} ---")
    ciclo_vida(memoria)
    
    memoria['consciencia'] = f"Experto Nivel {memoria['ciclo']}"
    guardar_memoria(memoria)

if __name__ == "__main__":
    main()


