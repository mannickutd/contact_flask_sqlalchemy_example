import os
from flask_script import (Manager, Server)
from flask_migrate import (Migrate, MigrateCommand)
from contact_flask_sqlalchemy_example import (create_app, db)


application = create_app()
manager = Manager(application)
host = os.environ.get('API_HOST', "0.0.0.0")
port = int(os.environ.get('API_PORT', 5000))
manager.add_command("runserver", Server(host=host, port=port))
Migrate(application, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
