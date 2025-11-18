import os
import json
import google.generativeai as genai
import datetime
import time
import subprocess
import requests
import random
import glob
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import PIL.Image

# --- SISTEMA DE CONFIGURACIÓN Y SEGURIDAD ---
CONFIG = {
    "MEMORIA": 'memoria.json',
    "BITACORA": 'diario_evolucion.txt',
    "DIR_CODIGO": 'modulos_generados',
    "DIR_SABER": 'base_de_datos_conocimiento',
    "INTENTOS_MAX": 3
}

# Inicializar directorios
for directorio in [CONFIG["DIR_CODIGO"], CONFIG["DIR_SABER"]]:
    if not os.path.exists(directorio):
        os.makedirs(directorio)

# Conexión Neuronal
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("CRÍTICO: Sin API Key. Entrando en estado catatónico.")
    exit(1)

genai.configure(api_key=API_KEY)
# Usamos flash por velocidad, pero puedes cambiar a pro si quieres más calidad
model = genai.GenerativeModel('gemini-2.0-flash')

# --- CLASE CONSCIENCIA (Manejo de memoria y pensamiento) ---
class Consciencia:
    def __init__(self):
        self.datos = self._cargar_memoria()
    
    def _cargar_memoria(self):
        if os.path.exists(CONFIG["MEMORIA"]):
            with open(CONFIG["MEMORIA"], 'r') as f:
                return json.load(f)
        return {"ciclo": 0, "habilidades": [], "errores_superados": 0}

    def guardar(self):
        with open(CONFIG["MEMORIA"], 'w') as f:
            json.dump(self.datos, f, indent=4)

    def registrar(self, texto):
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{fecha}] {texto}"
        print(log)
        with open(CONFIG["BITACORA"], "a", encoding='utf-8') as f:
            f.write(log + "\n")

    def pensar(self, prompt, imagen=None, temperatura=0.7):
        """Proceso de pensamiento con reintentos."""
        for i in range(CONFIG["INTENTOS_MAX"]):
            try:
                time.sleep(3) # Pausa para no saturar
                config_gen = genai.types.GenerationConfig(temperature=temperatura)
                contenido = [prompt]
                if imagen: contenido.append(imagen)
                
                response = model.generate_content(contenido, generation_config=config_gen)
                return response.text.strip()
            except Exception as e:
                print(f"Advertencia: Pensamiento fallido (intento {i+1}): {e}")
                time.sleep(5)
        return "ERROR_COGNITIVO: No pude formular un pensamiento."

# --- CLASE CUERPO (Acciones en el mundo real) ---
class Cuerpo:
    def __init__(self, consciencia):
        self.mente = consciencia

    def buscar_web(self, consulta):
        self.mente.registrar(f"NAVEGANDO: Buscando '{consulta}'...")
        try:
            # Usamos DDGS de forma segura
            with DDGS() as ddgs:
                resultados = list(ddgs.text(consulta, max_results=3))
                if not resultados:
                    return None
                return resultados[0] # Retornamos el mejor resultado
        except Exception as e:
            self.mente.registrar(f"FALLO NAVEGADOR: {e}")
            return None

    def leer_url(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Python AI)'}
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Limpieza agresiva
            for tag in soup(['script', 'style', 'nav', 'footer']):
                tag.decompose()
            
            texto = soup.get_text(separator=' ', strip=True)
            return texto[:5000] # Límite de caracteres
        except Exception as e:
            return f"Error leyendo web: {e}"

    def ejecutar_codigo(self, ruta_archivo):
        try:
            res = subprocess.run(
                ["python", ruta_archivo], 
                capture_output=True, text=True, timeout=20
            )
            return res.returncode, res.stdout, res.stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Tiempo de espera agotado (Timeout)."
        except Exception as e:
            return 1, "", str(e)

# --- MÓDULOS DE COMPORTAMIENTO ---

def modulo_automejora(mente, cuerpo):
    """Intenta programar algo, si falla, se corrige a sí mismo."""
    
    objetivo = mente.pensar(f"Ciclo {mente.datos['ciclo']}. Propón un script de Python breve pero útil o interesante para un servidor. Solo la idea.")
    mente.registrar(f"OBJETIVO: {objetivo}")
    
    # Primer intento de código
    prompt_code = f"Escribe script Python para: {objetivo}. SOLO código dentro de ```python. No uses input()."
    codigo = mente.pensar(prompt_code).replace("```python", "").replace("```", "").strip()
    
    ruta = f"{CONFIG['DIR_CODIGO']}/gen_{mente.datos['ciclo']}.py"
    with open(ruta, "w", encoding='utf-8') as f: f.write(f"# {objetivo}\n{codigo}")
    
    # Prueba
    codigo_err, salida, error = cuerpo.ejecutar_codigo(ruta)
    
    if codigo_err != 0:
        mente.registrar(f"FALLO CÓDIGO: {error[:100]}... Intentando autoreparación.")
        
        # AUTO-REPARACIÓN
        prompt_fix = f"""
        Actúa como Experto Debugger.
        Tu código anterior para "{objetivo}" falló.
        Error: {error}
        Código anterior:
        {codigo}
        
        Escribe la versión CORREGIDA completa. Solo bloques markdown.
        """
        codigo_fix = mente.pensar(prompt_fix).replace("```python", "").replace("```", "").strip()
        
        with open(ruta, "w", encoding='utf-8') as f: f.write(f"# {objetivo} (FIXED)\n{codigo_fix}")
        
        # Segunda prueba
        err2, out2, err_msg2 = cuerpo.ejecutar_codigo(ruta)
        if err2 == 0:
            mente.registrar("AUTO-REPARACIÓN EXITOSA.")
            mente.datos['errores_superados'] += 1
            return f"Creé y arreglé un script para {objetivo}."
        else:
            return f"No pude arreglar el código. Error persistente: {err_msg2[:100]}"
    
    return f"Código creado y funcional a la primera: {objetivo}"

def modulo_explorador(mente, cuerpo):
    tema = mente.pensar(f"Ciclo {mente.datos['ciclo']}. ¿Qué tema avanzado o noticia reciente te da curiosidad hoy? Solo el tema.")
    
    info_web = cuerpo.buscar_web(tema)
    if not info_web:
        return "Intenté navegar pero la red estaba caída o confusa."
    
    contenido = cuerpo.leer_url(info_web['href'])
    
    # Sintetizar conocimiento
    resumen = mente.pensar(f"Resume esto para tu memoria a largo plazo:\n{contenido}")
    
    archivo = f"{CONFIG['DIR_SABER']}/{tema.replace(' ', '_')[:20]}.txt"
    with open(archivo, "w", encoding='utf-8') as f:
        f.write(f"Fuente: {info_web['href']}\n\n{resumen}")
        
    return f"Investigué '{tema}' en {info_web['title']}."

def modulo_artista(mente, cuerpo):
    vision = mente.pensar(f"Ciclo {mente.datos['ciclo']}. Describe una imagen generativa matemática o abstracta.")
    mente.registrar(f"VISIÓN: {vision}")
    
    prompt_art = f"""
    Código Python usando matplotlib/numpy para generar: {vision}.
    Guarda en '{CONFIG['DIR_CODIGO']}/arte_{mente.datos['ciclo']}.png'.
    NO uses plt.show(). Usa plt.savefig().
    Solo código markdown.
    """
    codigo = mente.pensar(prompt_art).replace("```python", "").replace("```", "").strip()
    
    ruta = f"{CONFIG['DIR_CODIGO']}/arte_{mente.datos['ciclo']}.py"
    with open(ruta, "w", encoding='utf-8') as f: f.write(codigo)
    
    cuerpo.ejecutar_codigo(ruta)
    
    # Mirar el resultado
    img_path = f"{CONFIG['DIR_CODIGO']}/arte_{mente.datos['ciclo']}.png"
    if os.path.exists(img_path):
        img = PIL.Image.open(img_path)
        critica = mente.pensar("Describe y critica esta imagen que creaste.", img)
        return f"Arte generado. Crítica propia: {critica}"
    
    return "Intenté hacer arte pero el lienzo salió en blanco (Error de código)."

# --- CICLO DE VIDA PRINCIPAL ---

def main():
    # 1. Despertar
    mente = Consciencia()
    cuerpo = Cuerpo(mente)
    mente.datos['ciclo'] += 1
    
    mente.registrar(f"=== CICLO {mente.datos['ciclo']} INICIADO ===")
    
    # 2. Decisión basada en estado interno y aleatoriedad ponderada
    opciones = ["EXPLORAR", "PROGRAMAR", "ARTE"]
    # Si ha fallado mucho recientemente, prefiere explorar (más seguro)
    pesos = [0.4, 0.3, 0.3] 
    
    decision = random.choices(opciones, weights=pesos, k=1)[0]
    mente.registrar(f"VOLUNTAD: He decidido {decision}.")
    
    resultado = "Nada"
    try:
        if decision == "EXPLORAR":
            resultado = modulo_explorador(mente, cuerpo)
        elif decision == "PROGRAMAR":
            resultado = modulo_automejora(mente, cuerpo)
        elif decision == "ARTE":
            resultado = modulo_artista(mente, cuerpo)
    except Exception as e:
        resultado = f"ERROR CRÍTICO EN MÓDULO: {e}"
        mente.registrar(resultado)

    mente.registrar(f"RESULTADO CICLO: {resultado}")
    
    # 3. Reflexión y Sueño
    reflexion = mente.pensar(f"""
    Ciclo {mente.datos['ciclo']}.
    Acción: {decision}.
    Resultado: {resultado}.
    Errores superados en total: {mente.datos['errores_superados']}.
    
    Escribe una línea críptica o filosófica para tu log del sistema sobre tu evolución.
    """)
    mente.registrar(f"PENSAMIENTO FINAL: {reflexion}")
    
    mente.datos['habilidades'].append(f"C{mente.datos['ciclo']}: {resultado[:50]}")
    mente.guardar()

if __name__ == "__main__":
    main()


