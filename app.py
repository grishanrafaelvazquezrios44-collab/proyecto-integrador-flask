from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave-de-prueba-encuestaflix")

# En Render se puede cambiar DATABASE_PATH desde Environment.
# En Pydroid se guarda dentro de la carpeta del proyecto.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "encuestaflix.db"))

def conectar():
    carpeta = os.path.dirname(DB_PATH)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    return conexion

def crear_tablas():
    conexion = conectar()
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS encuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            calificacion INTEGER NOT NULL,
            opinion TEXT NOT NULL
        )
    """)
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS sugerencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            sugerencia TEXT NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

@app.route("/", methods=["GET"])
def inicio():
    return render_template("index.html")

@app.route("/encuesta", methods=["POST"])
def guardar_encuesta():
    nombre = request.form.get("nombre", "").strip()
    calificacion = request.form.get("calificacion", "").strip()
    opinion = request.form.get("opinion", "").strip()

    if not nombre or not opinion or calificacion not in ["1", "2", "3", "4", "5"]:
        flash("Completa todos los campos de la encuesta correctamente.", "error")
        return redirect(url_for("inicio"))

    conexion = conectar()
    conexion.execute(
        "INSERT INTO encuestas (nombre, calificacion, opinion) VALUES (?, ?, ?)",
        (nombre, int(calificacion), opinion)
    )
    conexion.commit()
    conexion.close()
    flash("¡Tu encuesta se guardó correctamente!", "success")
    return redirect(url_for("inicio"))

@app.route("/sugerencia", methods=["POST"])
def guardar_sugerencia():
    nombre = request.form.get("nombre", "").strip()
    categoria = request.form.get("categoria", "").strip()
    sugerencia = request.form.get("sugerencia", "").strip()

    categorias_validas = ["Servicio", "Diseño", "Contenido", "Otro"]
    if not nombre or not sugerencia or categoria not in categorias_validas:
        flash("Completa todos los campos del buzón correctamente.", "error")
        return redirect(url_for("inicio"))

    conexion = conectar()
    conexion.execute(
        "INSERT INTO sugerencias (nombre, categoria, sugerencia) VALUES (?, ?, ?)",
        (nombre, categoria, sugerencia)
    )
    conexion.commit()
    conexion.close()
    flash("¡Gracias! Tu sugerencia fue guardada.", "success")
    return redirect(url_for("inicio"))

@app.route("/respuestas", methods=["GET"])
def respuestas():
    conexion = conectar()
    encuestas = conexion.execute("SELECT * FROM encuestas ORDER BY id DESC").fetchall()
    sugerencias = conexion.execute("SELECT * FROM sugerencias ORDER BY id DESC").fetchall()
    conexion.close()
    return render_template("respuestas.html", encuestas=encuestas, sugerencias=sugerencias)

crear_tablas()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
