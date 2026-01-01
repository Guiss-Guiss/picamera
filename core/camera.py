from picamera2 import Picamera2
import logging
import threading
import time

camera_lock = threading.RLock()
camera = None

def initialize_camera():
    global camera
    with camera_lock:
        try:
            if camera is not None:
                cleanup_camera()

            time.sleep(0.5)
            camera = Picamera2()
            config = camera.create_preview_configuration(
                main={"size": (1280, 720)},
                buffer_count=2
            )
            camera.configure(config)
            return True
        except Exception as e:
            logging.error(f"Camera initialization error: {e}")
            camera = None
            return False

def get_camera(force_reset=False):
    global camera
    with camera_lock:
        if force_reset or camera is None:
            try:
                if camera is not None:
                    cleanup_camera()
                    time.sleep(1)  # Longer delay for reset
                initialize_camera()
            except Exception as e:
                logging.error(f"Camera reset error: {e}")
                camera = None
        return camera

def cleanup_camera():
    global camera
    with camera_lock:
        if camera:
            try:
                if hasattr(camera, 'started') and camera.started:
                    camera.stop()
                    time.sleep(0.2)
                camera.close()
                time.sleep(0.2)
            except Exception as e:
                logging.error(f"Camera cleanup error: {e}")
            finally:
                camera = None
