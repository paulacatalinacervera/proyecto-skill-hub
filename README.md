# SkillHub (Flask + Bootstrap, patrón MVC)

## Ejecutar
```bash
python -m venv venv
venv\Scripts\activate        # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python app.py
```
Abre http://127.0.0.1:5000 (necesita internet para cargar Bootstrap y la fuente Poppins por CDN).
La base de datos `skillhub.db` (SQLite) se crea sola con 6 perfiles de ejemplo.

## Estructura MVC
- **Modelo** `models/`: acceso a datos y reglas de negocio (usuarios, oferentes, mensajes, reseñas, medallas).
- **Vista** `views/templates/` + `static/`: plantillas Jinja2, Bootstrap, CSS y JS.
- **Controlador** `controllers/`: rutas Flask (`main`, `auth`, `chat`) que conectan modelo y vista.

## Funciones
Búsqueda en vivo y filtros por categoría/calificación/orden (RF-04, RF-05) · registro e inicio de sesión
con contraseña cifrada (RF-01) · perfil con medallas por 10/50/100 servicios (RF-07, RN-02) ·
chat (RF-06) · reseñas solo tras chatear (RF-08, RN-03) con filtro de lenguaje ofensivo (RN-04).

## Notas
- Los perfiles de ejemplo responden con un mensaje automático de demostración la primera vez que les escribes.
- Las contraseñas usan el hash de Werkzeug (scrypt/pbkdf2); el manual menciona Bcrypt, se puede cambiar con `flask-bcrypt`.
- Pendiente (del manual): panel de administración y carga de diplomas (RF-03, RF-09), denuncias (RF-10).
- Antes de desplegar, define la variable de entorno `SKILLHUB_SECRET`.
