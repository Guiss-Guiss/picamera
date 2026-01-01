# test_capture.py
import pytest
from app import app
from handlers.capture import capture, start_auto_capture, stop_auto_capture
from flask import Response
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_camera(monkeypatch):
    """Camera mock for tests."""
    camera_mock = MagicMock()
    camera_mock.started = False
    camera_mock.start = MagicMock()
    camera_mock.stop = MagicMock()
    camera_mock.capture_file = MagicMock()
    camera_mock.create_still_configuration = MagicMock(return_value=MagicMock())
    camera_mock.configure = MagicMock()

    def mock_get_camera(*args, **kwargs):
        return camera_mock
    monkeypatch.setattr('core.camera.get_camera', mock_get_camera)
    monkeypatch.setattr('handlers.capture.get_camera', mock_get_camera)

    yield camera_mock

def test_capture(app_context, mock_camera, mock_filesystem):
    """Tests photo capture."""
    result = capture()

    assert result.status_code == 200, f"Capture failed: {result.get_json()}"
    data = result.get_json()
    assert data['success'], "Capture was not successful"
    assert mock_camera.start.called, "Camera was not started"
    assert mock_camera.capture_file.called, "capture_file was not called"

def test_start_auto_capture(app_context, mock_camera):
    """Tests starting auto capture."""
    data = {'interval': 10, 'duration': 1}
    result = start_auto_capture(data)

    assert result.status_code == 200, f"Start auto capture failed: {result.get_json()}"
    response_data = result.get_json()
    assert response_data['success'], "Auto capture did not start"

    # Clean up - stop the auto capture
    stop_auto_capture()

def test_stop_auto_capture(app_context, mock_camera):
    """Tests stopping auto capture."""
    result = stop_auto_capture()

    assert result.status_code == 200, f"Stop auto capture failed: {result.get_json()}"
    response_data = result.get_json()
    assert response_data['success'], "Auto capture did not stop"

def test_auto_capture_minimum_interval(app_context, mock_camera):
    """Tests that minimum interval is enforced."""
    data = {'interval': 2, 'duration': 1}  # Less than 5 seconds minimum
    result = start_auto_capture(data)

    # Handler returns (response, status_code) tuple on error
    response, status_code = result
    assert status_code == 400, "Should reject interval less than 5 seconds"
    response_data = response.get_json()
    assert not response_data['success']
