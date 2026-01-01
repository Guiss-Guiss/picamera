# tests/test_camera.py
import pytest
from unittest.mock import patch, MagicMock
from core.camera import initialize_camera, get_camera, cleanup_camera

@pytest.fixture
def mock_camera(monkeypatch):
    """Camera mock for tests."""
    camera_mock = MagicMock()

    # Basic configuration
    camera_mock.started = False
    camera_mock.start = MagicMock()
    camera_mock.stop = MagicMock()
    camera_mock.close = MagicMock()

    # Initialization configuration
    config_mock = MagicMock()
    camera_mock.create_preview_configuration = MagicMock(return_value=config_mock)
    camera_mock.configure = MagicMock()

    # Mock Picamera2
    picamera_mock = MagicMock(return_value=camera_mock)
    monkeypatch.setattr('core.camera.Picamera2', picamera_mock)

    # Reset module global variables
    import core.camera
    monkeypatch.setattr(core.camera, 'camera', None)  # Force camera to None

    return camera_mock

def test_initialize_camera(mock_camera):
    """Tests camera initialization."""
    from core.camera import camera

    # Check initial state
    assert camera is None, "Camera should not be initialized"

    # Execute initialization
    result = initialize_camera()

    # Check result
    assert result == True, "Camera could not be initialized"
    mock_camera.create_preview_configuration.assert_called_once()
    mock_camera.configure.assert_called_once()

def test_get_camera(mock_camera):
    """Tests getting the camera."""
    camera = get_camera()
    assert camera is not None, "Camera instance is None"
    assert isinstance(camera, MagicMock), "Wrong camera instance returned"

def test_cleanup_camera(mock_camera, monkeypatch):
    """Tests camera resource cleanup."""
    import core.camera

    # Initialize and start camera
    initialize_camera()
    mock_camera.started = True

    # Execute cleanup
    cleanup_camera()

    # Check calls
    mock_camera.stop.assert_called_once()
    mock_camera.close.assert_called_once()

    # Check that global camera variable is set to None
    assert core.camera.camera is None
