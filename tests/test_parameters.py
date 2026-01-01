import pytest
from app import app
from handlers.parameters import get_parameters, update_parameters
from unittest.mock import MagicMock

@pytest.fixture
def app_context():
    """Creates a Flask application context for tests."""
    app.config['SERVER_NAME'] = 'localhost'
    with app.app_context():
        yield

@pytest.fixture
def mock_camera_metadata(mock_camera):
    """Configures the camera mock with metadata."""
    mock_camera.capture_metadata = MagicMock(return_value={
        'ExposureTime': 1000,
        'AnalogueGain': 1.0,
        'Brightness': 0.0,
        'Contrast': 1.0,
        'Saturation': 1.0,
        'Sharpness': 1.0
    })
    return mock_camera

def test_get_parameters(app_context, mock_camera_metadata):
    """Tests retrieving camera parameters."""
    response, status_code = get_parameters()

    assert status_code == 200, f"Error retrieving parameters: {response}"
    data = response.get_json()
    assert data['success'], "Camera parameters were not retrieved"
    assert 'parameters' in data, "Parameters are missing"

    parameters = data['parameters']
    assert 'exposure' in parameters
    assert 'gain' in parameters
    assert 'brightness' in parameters
    assert 'contrast' in parameters
    assert 'saturation' in parameters
    assert 'sharpness' in parameters

def test_update_parameters(app_context, mock_camera):
    """Tests updating camera parameters."""
    test_params = {
        'exposure': 1000,
        'gain': 1.5,
        'brightness': 0.5,
        'contrast': 1.2,
        'saturation': 1.1,
        'sharpness': 1.3
    }

    assert mock_camera is not None
    response, status_code = update_parameters(test_params)

    assert status_code == 200, f"Error updating parameters: {response}"
    data = response.get_json()
    assert data['success'], "Parameter update failed"
    mock_camera.set_controls.assert_called_once()

def test_update_parameters_invalid(app_context, mock_camera):
    """Tests updating with invalid parameters."""
    test_params = {}  # Empty parameters

    response, status_code = update_parameters(test_params)

    assert status_code == 400, "Should reject empty parameters"
    data = response.get_json()
    assert not data['success']
