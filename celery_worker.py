import os
from contact_flask_sqlalchemy_example import celery, create_app
 
app = create_app()
app.app_context().push()
