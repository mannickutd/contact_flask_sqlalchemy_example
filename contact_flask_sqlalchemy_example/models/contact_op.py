from contact_flask_sqlalchemy_example import db
from contact_flask_sqlalchemy_example.models import (Contact, transactional)


def create_contact_op(username: str, first_name: str, last_name: str) -> Contact:
    contact = Contact(username=username, first_name=first_name, last_name=last_name)
    db.session.add(contact)
    db.session.commit()
    return contact


def get_contact_op(id_: int):
    return Contact.query.filter_by(id=id_).one()


@transactional
def update_contact_op(id_: int, username: str, first_name: str, last_name: str) -> Contact:
    db.session.query(Contact)\
        .filter(Contact.id == id_)\
        .update({'username': username, 'first_name': first_name, 'last_name': last_name})


def get_contacts_op(username=None):
    query = Contact.query
    if username:
        query = query.filter_by(username=username)
    return query.all()


@transactional
def delete_contact_op(id_):
    Contact.query.filter_by(id=id_).delete()

