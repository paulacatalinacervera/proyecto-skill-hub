from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db


class UsuarioModel:
    @staticmethod
    def crear(nombre, email, password, rol="cliente"):
        db = get_db()
        cur = db.execute(
            "INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES (?,?,?,?)",
            (nombre, email.lower(), generate_password_hash(password), rol),
        )
        db.commit()
        return cur.lastrowid

    @staticmethod
    def por_email(email):
        return get_db().execute(
            "SELECT * FROM usuarios WHERE email = ?", (email.lower(),)
        ).fetchone()

    @staticmethod
    def por_id(usuario_id):
        return get_db().execute(
            "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()

    @staticmethod
    def autenticar(email, password):
        u = UsuarioModel.por_email(email)
        if u and check_password_hash(u["password_hash"], password):
            return u
        return None
