import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SKILLHUB_SECRET", "cambia-esta-clave-en-produccion")
    DATABASE = os.path.join(BASE_DIR, "skillhub.db")
    TEMPLATES_FOLDER = os.path.join(BASE_DIR, "views", "templates")
    STATIC_FOLDER = os.path.join(BASE_DIR, "static")
