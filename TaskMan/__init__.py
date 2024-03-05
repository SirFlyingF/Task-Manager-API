from flask import Flask
from config import get_config
from .Database.database import database, init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    database.init_session(app)

    # Spin up a new empty DB for tests
    if app.config['INIT_DB']:
        init_db()

    from . import utils
    from .TaskAPI.routes import tasks
    from .AuthAPI.routes import auth
    app.register_blueprint(tasks, url_prefix='/tasks')
    app.register_blueprint(auth, url_prefix='/auth')

    return app

app = create_app()
