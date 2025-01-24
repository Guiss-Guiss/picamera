# tests/test_camera.py
import pytest
from unittest.mock import patch, MagicMock
from noyau.camera import initialiser_camera, obtenir_camera, nettoyer_camera

@pytest.fixture
def mock_camera(monkeypatch):
    """Mock de la caméra pour les tests."""
    camera_mock = MagicMock()
    
    # Configuration de base
    camera_mock.started = False
    camera_mock.start = MagicMock()
    camera_mock.stop = MagicMock()
    camera_mock.close = MagicMock()
    
    # Configuration pour l'initialisation
    config_mock = MagicMock()
    camera_mock.create_preview_configuration = MagicMock(return_value=config_mock)
    camera_mock.configure = MagicMock()
    
    # Mock de Picamera2
    picamera_mock = MagicMock(return_value=camera_mock)
    monkeypatch.setattr('noyau.camera.Picamera2', picamera_mock)
    
    # Réinitialisation des variables globales du module
    import noyau.camera
    monkeypatch.setattr(noyau.camera, 'camera', None)  # Forcer camera à None
    
    return camera_mock

def test_initialiser_camera(mock_camera):
    """Teste l'initialisation de la caméra."""
    from noyau.camera import camera
    
    # Vérifier l'état initial
    assert camera is None, "La caméra ne devrait pas être initialisée"
    
    # Exécuter l'initialisation
    result = initialiser_camera()
    
    # Vérifier le résultat
    assert result == True, "La caméra n'a pas pu être initialisée"
    mock_camera.create_preview_configuration.assert_called_once()
    mock_camera.configure.assert_called_once()

def test_obtenir_camera(mock_camera):
    """Teste l'obtention de la caméra."""
    camera = obtenir_camera()
    assert camera is not None, "L'instance de la caméra est None"
    assert isinstance(camera, MagicMock), "La mauvaise instance de caméra a été retournée"

def test_nettoyer_camera(mock_camera, monkeypatch):
    """Teste le nettoyage des ressources de la caméra."""
    import noyau.camera
    
    # Initialiser et démarrer la caméra
    initialiser_camera()
    mock_camera.started = True
    
    # Exécuter le nettoyage
    nettoyer_camera()
    
    # Vérifier les appels
    mock_camera.stop.assert_called_once()
    mock_camera.close.assert_called_once()
    
    # Vérifier que la variable globale camera est bien mise à None
    assert noyau.camera.camera is None