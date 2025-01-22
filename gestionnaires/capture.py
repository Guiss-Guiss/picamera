import threading
import logging
from noyau.camera import obtenir_camera
from flask import jsonify, url_for
from datetime import datetime, timedelta
import os
import traceback



# Verrous globaux pour la synchronisation
verrou_camera = threading.RLock()
verrou_capture = threading.Lock()

# Variables globales pour la capture automatique
capture_auto_active = False
fil_capture_auto = None

def capturer():
    try:
        with verrou_camera:
            camera = obtenir_camera()
            if not obtenir_camera():
                return jsonify({'succes': False, 'erreur': "Erreur de caméra"}), 500

            horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_fichier = f"photo_{horodatage}.jpg"
            chemin_fichier = os.path.join('static/media', nom_fichier)

            # Arrêter la caméra si elle est en cours d'utilisation
            if camera.started:
                camera.stop()

            # Configurer une nouvelle résolution pour la capture
            config = camera.create_still_configuration(
                main={"size": (4608, 2592), "format": "XBGR8888"},
            )
            camera.configure(config)

            # Redémarrer la caméra après configuration
            camera.start()

            camera.capture_file(chemin_fichier)
            logging.info(f"Photo capturée: {nom_fichier}")
            
            return jsonify({
                'succes': True,
                'nom_fichier': nom_fichier,
                'chemin': url_for('static', filename=f'media/{nom_fichier}')
            })
            
    except Exception as e:
        msg_erreur = str(e)
        logging.error(f"Erreur de capture: {msg_erreur}")
        logging.error(traceback.format_exc())
        return jsonify({'succes': False, 'erreur': msg_erreur}), 500
        
def tache_capture_auto(intervalle_secondes, duree_minutes):
    """Tâche d'arrière-plan pour la capture automatique de photos."""
    global capture_auto_active
    heure_fin = datetime.now() + timedelta(minutes=duree_minutes)
    nombre_photos = 0
    
    while datetime.now() < heure_fin and capture_auto_active:
        try:
            with verrou_camera:
                camera = obtenir_camera()
                if not camera:
                    logging.error("Erreur de caméra pendant la capture automatique")
                    break
                
                horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
                nom_fichier = f"auto_{horodatage}.jpg"
                chemin_fichier = os.path.join('static/media', nom_fichier)

                # Arrêter la caméra si elle est en cours d'utilisation
                if camera.started:
                    camera.stop()

                # Configurer une nouvelle résolution pour la capture
                config = camera.create_still_configuration(
                    main={"size": (4608, 2592), "format": "XBGR8888"},
                )
                camera.configure(config)

                # Redémarrer la caméra après configuration
                camera.start()

                camera.capture_file(chemin_fichier)
                nombre_photos += 1
                logging.info(f"Photo automatique {nombre_photos} capturée: {nom_fichier}")
        except Exception as e:
            logging.error(f"Erreur de capture automatique: {e}")
        
        threading.Event().wait(intervalle_secondes)
    
    capture_auto_active = False
    logging.info(f"Capture automatique terminée. Total des photos: {nombre_photos}")

def demarrer_capture_auto(donnees):
    """Démarre une séquence de capture automatique."""
    global capture_auto_active, fil_capture_auto
    try:
        intervalle = int(donnees.get('intervalle', 60))
        duree = int(donnees.get('duree', 60))
        
        if intervalle < 5:
            return jsonify({'succes': False, 'erreur': "L'intervalle minimum est de 5 secondes"}), 400
        
        with verrou_capture:
            if capture_auto_active:
                return jsonify({'succes': False, 'erreur': "La capture automatique est déjà en cours"}), 400
            
            capture_auto_active = True
            fil_capture_auto = threading.Thread(target=tache_capture_auto, args=(intervalle, duree))
            fil_capture_auto.start()
            logging.info(f"Capture automatique démarrée: {duree}min, intervalle {intervalle}s")
            return jsonify({'succes': True})
    except Exception as e:
        logging.error(f"Erreur lors du démarrage de la capture automatique: {e}")
        return jsonify({'succes': False, 'erreur': str(e)}), 500

def arreter_capture_auto():
    """Arrête la capture automatique."""
    global capture_auto_active
    with verrou_capture:
        capture_auto_active = False
    logging.info("Capture automatique arrêtée")
    return jsonify({'succes': True})
