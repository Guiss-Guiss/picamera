# test_capture.py
import pytest
from app import app
from gestionnaires.capture import capturer, demarrer_capture_auto, arreter_capture_auto
from flask import Response
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_camera(monkeypatch):
    """Mock de la caméra pour les tests."""
    camera_mock = MagicMock()
    camera_mock.started = False
    camera_mock.start = MagicMock()
    camera_mock.stop = MagicMock()
    camera_mock.capture_file = MagicMock()
    camera_mock.create_still_configuration = MagicMock(return_value=MagicMock())
    camera_mock.configure = MagicMock()

    def mock_get_camera(*args, **kwargs):
        return camera_mock
    monkeypatch.setattr('noyau.camera.obtenir_camera', mock_get_camera)
    monkeypatch.setattr('gestionnaires.capture.obtenir_camera', mock_get_camera)
    
    yield camera_mock

def test_capturer(app_context, mock_camera, mock_filesystem):
    """Teste la capture d'une photo."""
    result = capturer()
    
    assert result.status_code == 200, f"La capture a échoué: {result.get_json()}"
    data = result.get_json()
    assert data['succes'], "La capture n'a pas réussi"
    assert mock_camera.start.called, "La caméra n'a pas été démarrée"
    assert mock_camera.capture_file.called, "capture_file n'a pas été appelé"