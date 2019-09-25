#!/usr/bin/env python
import pytest
from contact_flask_sqlalchemy_example import (create_app, db)
from contact_flask_sqlalchemy_example.models.contact_op import (
    create_contact_op
)


@pytest.fixture(scope='session')
def flask_app(request):
    app = create_app()
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def db_sess(request, flask_app):
    def teardown():
        meta = db.metadata
        db.session.rollback()
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
            db.session.commit()
        db.session.remove()

    request.addfinalizer(teardown)
    db.create_all()
    return db.session


@pytest.fixture(scope='session')
def sample_username():
    return "username"


@pytest.fixture(scope='session')
def sample_first_name():
    return "first_name"


@pytest.fixture(scope='session')
def sample_last_name():
    return "last_name"


@pytest.fixture
def sample_contact(db_sess,
                   sample_username,
                   sample_first_name,
                   sample_last_name
):
    return create_contact_op(sample_username,
                             sample_first_name,
                             sample_last_name
    )


@pytest.fixture
def sample_email_address():
    return "email@email.com"


@pytest.fixture
def sample_contact_with_email_addresses(db_sess,
                                        sample_username,
                                        sample_first_name,
                                        sample_last_name,
                                        sample_email_address
):
    return create_contact_op(sample_username,
                             sample_first_name,
                             sample_last_name,
                             [sample_email_address]
    )
