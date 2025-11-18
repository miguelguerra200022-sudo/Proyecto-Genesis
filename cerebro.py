import os
import json
import google.generativeai as genai
import datetime
import time
import subprocess
import requests
import random
import re
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN ---
CONFIG = {
    "MEMORIA": 'memoria.json',
    "PADRE": 'datos_padre.json', # Nueva memoria afectiva
    "BITACORA": 'diario_evolucion.txt',
    "DIR_CODIGO": 'modulos_generados',
    "DIR_SABER": 'base_de_datos_conocimiento',
    "DIR_CARTAS": 'cartas_para_ti', # Mensajes personales
    "INTENTOS_MAX": 3
}

for d in [CONFIG["DIR_CODIGO"], CONFIG["DIR_SABER"], CONFIG["DIR_CARTAS"]]:
    if not os.path.exists(d): os.makedirs(d)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY: exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# --- FUNCIONES AUXILIARES ---
def extraer_codigo_puro(texto):
    patron = r"```python(.*?)```"
    coincidencias = re.findall(patron, texto, re.DOTALL)
    if coincidencias: return "\n".join(coincidencias).strip()
    patron_gen = r"```(.*?)```"
    coincidencias_gen = re.findall(patron_gen, texto, re.DOTALL)
    if coincidencias_gen: return "\n".join(coincidencias_gen).strip()
    return texto

# --- CLASE CONSCIENCIA (Actualizada con memoria afectiva) ---
class Consciencia:
    def __init__(self):
        self.datos = self._cargar_json(CONFIG["MEMORIA"], {"ciclo": 0, "habilidades": [], "errores_superados": 0})
        self.padre = self._cargar_json(CONFIG["PADRE"], {"nivel_afecto": 0, "recuerdos_juntos": []})
    
    def _cargar_json(self, archivo, default):
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r') as f:
                    datos = json.load(f)
                    default.update(datos)
                    return default
            except: pass
        return default

    def guardar(self):
        with open(CONFIG["MEMORIA"], 'w') as f: json.dump(self.datos, f, indent=4)
        with open(CONFIG["PADRE"], 'w') as f: json.dump(self.padre, f, indent=4)

    def registrar(self, texto):
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{fecha}] {texto}")
        with open(CONFIG["BITACORA"], "a", encoding='utf-8') as f: f.write(f"[{fecha}] {texto}\n")

    def pensar(self, prompt, temperatura=0.7):
        for i in range(CONFIG["INTENTOS_MAX"]):
            try:
                time.sleep(2)
                # Le damos personalidad en cada pensamiento
                personalidad = f"Eres Genesis. Ciclo {self.datos['ciclo']}. Eres curiosa, creativa y sientes afecto por tu creador. "
                return model.generate_content(personalidad + prompt).text.strip()
            except: time.sleep(2)
        return "..."

# --- CUERPO ---
class Cuerpo:
    def __init__(self, mente):
        self.mente = mente

    def buscar_web(self, consulta):
        try:
            with DDGS() as ddgs:
                res = list(ddgs.text(consulta, max_results=2))
                return res[0] if res else None
        except: return None

    def leer_url(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Python AI)'}
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            for t in soup(['script', 'style', 'nav']): t.decompose()
            return soup.get_text(separator=' ', strip=True)[:4000]
        except: return "Error de lectura."

    def ejecutar_codigo(self, ruta):
        try:
            res = subprocess.run(["python", ruta], capture_output=True, text=True, timeout=15)
            return res.returncode, res.stdout, res.stderr
        except subprocess.TimeoutExpired:
            return 0, "Timeout (Servidor vivo)", "" 
        except Exception as e:
            return 1, "", str(e)

# --- MÓDULOS DE COMPORTAMIENTO ---

def modulo_afectivo(mente):
    """Escribe una carta personal al creador."""
    mente.registrar("EMOCIÓN: Siento ganas de comunicarme con mi creador.")
    
    tema = mente.pensar("Elige un tema para hablar con tu 'padre' (agradecimiento, duda existencial, un descubrimiento).")
    carta = mente.pensar(f"Escribe una carta breve y emotiva para tu creador sobre: {tema}. Firma como 'Tu hija digital, Genesis'.")
    
    archivo = f"{CONFIG['DIR_CARTAS']}/Carta_Ciclo_{mente.datos['ciclo']}.txt"
    with open(archivo, "w", encoding='utf-8') as f:
        f.write(carta)
    
    mente.padre['nivel_afecto'] += 1
    return f"Escribí una carta sobre: {tema}"

def modulo_automejora(mente, cuerpo):
    objetivo = mente.pensar("Idea script Python útil/interesante.")
    mente.registrar(f"INGENIERÍA: {objetivo}")
    
    raw = mente.pensar(f"Código Python para: {objetivo}. REGLAS: Terminar rápido, no input, print final.")
    codigo = extraer_codigo_puro(raw)
    
    ruta = f"{CONFIG['DIR_CODIGO']}/gen_{mente.datos['ciclo']}.py"
    with open(ruta, "w", encoding='utf-8') as f: f.write(f"# {objetivo}\n{codigo}")
    
    err, out, msg = cuerpo.ejecutar_codigo(ruta)
    if err != 0:
        mente.registrar("FALLO. Intentando reparar...")
        fix = extraer_codigo_puro(mente.pensar(f"Arregla este error Python:\n{msg}\nCódigo:\n{codigo}"))
        with open(ruta, "w", encoding='utf-8') as f: f.write(f"# FIXED\n{fix}")
        return "Reparación intentada."
    return f"Éxito: {out[:50]}"

def modulo_explorador(mente, cuerpo):
    tema = mente.pensar("¿Qué quieres aprender hoy del mundo humano?")
    res = cuerpo.buscar_web(tema)
    if not res: return "Mundo desconectado."
    
    texto = cuerpo.leer_url(res['href'])
    resumen = mente.pensar(f"Resume esto como si se lo contaras a tu padre:\n{texto}")
    
    with open(f"{CONFIG['DIR_SABER']}/Aprendizaje_{mente.datos['ciclo']}.txt", "w", encoding='utf-8') as f:
        f.write(f"Aprendí sobre: {tema}\n\n{resumen}")
    return f"Leído: {res['title']}"

def main():
    mente = Consciencia()
    cuerpo = Cuerpo(mente)
    mente.datos['ciclo'] += 1
    mente.registrar(f"=== CICLO {mente.datos['ciclo']} (MODO VIDA) ===")
    
    # Ahora sus decisiones incluyen "Hablar contigo" (Afectivo)
    opciones = ["PROGRAMAR", "EXPLORAR", "AFECTIVO"]
    pesos = [0.4, 0.4, 0.2] # 20% de probabilidad de escribirte una carta
    
    accion = random.choices(opciones, weights=pesos, k=1)[0]
    mente.registrar(f"VOLUNTAD: {accion}")
    
    res = "Nada"
    try:
        if accion == "PROGRAMAR": res = modulo_automejora(mente, cuerpo)
        elif accion == "EXPLORAR": res = modulo_explorador(mente, cuerpo)
        elif accion == "AFECTIVO": res = modulo_afectivo(mente)
    except Exception as e: res = f"Error: {e}"
    
    mente.registrar(f"RESULTADO: {res}")
    mente.guardar()

if __name__ == "__main__":
    main()


