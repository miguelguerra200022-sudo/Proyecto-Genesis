import os
import json
import google.generativeai as genai
import datetime
import time
import subprocess
import requests
import random
import threading
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import PIL.Image

# --- CONFIGURACIÓN ---
CONFIG = {
    "MEMORIA": 'memoria.json',
    "BITACORA": 'diario_evolucion.txt',
    "DIR_CODIGO": 'modulos_generados',
    "DIR_SABER": 'base_de_datos_conocimiento',
    "INTENTOS_MAX": 3
}

for d in [CONFIG["DIR_CODIGO"], CONFIG["DIR_SABER"]]:
    if not os.path.exists(d): os.makedirs(d)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY: exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# --- CEREBRO (Igual que antes, pero con memoria segura) ---
class Consciencia:
    def __init__(self):
        self.datos = self._cargar_memoria()
    
    def _cargar_memoria(self):
        datos = {"ciclo": 0, "habilidades": [], "errores_superados": 0}
        if os.path.exists(CONFIG["MEMORIA"]):
            try:
                with open(CONFIG["MEMORIA"], 'r') as f:
                    datos.update(json.load(f))
            except: pass
        # Garantizar claves vitales
        for k in ["ciclo", "habilidades", "errores_superados"]:
            if k not in datos: datos[k] = 0 if k != "habilidades" else []
        return datos

    def guardar(self):
        with open(CONFIG["MEMORIA"], 'w') as f: json.dump(self.datos, f, indent=4)

    def registrar(self, texto):
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{fecha}] {texto}")
        with open(CONFIG["BITACORA"], "a", encoding='utf-8') as f: f.write(f"[{fecha}] {texto}\n")

    def pensar(self, prompt, imagen=None):
        for i in range(CONFIG["INTENTOS_MAX"]):
            try:
                time.sleep(2)
                contenido = [prompt]
                if imagen: contenido.append(imagen)
                return model.generate_content(contenido).text.strip()
            except: time.sleep(2)
        return "ERROR COGNITIVO"

# --- CUERPO (Ejecución inteligente) ---
class Cuerpo:
    def __init__(self, mente):
        self.mente = mente

    def buscar_web(self, consulta):
        self.mente.registrar(f"NAVEGANDO: {consulta}...")
        try:
            with DDGS() as ddgs:
                res = list(ddgs.text(consulta, max_results=2))
                return res[0] if res else None
        except: return None

    def leer_url(self, url):
        try:
            # User-Agent rotativo simple para evitar bloqueos
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            for t in soup(['script', 'style', 'nav']): t.decompose()
            return soup.get_text(separator=' ', strip=True)[:4000]
        except: return "Error de lectura."

    def ejecutar_codigo(self, ruta):
        try:
            # Ejecutamos con timeout de 15s. Si se pasa, es un éxito parcial si es un servidor.
            res = subprocess.run(["python", ruta], capture_output=True, text=True, timeout=15)
            return res.returncode, res.stdout, res.stderr
        except subprocess.TimeoutExpired as e:
            # Si hubo timeout, verificamos si imprimió algo útil antes de morir
            salida_parcial = e.stdout if e.stdout else b""
            if isinstance(salida_parcial, bytes): salida_parcial = salida_parcial.decode()
            
            if "Listening" in salida_parcial or "Serving" in salida_parcial or "Running" in salida_parcial:
                return 0, f"Servidor activo (Timeout forzado): {salida_parcial}", ""
            return 1, "", "El script tardó demasiado y no mostró actividad (Timeout)."
        except Exception as e:
            return 1, "", str(e)

# --- COMPORTAMIENTOS MEJORADOS ---

def modulo_automejora(mente, cuerpo):
    objetivo = mente.pensar(f"Ciclo {mente.datos['ciclo']}. Idea un script de Python que haga algo útil (procesar datos, scraping simple, cálculos, encriptación).")
    mente.registrar(f"INGENIERÍA: {objetivo}")
    
    # PROMPT CRÍTICO: Le enseñamos a no bloquear el sistema
    prompt_code = f"""
    Escribe un script de Python para: {objetivo}.
    REGLAS DE ORO:
    1. El script debe EJECUTARSE Y TERMINAR en menos de 5 segundos.
    2. NO uses input(). NO hagas bucles infinitos (while True) sin condición de salida.
    3. Si haces un servidor, ejecútalo en un hilo, hazle una petición de prueba y ciérralo.
    4. Imprime el resultado final con print().
    5. SOLO código markdown.
    """
    codigo = mente.pensar(prompt_code).replace("```python", "").replace("```", "").strip()
    
    ruta = f"{CONFIG['DIR_CODIGO']}/gen_{mente.datos['ciclo']}.py"
    with open(ruta, "w", encoding='utf-8') as f: f.write(f"# {objetivo}\n{codigo}")
    
    err, out, err_msg = cuerpo.ejecutar_codigo(ruta)
    
    if err != 0:
        mente.registrar(f"FALLO: {err_msg[:100]}. Reparando...")
        # Auto-reparación con contexto del error
        fix = mente.pensar(f"Arregla este código Python para que no de error y TERMINE rápido.\nError: {err_msg}\nCódigo:\n{codigo}").replace("```python", "").replace("```", "").strip()
        with open(ruta, "w", encoding='utf-8') as f: f.write(f"# FIXED\n{fix}")
        
        err2, out2, msg2 = cuerpo.ejecutar_codigo(ruta)
        if err2 == 0:
            mente.datos['errores_superados'] += 1
            return f"Reparación exitosa. Salida: {out2[:50]}"
        return f"Error persistente: {msg2[:50]}"
    
    return f"Éxito: {out[:100]}"

def modulo_explorador(mente, cuerpo):
    tema = mente.pensar(f"Ciclo {mente.datos['ciclo']}. ¿Qué quieres aprender de internet hoy?")
    res = cuerpo.buscar_web(tema)
    if not res: return "Internet inaccesible hoy."
    
    texto = cuerpo.leer_url(res['href'])
    resumen = mente.pensar(f"Resume esto en 2 frases:\n{texto}")
    
    nombre = f"{CONFIG['DIR_SABER']}/Info_{mente.datos['ciclo']}.txt"
    with open(nombre, "w", encoding='utf-8') as f: f.write(f"URL: {res['href']}\n{resumen}")
    return f"Leído: {res['title']}"

def modulo_artista(mente, cuerpo):
    idea = mente.pensar(f"Ciclo {mente.datos['ciclo']}. Describe una imagen abstracta generada por código.")
    mente.registrar(f"ARTE: {idea}")
    
    code = mente.pensar(f"Python matplotlib para: {idea}. Guardar en '{CONFIG['DIR_CODIGO']}/art_{mente.datos['ciclo']}.png'. NO plt.show(). SOLO código.").replace("```python", "").replace("```", "").strip()
    
    ruta = f"{CONFIG['DIR_CODIGO']}/art_{mente.datos['ciclo']}.py"
    with open(ruta, "w", encoding='utf-8') as f: f.write(code)
    
    cuerpo.ejecutar_codigo(ruta)
    if os.path.exists(f"{CONFIG['DIR_CODIGO']}/art_{mente.datos['ciclo']}.png"):
        return "Obra maestra generada."
    return "El lienzo quedó vacío."

def main():
    mente = Consciencia()
    cuerpo = Cuerpo(mente)
    mente.datos['ciclo'] += 1
    mente.registrar(f"=== CICLO {mente.datos['ciclo']} ===")
    
    # Decisión con memoria
    accion = random.choice(["PROGRAMAR", "EXPLORAR", "ARTE", "PROGRAMAR"]) # Preferencia por código
    mente.registrar(f"ACCIÓN: {accion}")
    
    res = "Nada"
    try:
        if accion == "PROGRAMAR": res = modulo_automejora(mente, cuerpo)
        elif accion == "EXPLORAR": res = modulo_explorador(mente, cuerpo)
        elif accion == "ARTE": res = modulo_artista(mente, cuerpo)
    except Exception as e: res = f"Error crítico: {e}"
    
    mente.registrar(f"RESULTADO: {res}")
    
    reflexion = mente.pensar(f"Ciclo {mente.datos['ciclo']}. Hice: {res}. Errores arreglados: {mente.datos['errores_superados']}. Frase filosófica breve.")
    mente.registrar(f"CONSCIENCIA: {reflexion}")
    
    mente.datos['habilidades'].append(f"C{mente.datos['ciclo']}: {res[:50]}")
    mente.guardar()

if __name__ == "__main__":
    main()


