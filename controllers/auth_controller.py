import re
from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from models.usuario_model import UsuarioModel

bp = Blueprint("auth", __name__)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _destino_seguro(ruta):
    return ruta if ruta and ruta.startswith("/") and not ruta.startswith("//") else url_for("main.index")


@bp.route("/login", methods=["GET", "POST"])
def login():
    siguiente = request.values.get("siguiente", "")
    if request.method == "POST":
        u = UsuarioModel.autenticar(request.form.get("email", ""), request.form.get("password", ""))
        if u:
            session.clear()
            session["usuario_id"] = u["id"]
            return redirect(_destino_seguro(siguiente))
        flash("Correo o contraseña incorrectos.", "danger")
    return render_template("login.html", siguiente=siguiente)


@bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        rol = request.form.get("rol", "cliente")
        if rol not in ("cliente", "postulante"):
            rol = "cliente"
        if not nombre or not EMAIL_RE.match(email):
            flash("Escribe tu nombre y un correo válido.", "danger")
        elif len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "danger")
        elif UsuarioModel.por_email(email):
            flash("Ese correo ya está registrado.", "danger")
        else:
            session.clear()
            session["usuario_id"] = UsuarioModel.crear(nombre, email, password, rol)
            flash("¡Cuenta creada! Bienvenido a SkillHub.", "success")
            return redirect(url_for("main.index"))
    return render_template("registro.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))
