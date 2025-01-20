import os
import logging
from flask import jsonify, url_for

DOSSIER_PHOTOS = 'static/media'

def obtenir_photos():
    """Récupère la liste des fichiers photos dans un répertoire spécifique."""
    try:
        return [
            f for f in os.listdir(DOSSIER_PHOTOS)
            if os.path.isfile(os.path.join(DOSSIER_PHOTOS, f)) 
            and f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des photos : {e}")
        return []

def api_photos():
    """Retourne la liste des photos capturées."""
    try:
        fichiers = []
        for nom_fichier in obtenir_photos():
            chemin_fichier = os.path.join(DOSSIER_PHOTOS, nom_fichier)
            fichiers.append({
                'nom_fichier': nom_fichier,
                'chemin': url_for('static', filename=f'media/{nom_fichier}', _external=True),
                'date': os.path.getctime(chemin_fichier)
            })

        fichiers_tries = sorted(fichiers, key=lambda x: x['date'], reverse=True)
        return jsonify({
            'succes': True,
            'photos': fichiers_tries
        })
    except Exception as e:
        logging.error(f"Erreur dans api_photos : {e}")
        return jsonify({
            'succes': False,
            'erreur': str(e),
            'photos': []
        })
def supprimer_photo(donnees):
    """Supprime une photo spécifiée."""
    try:
        nom_fichier = donnees.get('nom_fichier')
        if not nom_fichier:
            return jsonify({'succes': False, 'erreur': "Nom de fichier manquant"}), 400

        chemin_fichier = os.path.join(DOSSIER_PHOTOS, nom_fichier)
        if not os.path.exists(chemin_fichier):
            return jsonify({'succes': False, 'erreur': "Fichier non trouvé"}), 404

        os.remove(chemin_fichier)
        logging.info(f"Photo supprimée: {nom_fichier}")
        return jsonify({'succes': True}), 200
    except Exception as e:
        logging.error(f"Erreur dans supprimer_photo : {e}")
        return jsonify({'succes': False, 'erreur': str(e)}), 500