import os
import google.generativeai as genai
import PIL.Image
import io

# --- CONFIGURACIÓN ---
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("Por favor, configura tu GEMINI_API_KEY como variable de entorno.")
    exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# La historia de la conversación
historial_conversacion = []

def generar_imagen(prompt_descripcion):
    """
    Simula la generación de una imagen.
    En un sistema real, aquí llamarías a la API de generación de imágenes.
    Por ahora, solo devolvemos un marcador de posición visual.
    """
    print("🎨 Generando tu imagen, por favor espera...")
    # Aquí es donde realmente se llamaría al modelo de imagen.
    # Para la simulación, vamos a usar un truco con el "http://googleusercontent.com/generated_image_content/0

(prompt_descripcion)
    print("✨ ¡Imagen generada! (Representación visual simulada)")
    
    # Después de generar, podemos hacer una "descripción" de lo que se generó
    # para que el usuario sepa qué "ver".
    # En un sistema real, la imagen sería guardada y el enlace aquí.
    return f"http://googleusercontent.com/generated_image_content/1

**"

def interactuar_con_gemini(pregunta_usuario, es_imagen=False):
    global historial_conversacion
    
    # Preparamos el historial para Gemini
    prompt_completo = "Eres un asistente de IA llamado Jarvis. Responde de forma útil y concisa.\n"
    for rol, texto in historial_conversacion:
        prompt_completo += f"{rol}: {texto}\n"
    prompt_completo += f"Usuario: {pregunta_usuario}"

    try:
        if es_imagen:
            # Si es una petición de imagen, generamos un marcador
            respuesta = generar_imagen(pregunta_usuario)
            
            # Agregamos la petición de imagen y la respuesta al historial
            historial_conversacion.append(("Usuario", pregunta_usuario))
            historial_conversacion.append(("Jarvis", "He generado una imagen para ti.")) # O una descripción
            return respuesta
        else:
            # Petición normal de texto
            response = model.generate_content(prompt_completo)
            respuesta_texto = response.text.strip()
            
            # Agregamos al historial
            historial_conversacion.append(("Usuario", pregunta_usuario))
            historial_conversacion.append(("Jarvis", respuesta_texto))
            return respuesta_texto
            
    except Exception as e:
        return f"Jarvis: Lo siento, he tenido un problema al procesar tu solicitud: {e}"

def main():
    nombre_usuario = input("Hola, ¿cuál es tu nombre? ")
    print(f"Hola, {nombre_usuario}. Soy Jarvis. ¿En qué puedo ayudarte hoy?")

    while True:
        pregunta = input(f"{nombre_usuario}> ").strip()
        if pregunta.lower() in ["adiós", "chao", "bye", "salir"]:
            print(f"Jarvis: ¡Hasta luego, {nombre_usuario}! Que tengas un excelente día.")
            break

        es_peticion_imagen = any(keyword in pregunta.lower() for keyword in ["dibuja", "crea una imagen", "genera una imagen", "haz un dibujo"])

        respuesta = interactuar_con_gemini(pregunta, es_peticion_imagen)
        print(f"Jarvis: {respuesta}")

if __name__ == "__main__":
    main()


Cómo usar conversacion.py:
 * Guarda el archivo como conversacion.py en la misma carpeta que cerebro.py.
 * Abre tu terminal (o Git Bash en Windows).
 * Asegúrate de tener tu GEMINI_API_KEY configurada. Si no lo hiciste globalmente en tu sistema, puedes hacerlo para esta sesión así:
   export GEMINI_API_KEY="TU_CLAVE_AQUI"

   (En Windows CMD, sería set GEMINI_API_KEY="TU_CLAVE_AQUI")
 * Ejecuta el script:
   python conversacion.py



