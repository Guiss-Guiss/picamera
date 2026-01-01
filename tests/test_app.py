import pytest
from app import app

@pytest.fixture
def client():
    """Test client for Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(app_context):
    """Tests if the home page is accessible."""
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert b"PiCamera" in response.data

def test_gallery_route(app_context):
    """Tests if the gallery is accessible."""
    with app.test_client() as client:
        response = client.get('/gallery')
        assert response.status_code == 200
        assert b"Photo Gallery" in response.data

def test_404_error(app_context):
    """Tests 404 error handling."""
    with app.test_client() as client:
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] == False
        assert 'error' in data
