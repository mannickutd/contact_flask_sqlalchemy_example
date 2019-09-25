from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


db = SQLAlchemy()
ma = Marshmallow()


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


def create_app(app_name=None):
    if app_name is None:
        app_name = __name__
    application = Flask(app_name)
    from config import Config
    application.config.from_object(Config)
    db.init_app(application)
    ma.init_app(application)
    # Make sure to include the models.
    from contact_flask_sqlalchemy_example import models
    # Make sure to add url rules
    _add_urls(application)
    return application
