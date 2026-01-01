import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Mock picamera2 before importing app
mock_picamera2 = MagicMock()
mock_picamera2.Picamera2 = MagicMock()
mock_picamera2.encoders = MagicMock()
mock_picamera2.encoders.MJPEGEncoder = MagicMock()
mock_picamera2.outputs = MagicMock()
mock_picamera2.outputs.FileOutput = MagicMock()
sys.modules['picamera2'] = mock_picamera2
sys.modules['picamera2.encoders'] = mock_picamera2.encoders
sys.modules['picamera2.outputs'] = mock_picamera2.outputs

from flask import Flask
from app import app
from config.configuration import UPLOAD_FOLDER

@pytest.fixture
def app_context():
    """Creates a Flask application context for tests."""
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost'
    with app.app_context():
        yield

@pytest.fixture
def mock_camera(monkeypatch):
    """Simulates a camera for tests."""
    camera_mock = MagicMock()

    # Basic mock configuration
    camera_mock.started = False
    camera_mock.start = MagicMock()
    camera_mock.stop = MagicMock()
    camera_mock.close = MagicMock()
    camera_mock.capture_file = MagicMock()
    camera_mock.start_recording = MagicMock()
    camera_mock.stop_recording = MagicMock()

    # Configuration mock
    config_mock = MagicMock()
    camera_mock.create_still_configuration = MagicMock(return_value=config_mock)
    camera_mock.create_video_configuration = MagicMock(return_value=config_mock)
    camera_mock.create_preview_configuration = MagicMock(return_value=config_mock)
    camera_mock.configure = MagicMock()

    # Metadata and controls mock
    camera_mock.capture_metadata = {
        'ExposureTime': 1000,
        'AnalogueGain': 1.0,
        'Brightness': 0.0,
        'Contrast': 1.0,
        'Saturation': 1.0,
        'Sharpness': 1.0
    }
    camera_mock.set_controls = MagicMock()

    def mock_get_camera(*args, **kwargs):
        return camera_mock

    # Global patch of get_camera function
    monkeypatch.setattr('core.camera.get_camera', mock_get_camera)
    monkeypatch.setattr('handlers.capture.get_camera', mock_get_camera)
    monkeypatch.setattr('handlers.parameters.get_camera', mock_get_camera)
    monkeypatch.setattr('handlers.stream.get_camera', mock_get_camera)

    yield camera_mock

@pytest.fixture
def mock_filesystem(tmp_path, monkeypatch):
    """Simulates the filesystem for tests."""
    test_media_dir = tmp_path / 'static' / 'media'
    test_media_dir.mkdir(parents=True, exist_ok=True)

    # Create a test file
    test_file = test_media_dir / 'photo_test.jpg'
    test_file.write_text('test content')

    # Mock UPLOAD_FOLDER for all modules that use it
    monkeypatch.setattr('config.configuration.UPLOAD_FOLDER', str(test_media_dir))
    monkeypatch.setattr('handlers.photos.PHOTOS_FOLDER', str(test_media_dir))

    # Mock os.path.join for file paths
    original_join = os.path.join
    def mock_path_join(*args):
        if 'media' in args:
            return original_join(str(test_media_dir), args[-1])
        return original_join(*args)

    monkeypatch.setattr('os.path.join', mock_path_join)
    yield test_media_dir
