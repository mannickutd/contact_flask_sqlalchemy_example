from functools import wraps
from contact_flask_sqlalchemy_example import db



def transactional(func):
    @wraps(func)
    def commit_or_rollback(*args, **kwargs):
        from flask import current_app
        try:
            res = func(*args, **kwargs)
            db.session.commit()
            return res
        except Exception as e:
            current_app.logger.error("Unable to perform transactional actions", exc_info=True)
            db.session.rollback()
            raise
    return commit_or_rollback


def transaction_rollback():
    db.session.rollback()


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
