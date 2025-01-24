import pytest
from app import app

@pytest.fixture
def client():
    """Client de test pour Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(app_context):
    """Teste si la page d'accueil est accessible."""
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b"PiCamera" in response.data

def test_galerie_route(app_context):
    """Teste si la galerie est accessible."""
    with app.test_client() as client:
        response = client.get('/galerie')
        assert response.status_code == 200
        assert b"Galerie Photos" in response.data
