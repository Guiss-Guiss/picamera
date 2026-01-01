import pytest
from app import app
from handlers.photos import api_photos, delete_photo
from unittest.mock import patch

@pytest.fixture
def app_context():
    """Creates a Flask application context for tests."""
    app.config['SERVER_NAME'] = 'localhost'
    with app.app_context():
        yield

def test_api_photos(app_context, mock_filesystem):
    """Tests retrieving the list of photos."""
    result = api_photos()

    assert result.status_code == 200, "Error retrieving photos"
    data = result.get_json()
    assert data['success'], "Photos were not retrieved"
    assert isinstance(data['photos'], list), "Photos should be a list"

def test_delete_photo(app_context, mock_filesystem):
    """Tests deleting a photo."""
    from handlers.photos import delete_photo

    response, status_code = delete_photo({'filename': 'photo_test.jpg'})
    assert status_code == 200, "Error deleting photo"
    data = response.get_json()
    assert data['success'], "Photo deletion failed"

def test_delete_photo_missing_filename(app_context, mock_filesystem):
    """Tests deleting without filename."""
    response, status_code = delete_photo({})
    assert status_code == 400, "Should reject missing filename"
    data = response.get_json()
    assert not data['success']

def test_delete_photo_not_found(app_context, mock_filesystem):
    """Tests deleting non-existent photo."""
    response, status_code = delete_photo({'filename': 'nonexistent.jpg'})
    assert status_code == 404, "Should return 404 for non-existent file"
    data = response.get_json()
    assert not data['success']
