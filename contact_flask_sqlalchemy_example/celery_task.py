import time
import random
import string
from celery.schedules import crontab
from contact_flask_sqlalchemy_example import celery
from contact_flask_sqlalchemy_example.models.contact_op import (
    create_contact_op,
    delete_old_contacts_op,
)


def random_string(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(15.0,
                             create_random_contact.s(),
                             name='Create contact every 15 secs',
    )
    #sender.add_periodic_task(60.0,
    #                         delete_old_contact.s(),
    #                         name='Remove contacts older than 1 minute',
    #)


@celery.task()
def create_random_contact():
    username = random_string()
    first_name = random_string()
    last_name = random_string()
    create_contact_op(username, first_name, last_name)


@celery.task()
def delete_old_contact():
    now = time.time()
    old = int(now - 60)
    delete_old_contacts_op(old)
