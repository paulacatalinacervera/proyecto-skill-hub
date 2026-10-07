from database import get_db

CATEGORIAS = {
    "ninos": "Cuidado de niños",
    "mascotas": "Paseo de mascotas",
    "limpieza": "Limpieza",
    "comida": "Comida a domicilio",
    "tecnologia": "Tecnología",
    "clases": "Clases particulares",
}

# RN-02: medallas automáticas por servicios completados
MEDALLAS = [(100, "Oro", "100 servicios"), (50, "Plata", "50 servicios"), (10, "Bronce", "10 servicios")]

ORDENES = {
    "recomendados": "verificado DESC, calificacion DESC, servicios_completados DESC",
    "calificacion": "calificacion DESC",
    "cercania": "distancia_km ASC",
    "precio": "tarifa ASC",
    "experiencia": "anios_experiencia DESC",
}


class OferenteModel:
    @staticmethod
    def buscar(q="", categoria="", orden="recomendados", min_estrellas=0):
        sql = "SELECT * FROM oferentes WHERE calificacion >= ?"
        params = [min_estrellas]
        if categoria in CATEGORIAS:
            sql += " AND categoria = ?"
            params.append(categoria)
        if q:
            like = f"%{q}%"
            etiquetas = [k for k, v in CATEGORIAS.items() if q.lower() in v.lower()]
            sql += " AND (nombre LIKE ? OR descripcion LIKE ? OR categoria IN (%s))" % (
                ",".join("?" * len(etiquetas)) or "NULL"
            )
            params += [like, like] + etiquetas
        sql += " ORDER BY " + ORDENES.get(orden, ORDENES["recomendados"])
        return get_db().execute(sql, params).fetchall()

    @staticmethod
    def obtener(oferente_id):
        return get_db().execute(
            "SELECT * FROM oferentes WHERE id = ?", (oferente_id,)
        ).fetchone()

    @staticmethod
    def medallas(servicios):
        return [{"nivel": n, "detalle": d} for minimo, n, d in MEDALLAS if servicios >= minimo]

    @staticmethod
    def recalcular_calificacion(oferente_id):
        db = get_db()
        prom = db.execute(
            "SELECT AVG(estrellas) FROM resenas WHERE oferente_id = ?", (oferente_id,)
        ).fetchone()[0]
        if prom is not None:
            db.execute(
                "UPDATE oferentes SET calificacion = ? WHERE id = ?",
                (round(prom, 1), oferente_id),
            )
            db.commit()
