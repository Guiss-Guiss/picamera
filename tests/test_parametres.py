import pytest
from app import app
from gestionnaires.parametres import obtenir_parametres, mettre_a_jour_parametres
from unittest.mock import MagicMock

@pytest.fixture
def app_context():
    """Crée un contexte d'application Flask pour les tests."""
    app.config['SERVER_NAME'] = 'localhost'
    with app.app_context():
        yield

@pytest.fixture
def mock_camera_metadata(mock_camera):
    """Configure le mock de la caméra avec des métadonnées."""
    mock_camera.capture_metadata = MagicMock(return_value={
        'ExposureTime': 1000,
        'AnalogueGain': 1.0,
        'Brightness': 0.0,
        'Contrast': 1.0,
        'Saturation': 1.0,
        'Sharpness': 1.0
    })
    return mock_camera

def test_obtenir_parametres(app_context, mock_camera_metadata):
    """Teste la récupération des paramètres de la caméra."""
    reponse, code_status = obtenir_parametres()
    
    assert code_status == 200, f"Erreur lors de la récupération des paramètres: {reponse}"
    donnees = reponse.get_json()
    assert donnees['succes'], "Les paramètres de la caméra n'ont pas été récupérés"
    assert 'parametres' in donnees, "Les paramètres sont manquants"
    
    parametres = donnees['parametres']
    assert 'exposition' in parametres
    assert 'gain' in parametres
    assert 'luminosite' in parametres
    assert 'contraste' in parametres
    assert 'saturation' in parametres
    assert 'nettete' in parametres

def test_mettre_a_jour_parametres(app_context, mock_camera):
    """Teste la mise à jour des paramètres de la caméra."""
    parametres_test = {
        'exposition': 1000,
        'gain': 1.5,
        'luminosite': 0.5,
        'contraste': 1.2,
        'saturation': 1.1,
        'nettete': 1.3
    }
    
    assert mock_camera is not None
    reponse, code_status = mettre_a_jour_parametres(parametres_test)
    
    assert code_status == 200, f"Erreur lors de la mise à jour des paramètres: {reponse}"
    donnees = reponse.get_json()
    assert donnees['succes'], "La mise à jour des paramètres a échoué"
    mock_camera.set_controls.assert_called_once()