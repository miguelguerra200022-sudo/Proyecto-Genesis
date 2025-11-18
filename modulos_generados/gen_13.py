# FIXED
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

def analizar_sentimiento_noticias(tema, sitios_web):
    """
    Analiza el sentimiento de titulares de noticias sobre un tema específico de varios sitios web.

    Args:
        tema (str): El tema sobre el cual se analizarán las noticias.
        sitios_web (list): Lista de URLs de sitios web de noticias a analizar.

    Returns:
        dict: Un diccionario con el análisis de sentimiento:
              - 'positivo': porcentaje de titulares positivos.
              - 'negativo': porcentaje de titulares negativos.
              - 'neutral': porcentaje de titulares neutrales.
              - 'ejemplos': una lista de tuplas con titulares y su polaridad.
    """

    titulares = []
    for sitio_web in sitios_web:
        try:
            response = requests.get(sitio_web)
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
            soup = BeautifulSoup(response.content, 'html.parser')

            # Ajusta esto según la estructura del HTML de cada sitio web
            for link in soup.find_all('a'):
                titulo = link.get_text()
                if tema.lower() in titulo.lower():
                    titulares.append(titulo)
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {sitio_web}: {e}")
        except Exception as e:
            print(f"Error al procesar {sitio_web}: {e}")


    sentimientos = []
    for titulo in titulares:
        analisis = TextBlob(titulo)
        polaridad = analisis.sentiment.polarity
        sentimientos.append(polaridad)

    positivo = sum(1 for s in sentimientos if s > 0.1)
    negativo = sum(1 for s in sentimientos if s < -0.1)
    neutral = sum(1 for s in sentimientos if -0.1 <= s <= 0.1)

    total = len(sentimientos)
    if total > 0:
        porcentaje_positivo = (positivo / total) * 100
        porcentaje_negativo = (negativo / total) * 100
        porcentaje_neutral = (neutral / total) * 100
    else:
        porcentaje_positivo = 0
        porcentaje_negativo = 0
        porcentaje_neutral = 0

    ejemplos = []
    for i, titulo in enumerate(titulares):
         analisis = TextBlob(titulo)
         polaridad = analisis.sentiment.polarity
         if abs(polaridad) > 0.1:
              ejemplos.append((titulo, "Positivo" if polaridad > 0 else "Negativo"))
         elif len(ejemplos) < 5: # Incluye algunos neutrales si hay pocos ejemplos significativos
              ejemplos.append((titulo, "Neutral"))
         if len(ejemplos) >= 5:
              break  # Solo mostrar 5 ejemplos

    return {
        'positivo': porcentaje_positivo,
        'negativo': porcentaje_negativo,
        'neutral': porcentaje_neutral,
        'ejemplos': ejemplos
    }

if __name__ == '__main__':
    tema_busqueda = "inteligencia artificial"
    sitios_noticias = [
        "https://www.ejemplo.com", # Reemplazar con URLs reales
        "https://www.otroejemplo.com"
    ]

    resultados = analizar_sentimiento_noticias(tema_busqueda, sitios_noticias)

    print(f"Análisis de sentimiento para '{tema_busqueda}':")
    print(f"  Positivo: {resultados['positivo']:.2f}%")
    print(f"  Negativo: {resultados['negativo']:.2f}%")
    print(f"  Neutral: {resultados['neutral']:.2f}%")
    print("\nEjemplos:")
    for titulo, sentimiento in resultados['ejemplos']:
        print(f"  - {titulo} ({sentimiento})")


import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

def analizar_sentimiento_noticias(tema, sitios_web):
    """
    Analiza el sentimiento de titulares de noticias sobre un tema específico de varios sitios web.

    Args:
        tema (str): El tema sobre el cual se analizarán las noticias.
        sitios_web (list): Lista de URLs de sitios web de noticias a analizar.

    Returns:
        dict: Un diccionario con el análisis de sentimiento:
              - 'positivo': porcentaje de titulares positivos.
              - 'negativo': porcentaje de titulares negativos.
              - 'neutral': porcentaje de titulares neutrales.
              - 'ejemplos': una lista de tuplas con titulares y su polaridad.
    """

    # ¿Por qué es interesante?:
    titulares = []
    for sitio_web in sitios_web:
        try:
            response = requests.get(sitio_web)
            response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
            soup = BeautifulSoup(response.content, 'html.parser')

            # Ajusta esto según la estructura del HTML de cada sitio web
            for link in soup.find_all('a'):
                titulo = link.get_text()
                if tema.lower() in titulo.lower():
                    titulares.append(titulo)
        except requests.exceptions.RequestException as e:
            print(f"Error al acceder a {sitio_web}: {e}")
        except Exception as e:
            print(f"Error al procesar {sitio_web}: {e}")


    sentimientos = []
    for titulo in titulares:
        analisis = TextBlob(titulo)
        polaridad = analisis.sentiment.polarity
        sentimientos.append(polaridad)

    positivo = sum(1 for s in sentimientos if s > 0.1)
    negativo = sum(1 for s in sentimientos if s < -0.1)
    neutral = sum(1 for s in sentimientos if -0.1 <= s <= 0.1)

    total = len(sentimientos)
    if total > 0:
        porcentaje_positivo = (positivo / total) * 100
        porcentaje_negativo = (negativo / total) * 100
        porcentaje_neutral = (neutral / total) * 100
    else:
        porcentaje_positivo = 0
        porcentaje_negativo = 0
        porcentaje_neutral = 0

    ejemplos = []
    for i, titulo in enumerate(titulares):
         analisis = TextBlob(titulo)
         polaridad = analisis.sentiment.polarity
         if abs(polaridad) > 0.1:
              ejemplos.append((titulo, "Positivo" if polaridad > 0 else "Negativo"))
         elif len(ejemplos) < 5: # Incluye algunos neutrales si hay pocos ejemplos significativos
              ejemplos.append((titulo, "Neutral"))
         if len(ejemplos) >= 5:
              break  # Solo mostrar 5 ejemplos

    return {
        'positivo': porcentaje_positivo,
        'negativo': porcentaje_negativo,
        'neutral': porcentaje_neutral,
        'ejemplos': ejemplos
    }

if __name__ == '__main__':
    tema_busqueda = "inteligencia artificial"
    sitios_noticias = [
        "https://www.ejemplo.com", # Reemplazar con URLs reales
        "https://www.otroejemplo.com"
    ]

    resultados = analizar_sentimiento_noticias(tema_busqueda, sitios_noticias)

    print(f"Análisis de sentimiento para '{tema_busqueda}':")
    print(f"  Positivo: {resultados['positivo']:.2f}%")
    print(f"  Negativo: {resultados['negativo']:.2f}%")
    print(f"  Neutral: {resultados['neutral']:.2f}%")
    print("\nEjemplos:")
    for titulo, sentimiento in resultados['ejemplos']:
        print(f"  - {titulo} ({sentimiento})")