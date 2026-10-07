from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)
from controllers.utils import login_requerido
from models.mensaje_model import MensajeModel
from models.oferente_model import CATEGORIAS, ORDENES, OferenteModel
from models.resena_model import ResenaModel

bp = Blueprint("main", __name__)


def _filtros():
    try:
        min_est = float(request.args.get("min_estrellas", 0))
    except ValueError:
        min_est = 0
    return dict(
        q=request.args.get("q", "").strip(),
        categoria=request.args.get("categoria", ""),
        orden=request.args.get("orden", "recomendados"),
        min_estrellas=min_est,
    )


@bp.route("/")
def index():
    oferentes = OferenteModel.buscar(**_filtros())
    return render_template("index.html", oferentes=oferentes,
                           categorias=CATEGORIAS, ordenes=list(ORDENES))


@bp.route("/buscar")
def buscar():
    """Devuelve solo las tarjetas (HTML parcial) para actualizar sin recargar."""
    oferentes = OferenteModel.buscar(**_filtros())
    return render_template("_tarjetas.html", oferentes=oferentes)


@bp.route("/perfil/<int:oferente_id>")
def perfil(oferente_id):
    o = OferenteModel.obtener(oferente_id)
    if o is None:
        abort(404)
    puede_resenar = bool(g.usuario) and MensajeModel.hay_interaccion(g.usuario["id"], oferente_id)
    return render_template(
        "perfil.html", o=o, categorias=CATEGORIAS,
        medallas=OferenteModel.medallas(o["servicios_completados"]),
        resenas=ResenaModel.listar(oferente_id), puede_resenar=puede_resenar,
    )


@bp.route("/perfil/<int:oferente_id>/resena", methods=["POST"])
@login_requerido
def resenar(oferente_id):
    if OferenteModel.obtener(oferente_id) is None:
        abort(404)
    # RN-03: solo si hubo interacción previa en el chat
    if not MensajeModel.hay_interaccion(g.usuario["id"], oferente_id):
        flash("Solo puedes reseñar a quien hayas contactado por el chat.", "warning")
        return redirect(url_for("main.perfil", oferente_id=oferente_id))
    comentario = request.form.get("comentario", "").strip()
    try:
        estrellas = int(request.form.get("estrellas", 0))
    except ValueError:
        estrellas = 0
    if not 1 <= estrellas <= 5 or not comentario:
        flash("Elige de 1 a 5 estrellas y escribe un comentario.", "danger")
    elif ResenaModel.contiene_ofensas(comentario):  # RN-04
        flash("Tu comentario contiene lenguaje no permitido.", "danger")
    else:
        ResenaModel.crear(g.usuario["id"], oferente_id, estrellas, comentario)
        flash("¡Gracias por tu reseña!", "success")
    return redirect(url_for("main.perfil", oferente_id=oferente_id))
