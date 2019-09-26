import json


def test_contacts(flask_app, db_sess, sample_contact):
    with flask_app.test_request_context():
        with flask_app.test_client() as client:
            resp = client.get('/contact')
            assert resp.status_code == 200
            json_resp = json.loads(resp.get_data(as_text=True))
            assert len(json_resp) == 1
            assert json_resp[0]['username'] == sample_contact.username


def test_contacts(flask_app,
                  db_sess,
                  sample_contact_with_email_addresses,
                  sample_email_address
):
    with flask_app.test_request_context():
        with flask_app.test_client() as client:
            resp = client.get('/contact')
            assert resp.status_code == 200
            json_resp = json.loads(resp.get_data(as_text=True))
            assert len(json_resp) == 1
            assert len(json_resp[0]['email_addresses']) == 1
            assert json_resp[0]['email_addresses'][0]['email_address'] == sample_email_address


def test_contacts_username(flask_app, db_sess, sample_contact):
    with flask_app.test_request_context():
        with flask_app.test_client() as client:
            resp = client.get(f'/contact?username={sample_contact.username}')
            assert resp.status_code == 200
            json_resp = json.loads(resp.get_data(as_text=True))
            assert len(json_resp) == 1
            assert json_resp[0]['username'] == sample_contact.username


def test_contacts_username_not_exists(flask_app, db_sess, sample_contact):
    with flask_app.test_request_context():
        with flask_app.test_client() as client:
            resp = client.get(f'/contact?username=random')
            assert resp.status_code == 200
            json_resp = json.loads(resp.get_data(as_text=True))
            assert len(json_resp) == 0


def test_create_contact(flask_app,
                        db_sess,
                        sample_username,
                        sample_first_name,
                        sample_last_name,
):
    with flask_app.test_request_context():
        with flask_app.test_client() as client:
            data = {
                'username': sample_username,
                'first_name': sample_first_name,
                'last_name': sample_last_name
            }
            resp = client.post('/contact', data=json.dumps(data))
            assert resp.status_code == 200
            json_resp = json.loads(resp.get_data(as_text=True))
            assert json_resp['username'] == sample_username


def test_create_contact_with_email_address(flask_app,
                                           db_sess,
                                           sample_username,
                                           sample_first_name,
                                           sample_last_name,
                                           sample_email_address,
):
    with flask_app.test_request_context():
        with flask_app.test_client() as client:
            data = {
                'username': sample_username,
                'first_name': sample_first_name,
                'last_name': sample_last_name,
                'email_addresses': [{'email_address': sample_email_address}]
            }
            resp = client.post('/contact', data=json.dumps(data))
            assert resp.status_code == 200
            json_resp = json.loads(resp.get_data(as_text=True))
            assert json_resp['username'] == sample_username
            assert json_resp['email_addresses'][0]['email_address'] == sample_email_address


def test_update_contact(flask_app,
                        db_sess,
                        sample_contact,
):
    with flask_app.test_request_context():
        with flask_app.test_client() as client:
            data = {
                'username': 'random',
                'first_name': 'random',
                'last_name': 'random',
            }
            resp = client.put(f'/contact/{sample_contact.id}', data=json.dumps(data))
            assert resp.status_code == 200
            json_resp = json.loads(resp.get_data(as_text=True))
            assert json_resp['username'] == 'random'


def test_delete_contact(flask_app,
                        db_sess,
                        sample_contact
):
    with flask_app.test_request_context():
        with flask_app.test_client() as client:
            resp = client.delete(f'/contact/{sample_contact.id}')
            assert resp.status_code == 200
            resp = client.get('/contact')
            assert resp.status_code == 200
            json_resp = json.loads(resp.get_data(as_text=True))
            assert len(json_resp) == 0
