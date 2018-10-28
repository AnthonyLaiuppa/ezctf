import pytest

from app import create_app
from tests.db_utils import provision_db, destroy_db
from app.extensions import mysql

@pytest.fixture
def app():
    #Create temporary test database
    provision_db()
    print('provisining test db')
    app = create_app({
		'TESTING': True,
		'MYSQL_HOST': '',
		'MYSQL_USER': '',
		'MYSQL_PASSWORD': '',
		'MYSQL_DB': 'ezctf-test',
		'MYSQL_CURSORCLASS': 'DictCursor'
		})

#	with app.app_context():
#		mysql.init_app(app)	

    yield app
    destroy_db()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
