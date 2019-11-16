import os

class Config(object):
    """
    Common configurations
    """


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    MONGO_URI = "mongodb://localhost:27017/junction"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://avnadmin:pzhzdsl1qwd67r7v@mysql-sk5-mymail-0739.aivencloud.com:11180/skincaredb'
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://favebook_admin:password@localhost/50043db'

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'p9Bv<3Eid9%$i01'
    MONGO_URI = "mongodb://localhost:27017/junction"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://avnadmin:pzhzdsl1qwd67r7v@mysql-sk5-mymail-0739.aivencloud.com:11180/skincaredb'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}