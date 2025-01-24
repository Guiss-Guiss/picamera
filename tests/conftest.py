import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import app
import os
from config.configuration import DOSSIER_UPLOAD

@pytest.fixture
def app_context():
    """Crée un contexte d'application Flask pour les tests."""
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost'
    with app.app_context():
        yield

@pytest.fixture
def mock_camera(monkeypatch):
    """Simule une caméra pour les tests."""
    camera_mock = MagicMock()
    
    # Configuration de base du mock
    camera_mock.started = False
    camera_mock.start = MagicMock()
    camera_mock.stop = MagicMock()
    camera_mock.close = MagicMock()
    camera_mock.capture_file = MagicMock()
    camera_mock.start_recording = MagicMock()
    camera_mock.stop_recording = MagicMock()
    
    # Mock de la configuration
    config_mock = MagicMock()
    camera_mock.create_still_configuration = MagicMock(return_value=config_mock)
    camera_mock.create_video_configuration = MagicMock(return_value=config_mock)
    camera_mock.create_preview_configuration = MagicMock(return_value=config_mock)
    camera_mock.configure = MagicMock()
    
    # Mock des métadonnées et contrôles
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
    
    # Patch global de la fonction obtenir_camera
    monkeypatch.setattr('noyau.camera.obtenir_camera', mock_get_camera)
    monkeypatch.setattr('gestionnaires.capture.obtenir_camera', mock_get_camera)
    monkeypatch.setattr('gestionnaires.parametres.obtenir_camera', mock_get_camera)
    monkeypatch.setattr('gestionnaires.flux.obtenir_camera', mock_get_camera)
    
    yield camera_mock

@pytest.fixture
def mock_filesystem(tmp_path, monkeypatch):
    """Simule le système de fichiers pour les tests."""
    test_media_dir = tmp_path / 'static' / 'media'
    test_media_dir.mkdir(parents=True, exist_ok=True)
    
    # Créer un fichier de test
    test_file = test_media_dir / 'photo_test.jpg'
    test_file.write_text('test content')
    
    # Mock DOSSIER_UPLOAD pour tous les modules qui l'utilisent
    monkeypatch.setattr('config.configuration.DOSSIER_UPLOAD', str(test_media_dir))
    monkeypatch.setattr('gestionnaires.photos.DOSSIER_PHOTOS', str(test_media_dir))
    
    # Mock os.path.join pour les chemins de fichiers
    original_join = os.path.join
    def mock_path_join(*args):
        if 'media' in args:
            return original_join(str(test_media_dir), args[-1])
        return original_join(*args)
    
    monkeypatch.setattr('os.path.join', mock_path_join)
    yield test_media_dir