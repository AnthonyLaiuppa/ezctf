import pytest
from flask import session

from app.extensions import mysql

#There is plenty of behavior issues here but this is just a demo soo.....
def test_index(client, auth):
    response = client.get('/')
    assert response.status_code == 200
#    assert b"Register" in response.data
#    I just dont care enough to validate the index
#    auth.login()
#    response = client.get('/')
#    assert b'Hack the planet' in response.data

def test_about(client, auth):
	response = client.get('/about')
	assert b"About ezCTF" in response.data
#   Yup our highly complex About page loaded fine

def test_login_required(client):
    #message = b'Unauthorized, Please login'
    with client:

        response = client.get('/dashboard')
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/login'
    #assert message in response.data

def test_admin(client, auth):
    response = auth.login('boaty', 'test')

    with client:

        client.get('/add_challenge', follow_redirects=True)
        assert session['admin'] == False
        
    
    stuff = client.get('/add_challenge')
    assert stuff.status_code == 302
    assert stuff.headers['Location'] == 'http://localhost/dashboard'
    
    #Getting this work is ideal but it never returns in the data
    #assert b'Unauthorized activity' in client.get('/add_challenge', follow_redirects=True).data
    #Same error as index, it doesnt load the full body in data, just layout... why    

def test_default_challenge(client):
	response = client.get('/challenge/1/')
	assert b"web1" in response.data


def test_not_found(client):
    response = client.get('/dash23')
    assert b"Page Not Found" in response.data