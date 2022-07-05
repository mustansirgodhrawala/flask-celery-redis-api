import os

from flask import Flask
from celery import Celery
from flask_caching import Cache
from celery import Celery

cache = Cache()

celery = Celery(__name__,)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

def create_app(script_info=None):

    # instantiate the app
    app = Flask(
        __name__,
    )

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    if app_settings:
        app.config.from_object(app_settings)
    else:
        app.config.from_object('project.config.config.local_config')

    # API Blueprint Register
    from project.server.views import api_blueprint
    app.register_blueprint(api_blueprint)
    cache.init_app(app)


    # shell context for flask cli
    app.shell_context_processor({"app": app})

    return app