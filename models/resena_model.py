import re
from database import get_db
from models.oferente_model import OferenteModel

# RN-04: filtro básico de lenguaje ofensivo
PALABRAS_BLOQUEADAS = ["idiota", "estupido", "estúpido", "imbecil", "imbécil", "basura", "maldito"]


class ResenaModel:
    @staticmethod
    def contiene_ofensas(texto):
        t = texto.lower()
        return any(re.search(r"\b" + re.escape(p) + r"\b", t) for p in PALABRAS_BLOQUEADAS)

    @staticmethod
    def listar(oferente_id):
        return get_db().execute(
            """SELECT r.*, u.nombre AS autor FROM resenas r
               JOIN usuarios u ON u.id = r.usuario_id
               WHERE r.oferente_id = ? ORDER BY r.id DESC""",
            (oferente_id,),
        ).fetchall()

    @staticmethod
    def crear(usuario_id, oferente_id, estrellas, comentario):
        db = get_db()
        db.execute(
            "INSERT INTO resenas (usuario_id, oferente_id, estrellas, comentario) VALUES (?,?,?,?)",
            (usuario_id, oferente_id, estrellas, comentario),
        )
        db.commit()
        OferenteModel.recalcular_calificacion(oferente_id)
