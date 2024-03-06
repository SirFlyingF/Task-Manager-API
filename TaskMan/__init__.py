from flask import Flask
from config import get_config
from .Database.database import database


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    database.init_session(app)

    # utils need to be imported before blueprints
    # routes to avoid a circular import
    from . import utils
    
    from .TaskAPI.routes import tasks
    from .AuthAPI.routes import auth
    app.register_blueprint(tasks, url_prefix='/tasks')
    app.register_blueprint(auth, url_prefix='/auth')

    return app

app = create_app()
