from __future__ import absolute_import
from __future__ import unicode_literals

import os

# Import flask and template operators
from flask import Flask, render_template, request
import redis

# Define the WSGI application object
app = Flask(__name__)

# Configurations
if os.environ.get('SHARESCAN_CONFIG'):
    app.config.from_object('config.%s' % os.environ.get('SHARESCAN_CONFIG'))
else:
    app.config.from_object('config.DevelopmentConfig')

# Define the database object which is imported
# by modules and controllers
# HERE BE REDIS
db = redis.StrictRedis(
    host=app.config.get('REDIS_HOST'),
    port=app.config.get('REDIS_PORT'),
    db=app.config.get('REDIS_DB'),
)

# Rest API
from .restful import Api
api = Api(app)

# Configure logging
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter

# Configure the application log
if app.config.get('APPLICATION_LOG', None):
    application_log_handler = TimedRotatingFileHandler(app.config.get('APPLICATION_LOG'), 'd', 7)
    application_log_handler.setLevel(logging.INFO)
    application_log_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(application_log_handler)


# Configure the access log if defined in the configuration
if app.config.get('ACCESS_LOG', None):
    access_log = logging.getLogger('access_log')
    access_log_handler = TimedRotatingFileHandler(app.config.get('ACCESS_LOG'), 'd', 7)
    access_log_handler.setLevel(logging.INFO)
    access_log_handler.setFormatter(Formatter('%(asctime)s   %(message)s'))
    access_log.addHandler(access_log_handler)

    @app.before_request
    def pre_request_logging():
        # Log except when testing
        if not app.config.get('TESTING'):
            access_log.info('\t'.join([
                request.remote_addr,
                request.method,
                request.url,
                str(request.data)])
            )


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/', endpoint='index')
def index():
    return render_template('home.html'), 200

# Import modules
from app.ips import views as ips_views
from app.results import views as results_views
