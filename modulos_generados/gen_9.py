# ```python
# Idea: Servidor web simple que sirve archivos estáticos y responde a una API básica.

import http.server
import socketserver
import json

# Configuración
PORT = 8000
DIRECTORY = "public"  # Carpeta donde se guardan los archivos estáticos

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Manejo de la API (ejemplo: /api/data)
        if self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {"message": "Hola desde la API!", "status": "ok"}
            self.wfile.write(json.dumps(data).encode())
        else:
            # Servir archivos estáticos desde el directorio configurado
            super().do_GET()


# Iniciar el servidor
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Servidor corriendo en el puerto {PORT}, sirviendo desde '{DIRECTORY}'")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
```

**Explicación de la idea:**

1. **Importaciones:**  Importa los módulos necesarios para crear un servidor HTTP básico y manejar JSON.
2. **Configuración:** Define el puerto en el que el servidor escuchará y el directorio desde el cual se servirán los archivos estáticos (HTML, CSS, JavaScript, imágenes, etc.).
3. **Clase `RequestHandler`:**  Esta clase extiende `http.server.SimpleHTTPRequestHandler` para personalizar el comportamiento del servidor.
   - **`do_GET`:**  Sobreescribe el método `do_GET` para manejar las solicitudes GET.
     - **Manejo de la API:** Si la ruta solicitada es `/api/data` (o cualquier otra ruta de API que definas), el servidor responderá con datos JSON.  En este ejemplo, envía un mensaje simple.
     - **Servir archivos estáticos:** Si la ruta no coincide con una ruta de API, llama a `super().do_GET()` para que la clase base se encargue de servir los archivos estáticos desde el directorio configurado.
4. **Iniciar el servidor:**
   - Crea un objeto `socketserver.TCPServer` para escuchar en el puerto especificado y usar la clase `RequestHandler` para manejar las solicitudes.
   - Inicia el servidor con `httpd.serve_forever()`.
   - Captura la excepción `KeyboardInterrupt` (Ctrl+C) para detener el servidor de forma limpia.

**Cómo usarlo:**

1. **Guarda el script:** Guarda el código como un archivo Python (por ejemplo, `server.py`).
2. **Crea un directorio `public`:** Crea una carpeta llamada `public` en el mismo directorio que el script.  Coloca tus archivos estáticos (HTML, CSS, JavaScript, imágenes) dentro de esta carpeta.
3. **Ejecuta el script:**  Abre una terminal o línea de comandos y ejecuta `python server.py`.
4. **Accede al servidor:**  Abre un navegador web y ve a `http://localhost:8000/` para ver los archivos estáticos.  Ve a `http://localhost:8000/api/data` para ver la respuesta de la API.

**Mejoras:**

* **Manejo de errores:**  Añade manejo de errores más robusto (por ejemplo, para archivos no encontrados).
* **Rutas más complejas:**  Implementa rutas de API más complejas con parámetros.
* **Métodos HTTP:**  Soporta otros métodos HTTP como POST, PUT, DELETE.
* **Framework web:**  Para aplicaciones más grandes, considera usar un framework web como Flask o Django.
* **Seguridad:**  En un entorno de producción, asegúrate de implementar medidas de seguridad adecuadas (HTTPS, validación de entrada, etc.). (FIXED)
# Idea: Servidor web simple que sirve archivos estáticos y responde a una API básica.

import http.server
import socketserver
import json
import os

# Configuración
PORT = 8000
DIRECTORY = "public"  # Carpeta donde se guardan los archivos estáticos

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Manejo de la API (ejemplo: /api/data)
        if self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {"message": "Hola desde la API!", "status": "ok"}
            self.wfile.write(json.dumps(data).encode())
        elif self.path == "/api/items":
            self.handle_items_api()
        else:
            # Servir archivos estáticos desde el directorio configurado
            # Check if the requested file exists before attempting to serve it
            filepath = os.path.join(DIRECTORY, self.path[1:]) # Remove leading /
            if os.path.exists(filepath) or self.path == "/":  #Handle root path
                super().do_GET()
            else:
                self.send_error(404, "File not found")

    def handle_items_api(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        items = [
            {"id": 1, "name": "Item 1", "price": 10.99},
            {"id": 2, "name": "Item 2", "price": 20.50},
            {"id": 3, "name": "Item 3", "price": 5.75}
        ]
        self.wfile.write(json.dumps(items).encode())


# Iniciar el servidor
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Servidor corriendo en el puerto {PORT}, sirviendo desde '{DIRECTORY}'")
    try:
        # Create the 'public' directory if it doesn't exist
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)
            print(f"Directorio '{DIRECTORY}' creado.")

        #Create a default index.html if it doesn't exist
        index_path = os.path.join(DIRECTORY, "index.html")
        if not os.path.exists(index_path):
            with open(index_path, "w") as f:
                f.write("<h1>¡Hola desde el servidor web!</h1>")
            print("index.html creado")

        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")