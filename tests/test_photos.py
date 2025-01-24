import pytest
from app import app
from gestionnaires.photos import api_photos, supprimer_photo
from unittest.mock import patch

@pytest.fixture
def app_context():
    """Crée un contexte d'application Flask pour les tests."""
    app.config['SERVER_NAME'] = 'localhost'
    with app.app_context():
        yield

def test_api_photos(app_context, mock_filesystem):
    """Teste la récupération de la liste des photos."""
    result = api_photos()
    
    assert result.status_code == 200, "Erreur lors de la récupération des photos"
    data = result.get_json()
    assert data['succes'], "Les photos n'ont pas été récupérées"
    assert isinstance(data['photos'], list), "Les photos doivent être une liste"
def test_supprimer_photo(app_context, mock_filesystem):
    """Teste la suppression d'une photo."""
    from gestionnaires.photos import supprimer_photo
    
    response, status_code = supprimer_photo({'nom_fichier': 'photo_test.jpg'})
    assert status_code == 200, "Erreur lors de la suppression de la photo"
    data = response.get_json()
    assert data['succes'], "La suppression de la photo a échoué"