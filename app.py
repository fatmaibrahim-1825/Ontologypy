import os
import unittest

import serverless_wsgi
from flask_script import Manager

from api.controller import blueprint as apis

from api import create_app

app = create_app(os.getenv('ENV') or 'dev')

app.config['ERROR_404_HELP'] = False

# app.register_blueprint(user)
app.register_blueprint(apis)

app.app_context().push()

manager = Manager(app)


@manager.command
def run():
    app.run()


def handler(event, context):
    print(f'event {event}')
    return serverless_wsgi.handle_request(app, event, context)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
