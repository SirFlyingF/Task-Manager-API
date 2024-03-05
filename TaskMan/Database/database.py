from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class DataBase:
    def __init__(self):
        self.session = self.Base = self.engine = None


    def init_session(self, app):
        self.engine = create_engine(app.config['DB_URL'])
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                autoflush=False,
                                                bind=self.engine))
        
        self.Base = declarative_base()
        self.Base.query = self.session.query_property()

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            self.session.remove() 


database = DataBase()

# Do not call unless creating new DB from scratch
def init_db():
    from . import models
    database.Base.metadata.create_all(bind=database.engine)


    