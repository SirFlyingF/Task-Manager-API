from flask import Flask
from config import get_config
from .Database.database import database


def create_app(env=None):
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    database.init_session(app)

    from . import utils
    from .TaskAPI.routes import tasks
    from .AuthAPI.routes import auth
    app.register_blueprint(tasks, url_prefix='/tasks')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
