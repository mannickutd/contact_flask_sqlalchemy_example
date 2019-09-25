import json
from flask import (request, abort, jsonify)
from werkzeug.exceptions import (BadRequest, NotFound)
from marshmallow import fields
from contact_flask_sqlalchemy_example import ma
from contact_flask_sqlalchemy_example.models import (Contact, EmailAddress)
from contact_flask_sqlalchemy_example.models.contact_op import (
    create_contact_op,
    get_contacts_op,
    get_contact_op,
    update_contact_op,
    delete_contact_op,
)


class EmailAddressSchema(ma.ModelSchema):
    class Meta:
        model = EmailAddress

class ContactSchema(ma.ModelSchema):
    class Meta:
        model = Contact

    email_addresses = fields.Nested(EmailAddressSchema, many=True)


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)


def contacts() -> dict:
    username = request.args.get('username', None)
    return jsonify(contacts_schema.dump(get_contacts_op(username=username)))


def create_contact() -> dict:
    request_json = json.loads(request.get_data(as_text=True))
    errors = contact_schema.validate(request_json)
    if errors:
        abort(BadRequest, str(errors))
    contact = create_contact_op(request_json['username'],
                                request_json['first_name'],
                                request_json['last_name']
    )
    return jsonify(contact_schema.dump(contact))


def update_contact(contact_id: int) -> dict:
    try:
        contact = get_contact_op(contact_id)
    except:
        abort(NotFound, 'Contact not found')
    request_json = json.loads(request.get_data(as_text=True))
    errors = contact_schema.validate(request_json)
    if errors:
        abort(BadRequest, str(errors))
    update_contact_op(contact_id,
                      request_json['username'],
                      request_json['first_name'],
                      request_json['last_name']
    ) 
    return jsonify(contact_schema.dump(get_contact_op(contact_id)))


def delete_contact(contact_id: int) -> dict:
    try:
        contact = get_contact_op(contact_id)
    except:
        abort(NotFound, 'Contact not found')
    delete_contact_op(contact_id)
    return jsonify({})
