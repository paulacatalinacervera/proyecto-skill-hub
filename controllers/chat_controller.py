from flask import Blueprint, abort, g, jsonify, render_template, request
from controllers.utils import login_requerido
from models.mensaje_model import MensajeModel
from models.oferente_model import OferenteModel

bp = Blueprint("chat", __name__, url_prefix="/chat")


def _oferente_o_404(oferente_id):
    o = OferenteModel.obtener(oferente_id)
    if o is None:
        abort(404)
    return o


@bp.route("/<int:oferente_id>")
@login_requerido
def sala(oferente_id):
    return render_template("chat.html", o=_oferente_o_404(oferente_id))


@bp.route("/<int:oferente_id>/mensajes")
@login_requerido
def mensajes(oferente_id):
    _oferente_o_404(oferente_id)
    desde = request.args.get("desde", 0, type=int)
    filas = MensajeModel.listar(g.usuario["id"], oferente_id, desde)
    return jsonify([dict(f) for f in filas])


@bp.route("/<int:oferente_id>/enviar", methods=["POST"])
@login_requerido
def enviar(oferente_id):
    o = _oferente_o_404(oferente_id)
    texto = (request.get_json(silent=True) or {}).get("texto", "").strip()
    if not texto or len(texto) > 500:
        return jsonify(error="Mensaje vacío o demasiado largo"), 400
    primero = not MensajeModel.hay_interaccion(g.usuario["id"], oferente_id)
    MensajeModel.crear(g.usuario["id"], oferente_id, "cliente", texto)
    # Perfiles de demostración (sin cuenta propia) responden automáticamente
    if o["usuario_id"] is None and primero:
        MensajeModel.crear(
            g.usuario["id"], oferente_id, "oferente",
            f"¡Hola! Soy {o['nombre'].split()[0]}. Gracias por escribirme, cuéntame qué necesitas, "
            "para qué fecha y te envío una propuesta. (Respuesta automática de demostración)",
        )
    return jsonify(ok=True)
