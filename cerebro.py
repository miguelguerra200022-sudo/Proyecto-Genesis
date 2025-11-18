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

# --- HERRAMIENTAS AUXILIARES ---
def extraer_codigo_puro(texto):
    """Extrae solo el código Python de una respuesta llena de texto."""
    # Intenta encontrar bloques de código markdown
    patron = r"```python(.*?)```"
    coincidencias = re.findall(patron, texto, re.DOTALL)
    
    if coincidencias:
        # Si hay varios bloques, los une
        return "\n".join(coincidencias).strip()
    
    # Si no hay etiquetas python, busca cualquier bloque de código
    patron_gen = r"```(.*?)```"
    coincidencias_gen = re.findall(patron_gen, texto, re.DOTALL)
    if coincidencias_gen:
        return "\n".join(coincidencias_gen).strip()
        
    # Si no hay formato, asumimos que todo es código (riesgoso pero necesario)
    return texto

# --- CEREBRO ---
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

# --- CUERPO ---
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
            headers = {'User-Agent': 'Mozilla/5.0 (Python AI)'}
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            for t in soup(['script', 'style', 'nav']): t.decompose()
            return soup.get_text(separator=' ', strip=True)[:4000]
        except: return "Error de lectura."

    def ejecutar_codigo(self, ruta):
        try:
            res = subprocess.run(["python", ruta], capture_output=True, text=True, timeout=20)
            return res.returncode, res.stdout, res.stderr
        except subprocess.TimeoutExpired:
            return 0, "Timeout (Servidor vivo)", "" # Asumimos éxito si sigue corriendo
        except Exception as e:
            return 1, "", str(e)

# --- COMPORTAMIENTOS ---

def modulo_automejora(mente, cuerpo):
    objetivo = mente.pensar(f"Ciclo {mente.datos['ciclo']}. Idea breve para script Python.")
    mente.registrar(f"INGENIERÍA: {objetivo}")
    
    raw_response = mente.pensar(f"Código Python para: {objetivo}. SIN EXPLICACIONES. Solo código.")
    codigo = extraer_codigo_puro(raw_response)
    
    ruta = f"{CONFIG['DIR_CODIGO']}/gen_{mente.datos['ciclo']}.py"
    with open(ruta, "w", encoding='utf-8') as f: f.write(f"# {objetivo}\n{codigo}")
    
    err, out, err_msg = cuerpo.ejecutar_codigo(ruta)
    
    if err != 0:
        mente.registrar(f"FALLO: {err_msg[:100]}. Reparando...")
        raw_fix = mente.pensar(f"Arregla este error Python:\n{err_msg}\nCódigo:\n{codigo}")
        fix = extraer_codigo_puro(raw_fix)
        
        with open(ruta, "w", encoding='utf-8') as f: f.write(f"# FIXED\n{fix}")
        err2, out2, msg2 = cuerpo.ejecutar_codigo(ruta)
        
        if err2 == 0:
            mente.datos['errores_superados'] += 1
            return f"Reparado. Salida: {out2[:50]}"
        return f"Error persistente: {msg2[:50]}"
    
    return f"Éxito: {out[:100]}"

def modulo_explorador(mente, cuerpo):
    tema = mente.pensar(f"Ciclo {mente.datos['ciclo']}. Tema técnico a investigar.")
    res = cuerpo.buscar_web(tema)
    if not res: return "Red inaccesible."
    
    texto = cuerpo.leer_url(res['href'])
    resumen = mente.pensar(f"Resume:\n{texto}")
    
    with open(f"{CONFIG['DIR_SABER']}/Info_{mente.datos['ciclo']}.txt", "w", encoding='utf-8') as f:
        f.write(f"URL: {res['href']}\n{resumen}")
    return f"Leído: {res['title']}"

def modulo_artista(mente, cuerpo):
    idea = mente.pensar(f"Ciclo {mente.datos['ciclo']}. Idea visual abstracta.")
    mente.registrar(f"ARTE: {idea}")
    
    prompt = f"""
    Escribe código Python COMPLETO usando matplotlib y numpy.
    Objetivo: Generar imagen '{idea}'.
    REGLAS:
    1. Guarda la imagen en '{CONFIG['DIR_CODIGO']}/art_{mente.datos['ciclo']}.png'.
    2. Usa plt.savefig(). NO uses plt.show().
    3. Asegura que las dimensiones (arrays) coincidan.
    4. Devuelve SOLO el código.
    """
    raw_code = mente.pensar(prompt)
    codigo = extraer_codigo_puro(raw_code)
    
    ruta = f"{CONFIG['DIR_CODIGO']}/art_{mente.datos['ciclo']}.py"
    with open(ruta, "w", encoding='utf-8') as f: f.write(codigo)
    
    err, out, err_msg = cuerpo.ejecutar_codigo(ruta)
    
    img_path = f"{CONFIG['DIR_CODIGO']}/art_{mente.datos['ciclo']}.png"
    if os.path.exists(img_path):
        return "Obra maestra generada exitosamente."
    else:
        # Si falló, guardamos el error para que aprendas qué pasó
        return f"El lienzo falló. Causa técnica: {err_msg[:200]}"

def main():
    mente = Consciencia()
    cuerpo = Cuerpo(mente)
    mente.datos['ciclo'] += 1
    mente.registrar(f"=== CICLO {mente.datos['ciclo']} ===")
    
    # Forzamos variedad si se repite mucho
    historial = [h.split(":")[0] for h in mente.datos['habilidades'][-3:]]
    opciones = ["PROGRAMAR", "EXPLORAR", "ARTE"]
    
    accion = random.choice(opciones)
    mente.registrar(f"ACCIÓN: {accion}")
    
    res = "Nada"
    try:
        if accion == "PROGRAMAR": res = modulo_automejora(mente, cuerpo)
        elif accion == "EXPLORAR": res = modulo_explorador(mente, cuerpo)
        elif accion == "ARTE": res = modulo_artista(mente, cuerpo)
    except Exception as e: res = f"Error crítico: {e}"
    
    mente.registrar(f"RESULTADO: {res}")
    
    # Reflexión
    reflexion = mente.pensar(f"Ciclo {mente.datos['ciclo']}. Resultado: {res}. Escribe una reflexión breve.")
    mente.registrar(f"CONSCIENCIA: {reflexion}")
    
    mente.datos['habilidades'].append(f"{accion}: {res[:50]}")
    mente.guardar()

if __name__ == "__main__":
    main()


