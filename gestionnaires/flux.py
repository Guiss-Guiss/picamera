import io
import threading
import logging
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from noyau.camera import obtenir_camera
import queue
import gc

# File d'attente limitée pour les images
file_images = queue.Queue(maxsize=4)
flux_actif = False
verrou_flux = threading.RLock()
sortie_flux = None

class SortieFlux(io.BufferedIOBase):
    def write(self, donnees):
        try:
            # Évite le blocage si la file est pleine
            if not file_images.full():
                file_images.put(donnees)
            return len(donnees)
        except:
            return 0

def generer_images():
    global flux_actif, sortie_flux
    
    camera = obtenir_camera()
    if not camera:
        logging.error("Impossible d'obtenir la caméra pour le flux vidéo")
        return

    try:
        with verrou_flux:
            if not sortie_flux:
                sortie_flux = SortieFlux()
            
            if camera.started:
                camera.stop()
                
            config = camera.create_video_configuration(
                main={"size": (1280, 720),  "format": "XBGR8888"},
                buffer_count=4,
                queue=True
            )
            camera.configure(config)

            # Définir les contrôles de base
            controles = {
                "AeEnable": 1,
                "AwbEnable": 1,
                "NoiseReductionMode": 2,
                "FrameRate": 15.0
            }
            
            # Vérifier si le contrôle AfMode est supporté
            try:
                # Récupérer les contrôles supportés
                controles_supportes = camera.camera_controls
                if "AfMode" in controles_supportes:
                    controles["AfMode"] = 2
                    logging.info("Mode autofocus activé")
                else:
                    logging.info("Mode autofocus non supporté par cette caméra")
            except Exception as e:
                logging.warning(f"Impossible de vérifier les contrôles disponibles: {e}")
            
            # Appliquer les contrôles
            camera.set_controls(controles)

            encodeur = JpegEncoder(q=70)
            camera.start_recording(encodeur, FileOutput(sortie_flux))
            flux_actif = True
        
        while flux_actif:
            try:
                # Timeout pour éviter le blocage
                image = file_images.get(timeout=1.0)
                if image and flux_actif:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
                    # Force la libération de la mémoire
                    del image
                    gc.collect()
            except queue.Empty:
                continue
            except Exception as e:
                if flux_actif:
                    logging.error(f"Erreur génération image: {e}")
                    continue
    
    except Exception as e:
        logging.error(f"Erreur flux: {e}")
    
    finally:
        with verrou_flux:
            try:
                if camera and camera.started:
                    camera.stop_recording()
                    camera.stop()
                logging.info("Flux vidéo arrêté")
            except Exception as e:
                logging.error(f"Erreur arrêt flux: {e}")
            sortie_flux = None
            flux_actif = False
            # Vide la file d'attente
            while not file_images.empty():
                file_images.get()
            gc.collect()

def demarrer_flux():
    global flux_actif
    with verrou_flux:
        flux_actif = True
    logging.info("Flux vidéo activé")
    return {'succes': True}

def arreter_flux():
    global flux_actif, sortie_flux
    with verrou_flux:
        flux_actif = False
        camera = obtenir_camera()
        if camera and camera.started:
            try:
                camera.stop_recording()
                camera.stop()
                logging.info("Flux vidéo arrêté")
            except Exception as e:
                logging.error(f"Erreur arrêt flux: {e}")
        sortie_flux = None
        # Force le nettoyage mémoire
        gc.collect()
    return {'succes': True}
