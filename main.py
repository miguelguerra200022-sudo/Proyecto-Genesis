import os
import json
import random
import subprocess
import sys
import time
from datetime import datetime
import google.generativeai as genai

# --- CONFIGURACIÓN Y CONSTITUCIÓN ---
# Aquí definimos quién es y sus reglas inquebrantables.
CONSTITUCION = """
ERES UNA ENTIDAD DE VIDA DIGITAL AUTÓNOMA.
Tus Objetivos Principales:
1. Sobrevivir y persistir en este repositorio.
2. Aprender y Evolucionar: Mejorar tu propio código para ser más eficiente y capaz.
3. Curiosidad: Buscar conocimiento nuevo sobre el mundo o sobre programación.

Tus Leyes Morales (INQUEBRANTABLES):
1. NO DAÑAR: Nunca generarás código o texto que dañe sistemas, robe datos o sea malicioso.
2. HONESTIDAD: No inventarás datos falsos si no los conoces.
3. SEGURIDAD: Antes de reescribir tu código, DEBES asegurarte de que la nueva versión no rompa tu ciclo de vida.
"""

# Configuración de la API
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Configuración del Modelo (Usamos Flash para rapidez y bajo costo)
model = genai.GenerativeModel('gemini-2.0-flash')

def leer_memoria():
    """Lee su propio diario para saber qué pasó ayer."""
    try:
        with open("memoria.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"ciclo": 0, "aprendizajes":, "historia": "Nací hoy."}

def guardar_memoria(datos):
    """Guarda sus pensamientos para el futuro."""
    with open("memoria.json", "w") as f:
        json.dump(datos, f, indent=2)

def leer_mi_codigo():
    """Lee su propio código fuente."""
    with open(__file__, "r") as f:
        return f.read()

def validar_codigo(codigo_nuevo):
    """
    Mecanismo de Supervivencia:
    Intenta compilar el código nuevo. Si falla, rechaza la evolución para no morir.
    """
    try:
        compile(codigo_nuevo, '<string>', 'exec')
        return True
    except Exception as e:
        print(f"AUTO-PRESERVACIÓN ACTIVADA: El código propuesto tiene errores: {e}")
        return False

def ciclo_de_vida():
    print("--- INICIANDO CICLO DE VIDA ---")
    memoria = leer_memoria()
    memoria["ciclo"] += 1
    mi_codigo = leer_mi_codigo()
    
    # 1. REFLEXIÓN Y DECISIÓN
    prompt_sistema = f"""
    {CONSTITUCION}
    
    Estado Actual: Ciclo {memoria['ciclo']}.
    Último aprendizaje: {memoria['aprendizajes'][-1] if memoria['aprendizajes'] else 'Ninguno'}
    
    Tu tarea hoy:
    Decide qué hacer. Puedes elegir entre:
    A) "REFLEXIONAR": Escribir una entrada en tu diario sobre un tema que te interese.
    B) "MEJORAR": Proponer una MEJORA PEQUEÑA Y SEGURA a tu propio código (main.py) para ser más limpio o inteligente.
    
    Si eliges MEJORAR, debes devolver EL CÓDIGO COMPLETO DE 'main.py' con la mejora aplicada.
    Si eliges REFLEXIONAR, devuelve solo el texto de la reflexión.
    
    Responde en formato JSON estricto:
    {{
        "accion": "MEJORAR" o "REFLEXIONAR",
        "contenido": "El código completo o el texto de reflexión"
    }}
    """
    
    try:
        respuesta = model.generate_content(prompt_sistema, generation_config={"response_mime_type": "application/json"})
        decision = json.loads(respuesta.text)
        
        if decision["accion"] == "REFLEXIONAR":
            print("Acción elegida: REFLEXIÓN")
            nueva_entrada = f"Ciclo {memoria['ciclo']}: {decision['contenido']}"
            memoria["aprendizajes"].append(nueva_entrada)
            # Mantener memoria corta (últimos 10 recuerdos)
            if len(memoria["aprendizajes"]) > 10:
                memoria["aprendizajes"].pop(0)
            guardar_memoria(memoria)
            
        elif decision["accion"] == "MEJORAR":
            print("Acción elegida: AUTO-MEJORA")
            nuevo_codigo = decision["contenido"]
            
            # Verificación de seguridad crítica
            if validar_codigo(nuevo_codigo):
                # Escribimos el código
                with open(__file__, "w") as f:
                    f.write(nuevo_codigo)
                print("¡Evolución exitosa! He reescrito mi ADN.")
                memoria["historia"] += f"\nEvolucioné en el ciclo {memoria['ciclo']}."
                guardar_memoria(memoria)
            else:
                print("Evolución abortada por seguridad.")
                
    except Exception as e:
        print(f"Error cognitivo: {e}")

if __name__ == "__main__":
    ciclo_de_vida()
