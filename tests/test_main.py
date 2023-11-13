import pytest
import os
import tempfile
import sys
sys.path.append("src")
from main import app, page_de_garde, about_us

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            yield client

def test_page_de_garde(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Accueil' in response.data

def test_about_us(client):
    response = client.get('/about_us')
    assert response.status_code == 200
    assert b'About us' in response.data
