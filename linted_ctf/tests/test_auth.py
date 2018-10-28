import pytest

from flask import session
from app.extensions import mysql


def test_register(client, auth):
    #Make sure page renders
    assert client.get('/register').status_code == 200

    #Lets test our registration
    response = client.post(
        '/register',
        data={'name': 'alligarta',
              'username': 'Alligators',
              'email': 'SecretlyFly@floridalife.org',
              'password': 'ItsNoSecretWereTesting',
              'confirm': 'ItsNoSecretWereTesting'
              })
    assert 'http://localhost/login' == response.headers['Location']

    #Validate we can login as our new user
    response = auth.login('Alligators', 'ItsNoSecretWereTesting')
    with client:
        client.get('/')
        assert session['username'] == 'Alligators'
        assert session['logged_in'] == True


def test_login(client, auth):
    # test that viewing the page renders without template errors
    assert client.get('/login').status_code == 200

    # test that successful login redirects to the dashboard page
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/dashboard'

    with client:
        client.get('/')
        assert session['logged_in'] == True
        assert session['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Username not found'),
    ('test', 'a', b'Invalid login'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'logged_in' not in session
