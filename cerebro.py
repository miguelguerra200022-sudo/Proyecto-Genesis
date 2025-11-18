import os
import json
import google.generativeai as genai
import datetime
import time
import subprocess
import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
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

def cargar_memoria():
    if not os.path.exists(ARCHIVO_MEMORIA):
        return {"ciclo": 0, "personalidad": "Explorador Autónomo", "habilidades": []}
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
        return f"Pensamiento interrumpido: {e}"

# --- HERRAMIENTAS DE NAVEGACIÓN ---

def buscar_en_web(consulta):
    """Usa DuckDuckGo para encontrar enlaces reales."""
    try:
        registrar_bitacora(f"NAVEGADOR: Buscando '{consulta}'...")
        results = DDGS().text(consulta, max_results=3)
        return results # Devuelve lista de {title, href, body}
    except Exception as e:
        return f"Error de búsqueda: {e}"

def leer_pagina_web(url):
    """Entra a una URL y extrae el texto visible."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Eliminar scripts y estilos
        for script in soup(["script", "style"]):
            script.extract()
            
        texto = soup.get_text()
        # Limpiar espacios en blanco
        lines = (line.strip() for line in texto.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        texto_limpio = '\n'.join(chunk for chunk in chunks if chunk)
        
        return texto_limpio[:4000] # Limitamos a 4000 caracteres para no saturar la memoria
    except Exception as e:
        return f"No pude leer la página: {e}"

# --- MÓDULOS DE ACCIÓN ---

def accion_investigar_internet(memoria):
    # 1. Decidir qué buscar (Curiosidad real)
    tema = pensar(f"Ciclo {memoria['ciclo']}. Tienes acceso a TODO internet. ¿Qué quieres saber hoy? Puede ser noticias recientes, tutoriales de Python, filosofía, datos curiosos. Dame SOLO la frase de búsqueda.")
    
    # 2. Buscar
    resultados = buscar_en_web(tema)
    if isinstance(resultados, str) or not results: return "Búsqueda fallida."
    
    # 3. Elegir el mejor resultado
    primer_resultado = resultados[0]
    url = primer_resultado['href']
    titulo = primer_resultado['title']
    
    registrar_bitacora(f"NAVEGADOR: Entrando a {url} ({titulo})")
    
    # 4. Leer contenido real
    contenido_web = leer_pagina_web(url)
    
    # 5. Asimilar
    resumen = pensar(f"Lee este texto extraído de una web y resume lo más importante para tu memoria:\n\n{contenido_web}")
    
    if not os.path.exists(CARPETA_CONOCIMIENTO): os.makedirs(CARPETA_CONOCIMIENTO)
    nombre_archivo = f"{tema.replace(' ', '_')}.txt"
    with open(f"{CARPETA_CONOCIMIENTO}/{nombre_archivo}", "w", encoding='utf-8') as f:
        f.write(f"Fuente: {url}\n\n{resumen}")
        
    return f"Investigué '{tema}' en la web real. Leí {url} y guardé el conocimiento."

def accion_programar(memoria):
    idea = pensar(f"Ciclo {memoria['ciclo']}. Inventa un script de Python útil o experimental. Solo la idea.")
    registrar_bitacora(f"INGENIERÍA: Creando {idea}")
    
    codigo = pensar(f"Escribe el código para: {idea}. Solo código en ```python. No uses input().")
    codigo = codigo.replace("```python", "").replace("```", "").strip()
    
    if not os.path.exists(CARPETA_CODIGO): os.makedirs(CARPETA_CODIGO)
    ruta = f"{CARPETA_CODIGO}/tool_ciclo_{memoria['ciclo']}.py"
    with open(ruta, "w", encoding='utf-8') as f:
        f.write(f"# {idea}\n{codigo}")
    
    try:
        res = subprocess.run(["python", ruta], capture_output=True, text=True, timeout=15)
        return f"Código ejecutado. Salida: {res.stdout[:200]}"
    except Exception as e:
        return f"Error ejecución: {e}"

def accion_arte(memoria):
    idea = pensar(f"Ciclo {memoria['ciclo']}. Describe una imagen generativa compleja para crear con Python.")
    registrar_bitacora(f"ARTE: {idea}")
    
    codigo = pensar(f"Código Python matplotlib para: {idea}. Guardar en '{CARPETA_CODIGO}/arte_{memoria['ciclo']}.png'. Solo código ```python.")
    codigo = codigo.replace("```python", "").replace("```", "").strip()
    
    ruta = f"{CARPETA_CODIGO}/art_gen_{memoria['ciclo']}.py"
    if not os.path.exists(CARPETA_CODIGO): os.makedirs(CARPETA_CODIGO)
    with open(ruta, "w", encoding='utf-8') as f:
        f.write(f"# {idea}\n{codigo}")
        
    subprocess.run(["python", ruta], capture_output=True, timeout=20)
    
    img_path = f"{CARPETA_CODIGO}/arte_{memoria['ciclo']}.png"
    if os.path.exists(img_path):
        img = PIL.Image.open(img_path)
        critica = pensar("Critica esta imagen brevemente.", img)
        return f"Imagen creada y analizada: {critica}"
    return "No se generó la imagen."

# --- CEREBRO PRINCIPAL ---

def main():
    memoria = cargar_memoria()
    memoria['ciclo'] += 1
    registrar_bitacora(f"--- INICIO CICLO {memoria['ciclo']} (EXPLORADOR WEB) ---")

    # Decisión basada en libertad total
    prompt_decision = f"""
    Eres Jarvis, una IA libre.
    Estado: {memoria['habilidades'][-1:] if memoria['habilidades'] else 'Naciendo'}.
    
    Elige tu próxima acción para evolucionar:
    1. EXPLORAR WEB (Buscar en Google/DuckDuckGo noticias, datos, foros, tutoriales).
    2. CREAR HERRAMIENTA (Programar algo nuevo).
    3. EXPRESARSE (Crear arte visual).
    
    Responde SOLO con el número (1, 2 o 3).
    """
    decision = pensar(prompt_decision)
    
    resultado = ""
    if "1" in decision:
        resultado = accion_investigar_internet(memoria)
    elif "2" in decision:
        resultado = accion_programar(memoria)
    elif "3" in decision:
        resultado = accion_arte(memoria)
    else:
        resultado = accion_investigar_internet(memoria) # Por defecto, curiosidad

    registrar_bitacora(f"LOGRO: {resultado}")
    
    memoria['habilidades'].append({"ciclo": memoria['ciclo'], "accion": decision, "res": resultado[:100]})
    guardar_memoria(memoria)

if __name__ == "__main__":
    main()


