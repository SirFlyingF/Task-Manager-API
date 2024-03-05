from os import getenv


class Config:
    DEBUG = False
    TEST = False
    DB_URL = None
    SECRET_KEY = None


class TestConfig(Config):
    TEST = True
    DB_URL = 'sqlite:///foo.db'
    SECRET_KEY = "=n8_pko2imt&8(g#&-_cg2_2&__^@atx4#mp9zn0n=ufnsq__7"

class DebugConfig(Config):
    DEBUG = True
    DB_URL = 'sqlite:///foo.db'
    SECRET_KEY = "n()5svk5ne1884qc5kz%lnyz7d*f$o@9v(&=#$jpiucxolt7b@"

class ProductionConfig(Config):
    SECRET_KEY = getenv('SECRET_KEY') 

    db_user = getenv('DB_USER')
    db_pass = getenv('DB_PASS')
    db_host = getenv('DB_HOST')
    db_port = getenv('DB_PORT')
    db_name = getenv('DB_NAME')
    
    DB_URL = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'



def get_config(env=None):
    if env is None:
        env = getenv('ENVIRON', default='DEV')

    match env:
        case 'PROD': return ProductionConfig()
        case 'TEST' : return TestConfig()
        case 'DEV' : return DebugConfig()
        case _ : return DebugConfig()