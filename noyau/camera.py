from picamera2 import Picamera2
import logging
import threading
import time

verrou_camera = threading.RLock()
camera = None

def initialiser_camera():
    global camera
    with verrou_camera:
        try:
            if camera is not None:
                nettoyer_camera()
            
            time.sleep(0.5)
            camera = Picamera2()
            config = camera.create_preview_configuration(
                main={"size": (1280, 720)},
                buffer_count=2
            )
            camera.configure(config)
            return True
        except Exception as e:
            logging.error(f"Erreur initialisation caméra: {e}")
            camera = None
            return False

def obtenir_camera(force_reset=False):
    global camera
    with verrou_camera:
        if force_reset or camera is None:
            try:
                if camera is not None:
                    nettoyer_camera()
                    time.sleep(1)  # Délai plus long pour reset
                initialiser_camera()
            except Exception as e:
                logging.error(f"Erreur reset caméra: {e}")
                camera = None
        return camera

def nettoyer_camera():
    global camera
    with verrou_camera:
        if camera:
            try:
                if hasattr(camera, 'started') and camera.started:
                    camera.stop()
                    time.sleep(0.2)
                camera.close()
                time.sleep(0.2)
            except Exception as e:
                logging.error(f"Erreur nettoyage caméra: {e}")
            finally:
                camera = None