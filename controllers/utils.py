from functools import wraps
from flask import flash, g, redirect, request, session, url_for
from models.usuario_model import UsuarioModel


def cargar_usuario():
    uid = session.get("usuario_id")
    g.usuario = UsuarioModel.por_id(uid) if uid else None


def login_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if g.get("usuario") is None:
            flash("Inicia sesión para continuar.", "warning")
            return redirect(url_for("auth.login", siguiente=request.path))
        return vista(*args, **kwargs)
    return envoltura
