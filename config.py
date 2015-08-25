from __future__ import absolute_import
from __future__ import unicode_literals


class Config(object):
    DEBUG = False
    TESTING = False

    # Define the application directory
    import os
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Log file (the directory must exist)
    APPLICATION_LOG = os.path.join(BASE_DIR, 'log', 'application.log')
    ACCESS_LOG = os.path.join(BASE_DIR, 'log', 'access.log')

    # Secret key for flask sessions and CSRF protection
    SECRET_KEY = "secret key that you need to change, seriously!"


class ProductionConfig(Config):
    REDIS_HOST="127.0.0.1"
    REDIS_PORT=6379
    REDIS_DB=0


class DevelopmentConfig(Config):
    REDIS_HOST="127.0.0.1"
    REDIS_PORT=6379
    REDIS_DB=5
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


# Default configuration
default = DevelopmentConfig
