import logging
from flask import jsonify
from noyau.camera import obtenir_camera

def obtenir_parametres():
    """Récupère les paramètres actuels de la caméra."""
    try:
        camera = obtenir_camera()
        if not camera:
            return jsonify({'succes': False, 'erreur': "Caméra non disponible"}), 500

        metadonnees = camera.capture_metadata()
        if not isinstance(metadonnees, dict):
            return jsonify({'succes': False, 'erreur': "Métadonnées invalides"}), 500

        return jsonify({
            'succes': True,
            'parametres': {
                'exposition': metadonnees.get('ExposureTime', 0),
                'gain': metadonnees.get('AnalogueGain', 1.0),
                'luminosite': metadonnees.get('Brightness', 0.0),
                'contraste': metadonnees.get('Contrast', 1.0),
                'saturation': metadonnees.get('Saturation', 1.0),
                'nettete': metadonnees.get('Sharpness', 1.0)
            }
        }), 200
    except Exception as e:
        logging.error(f"Erreur dans obtenir_parametres: {e}")
        return jsonify({'succes': False, 'erreur': str(e)}), 500

def mettre_a_jour_parametres(donnees):
    """Met à jour les paramètres de la caméra avec gestion d'erreurs."""
    try:
        camera = obtenir_camera()
        if not camera:
            return jsonify({'succes': False, 'erreur': "Caméra non disponible"}), 500

        parametres_camera = {}
        
        # Traitement sécurisé du temps d'exposition
        try:
            if 'exposition' in donnees and donnees['exposition'] is not None:
                temps_exposition = int(donnees['exposition'])
                if temps_exposition >= 0:
                    parametres_camera['ExposureTime'] = temps_exposition
        except (ValueError, TypeError):
            logging.warning(f"Valeur d'exposition invalide: {donnees.get('exposition')}")

        # Traitement des paramètres de type flottant
        parametres_flottants = {
            'gain': 'AnalogueGain',
            'luminosite': 'Brightness',
            'contraste': 'Contrast',
            'saturation': 'Saturation',
            'nettete': 'Sharpness'
        }

        for param_fr, param_systeme in parametres_flottants.items():
            try:
                if param_fr in donnees and donnees[param_fr] is not None:
                    valeur = float(donnees[param_fr])
                    parametres_camera[param_systeme] = valeur
            except (ValueError, TypeError):
                logging.warning(f"Valeur invalide pour {param_fr}: {donnees.get(param_fr)}")

        if parametres_camera:
            camera.set_controls(parametres_camera)
            logging.info(f"Paramètres de caméra mis à jour: {parametres_camera}")
            return jsonify({'succes': True}), 200
        else:
            return jsonify({'succes': False, 'erreur': "Aucun paramètre valide fourni"}), 400
            
    except Exception as erreur:
        logging.error(f"Erreur dans mettre_a_jour_parametres: {erreur}")
        return jsonify({'succes': False, 'erreur': str(erreur)}), 500