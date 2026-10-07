import sqlite3
from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    rol TEXT NOT NULL DEFAULT 'cliente'
);

CREATE TABLE IF NOT EXISTS oferentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER REFERENCES usuarios(id),
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    tarifa INTEGER NOT NULL,
    distancia_km REAL NOT NULL,
    calificacion REAL NOT NULL DEFAULT 0,
    anios_experiencia INTEGER NOT NULL DEFAULT 0,
    servicios_completados INTEGER NOT NULL DEFAULT 0,
    verificado INTEGER NOT NULL DEFAULT 0,
    foto TEXT
);

CREATE TABLE IF NOT EXISTS mensajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    oferente_id INTEGER NOT NULL REFERENCES oferentes(id),
    emisor TEXT NOT NULL,            -- 'cliente' u 'oferente'
    texto TEXT NOT NULL,
    creado TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS resenas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    oferente_id INTEGER NOT NULL REFERENCES oferentes(id),
    estrellas INTEGER NOT NULL CHECK (estrellas BETWEEN 1 AND 5),
    comentario TEXT NOT NULL,
    creado TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

OFERENTES_INICIALES = [
    ("Ana Martinez", "ninos",
     "Cuido niños con experiencia de 5 años. Certificada en primeros auxilios pediátricos. Horarios flexibles.",
     20, 0.5, 5.0, 5, 52, 1, "ana.jpg"),
    ("Carlos Rodriguez", "mascotas",
     "Paseos personalizados según necesidades de tu mascota. Áreas verdes cercanas. Servicio de guardería canina.",
     10, 3, 5.0, 3, 110, 1, "carlos.jpg"),
    ("Luisa González", "limpieza",
     "Ofrezco limpieza residencial y de oficinas, utilizando siempre productos ecológicos que cuidan tanto de tu salud como del medio ambiente.",
     25, 1, 5.0, 4, 14, 1, "luisa.jpg"),
    ("Mateo Herrera", "tecnologia",
     "Reparación de computadores, redes domésticas e instalación de software. Atención a domicilio.",
     30, 2.2, 4.7, 6, 38, 1, None),
    ("Sofía Ramírez", "clases",
     "Clases particulares de matemáticas y física para bachillerato y primeros semestres universitarios.",
     18, 1.8, 4.8, 4, 27, 0, None),
    ("Doña Marta Gil", "comida",
     "Almuerzos caseros tradicionales del Tolima con entrega a domicilio. Pedidos por la mañana.",
     12, 2.5, 4.9, 8, 63, 1, None),
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(SCHEMA)
    if db.execute("SELECT COUNT(*) FROM oferentes").fetchone()[0] == 0:
        db.executemany(
            """INSERT INTO oferentes (nombre, categoria, descripcion, tarifa, distancia_km,
               calificacion, anios_experiencia, servicios_completados, verificado, foto)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            OFERENTES_INICIALES,
        )
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
