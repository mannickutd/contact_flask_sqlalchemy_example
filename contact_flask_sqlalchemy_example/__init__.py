from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from celery import Celery
from config import Config
 

db = SQLAlchemy()
ma = Marshmallow()
celery = Celery(
    __name__,
    backend=Config.CELERY_RESULT_BACKEND,
    broker=Config.CELERY_BROKER_URL,
)


def _add_urls(app):
    from contact_flask_sqlalchemy_example import contact_rest
    app.add_url_rule('/contact',
                     'contacts',
                     contact_rest.contacts,
                     methods=['GET'],
    )
    app.add_url_rule('/contact',
                     'create_contact',
                     contact_rest.create_contact,
                     methods=['POST'],
    )
    app.add_url_rule('/contact/<contact_id>',
                     'update_contact',
                     contact_rest.update_contact,
                     methods=['PUT'],
    )
    app.add_url_rule('/contact/<contact_id>',
                     'delete_contact',
                     contact_rest.delete_contact,
                     methods=['DELETE'],
    )


def init_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


def create_app(app_name=None):
    if app_name is None:
        app_name = __name__
    application = Flask(app_name)
    application.config.from_object(Config)
    db.init_app(application)
    ma.init_app(application)
    # Make sure to include the models.
    from contact_flask_sqlalchemy_example import models
    # Make sure to add url rules
    _add_urls(application)
    # Make sure to update celery
    celery.conf.update(application.config)
    from contact_flask_sqlalchemy_example import celery_task
    return application
