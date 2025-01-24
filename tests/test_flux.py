import pytest
from app import app
from gestionnaires.flux import demarrer_flux, arreter_flux

@pytest.fixture
def app_context():
    """Crée un contexte d'application Flask pour les tests."""
    with app.app_context():
        yield

def test_demarrer_flux(app_context, mock_camera):
    """Teste le démarrage du flux vidéo."""
    response = demarrer_flux()
    
    assert response['succes'], "Le démarrage du flux vidéo a échoué"

def test_arreter_flux(app_context, mock_camera):
    """Teste l'arrêt du flux vidéo."""
    response = arreter_flux()
    
    assert response['succes'], "L'arrêt du flux vidéo a échoué"
    if mock_camera.started:
        mock_camera.stop_recording.assert_called_once()