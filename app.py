from flask import Flask, g, render_template
import database
from config import Config
from controllers import auth_controller, chat_controller, main_controller
from controllers.utils import cargar_usuario
from models.oferente_model import CATEGORIAS


def create_app():
    app = Flask(__name__, template_folder=Config.TEMPLATES_FOLDER,
                static_folder=Config.STATIC_FOLDER)
    app.config.from_object(Config)
    database.init_app(app)

    app.before_request(cargar_usuario)
    app.register_blueprint(main_controller.bp)
    app.register_blueprint(auth_controller.bp)
    app.register_blueprint(chat_controller.bp)

    @app.context_processor
    def globales():
        return {"usuario": g.get("usuario"), "NOMBRES_CATEGORIA": CATEGORIAS}

    @app.errorhandler(404)
    def no_encontrado(_):
        return render_template("404.html"), 404

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
