import os
basedir =  os.path.abspath(os.path.dirname(__file__ ))

class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO=True
    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS=True

class ProductionConfig(Config):
    DEBUG=False
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SECRET_KEY=os.getenv('SECRET_KEY')

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

