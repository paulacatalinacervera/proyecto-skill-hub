from database import get_db


class MensajeModel:
    @staticmethod
    def listar(usuario_id, oferente_id, desde_id=0):
        return get_db().execute(
            """SELECT id, emisor, texto, creado FROM mensajes
               WHERE usuario_id = ? AND oferente_id = ? AND id > ? ORDER BY id""",
            (usuario_id, oferente_id, desde_id),
        ).fetchall()

    @staticmethod
    def crear(usuario_id, oferente_id, emisor, texto):
        db = get_db()
        db.execute(
            "INSERT INTO mensajes (usuario_id, oferente_id, emisor, texto) VALUES (?,?,?,?)",
            (usuario_id, oferente_id, emisor, texto),
        )
        db.commit()

    @staticmethod
    def hay_interaccion(usuario_id, oferente_id):
        return get_db().execute(
            "SELECT 1 FROM mensajes WHERE usuario_id = ? AND oferente_id = ? LIMIT 1",
            (usuario_id, oferente_id),
        ).fetchone() is not None
