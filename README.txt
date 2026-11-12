Proyecto Integrador Flask + SQLite
Tres enlaces en una sola aplicación:
 /cineflix
 /formulario1
 /formulario2
La página inicial / muestra los tres enlaces.

Pydroid 3:
1. Extrae el ZIP.
2. En la terminal instala: pip install flask
3. Abre app.py en Pydroid y ejecútalo.
4. En el navegador abre http://127.0.0.1:5000

Render:
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app

Aviso: el almacenamiento gratuito de Render es efímero. SQLite puede perder los datos al reiniciar o volver a desplegar. Para conservar datos se requiere disco persistente y configurar DATABASE_PATH.
