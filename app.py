
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "cineflix_clave_123"

def conectar():
    conexion = sqlite3.connect("cineflix.db")
    return conexion

def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            pelicula TEXT,
            fecha TEXT,
            horario TEXT,
            boletos INTEGER,
            sala TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS encuestas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            calificacion TEXT,
            opinion TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sugerencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            categoria TEXT,
            sugerencia TEXT
        )
    """)

    conexion.commit()
    conexion.close()


crear_tablas()


@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/cineflix", methods=["GET", "POST"])
def cineflix():
    if request.method == "POST":
        datos = (
            request.form["nombre"],
            request.form["pelicula"],
            request.form["fecha"],
            request.form["horario"],
            request.form["boletos"],
            request.form["sala"]
        )

        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO reservaciones
            (nombre, pelicula, fecha, horario, boletos, sala)
            VALUES (?, ?, ?, ?, ?, ?)
        """, datos)
        conexion.commit()
        conexion.close()

        flash("Reservación registrada correctamente.")
        return redirect(url_for("cineflix"))

    return render_template("cineflix.html")


@app.route("/cineflix/respuestas")
def respuestas_cineflix():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM reservaciones")
    filas = cursor.fetchall()
    conexion.close()

    headers = ["ID", "Nombre", "Película", "Fecha", "Horario", "Boletos", "Sala"]

    return render_template(
        "tabla.html",
        titulo="Reservaciones",
        headers=headers,
        rows=filas,
        back="/cineflix"
    )


@app.route("/formulario1", methods=["GET", "POST"])
def formulario1():
    if request.method == "POST":
        datos = (
            request.form["nombre"],
            request.form["calificacion"],
            request.form["opinion"]
        )

        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO encuestas (nombre, calificacion, opinion)
            VALUES (?, ?, ?)
        """, datos)
        conexion.commit()
        conexion.close()

        flash("Encuesta enviada correctamente.")
        return redirect(url_for("formulario1"))

    return render_template("formulario1.html")


@app.route("/formulario1/respuestas")
def respuestas_formulario1():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM encuestas")
    filas = cursor.fetchall()
    conexion.close()

    headers = ["ID", "Nombre", "Calificación", "Opinión"]

    return render_template(
        "tabla.html",
        titulo="Encuestas de satisfacción",
        headers=headers,
        rows=filas,
        back="/formulario1"
    )


@app.route("/formulario2", methods=["GET", "POST"])
def formulario2():
    if request.method == "POST":
        datos = (
            request.form["nombre"],
            request.form["categoria"],
            request.form["sugerencia"]
        )

        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO sugerencias (nombre, categoria, sugerencia)
            VALUES (?, ?, ?)
        """, datos)
        conexion.commit()
        conexion.close()

        flash("Sugerencia enviada correctamente.")
        return redirect(url_for("formulario2"))

    return render_template("formulario2.html")


@app.route("/formulario2/respuestas")
def respuestas_formulario2():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM sugerencias")
    filas = cursor.fetchall()
    conexion.close()

    headers = ["ID", "Nombre", "Categoría", "Sugerencia"]

    return render_template(
        "tabla.html",
        titulo="Buzón de sugerencias",
        headers=headers,
        rows=filas,
        back="/formulario2"
    )


if __name__ == "__main__":
    app.run(debug=True)
           
