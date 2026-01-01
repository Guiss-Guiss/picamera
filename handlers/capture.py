import threading
import logging
from core.camera import get_camera
from flask import jsonify, url_for
from datetime import datetime, timedelta
import os
import traceback



# Global locks for synchronization
camera_lock = threading.RLock()
capture_lock = threading.Lock()

# Global variables for automatic capture
auto_capture_active = False
auto_capture_thread = None

def capture():
    try:
        with camera_lock:
            camera = get_camera()
            if not get_camera():
                return jsonify({'success': False, 'error': "Camera error"}), 500

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{timestamp}.jpg"
            file_path = os.path.join('static/media', filename)

            # Stop camera if in use
            if camera.started:
                camera.stop()

            # Configure new resolution for capture
            config = camera.create_still_configuration(
                main={"size": (4608, 2592), "format": "XBGR8888"},
            )
            camera.configure(config)

            # Restart camera after configuration
            camera.start()

            camera.capture_file(file_path)
            logging.info(f"Photo captured: {filename}")

            return jsonify({
                'success': True,
                'filename': filename,
                'path': url_for('static', filename=f'media/{filename}')
            })

    except Exception as e:
        error_msg = str(e)
        logging.error(f"Capture error: {error_msg}")
        logging.error(traceback.format_exc())
        return jsonify({'success': False, 'error': error_msg}), 500

def auto_capture_task(interval_seconds, duration_minutes):
    """Background task for automatic photo capture."""
    global auto_capture_active
    end_time = datetime.now() + timedelta(minutes=duration_minutes)
    photo_count = 0

    while datetime.now() < end_time and auto_capture_active:
        try:
            with camera_lock:
                camera = get_camera()
                if not camera:
                    logging.error("Camera error during automatic capture")
                    break

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"auto_{timestamp}.jpg"
                file_path = os.path.join('static/media', filename)

                # Stop camera if in use
                if camera.started:
                    camera.stop()

                # Configure new resolution for capture
                config = camera.create_still_configuration(
                    main={"size": (4608, 2592), "format": "XBGR8888"},
                )
                camera.configure(config)

                # Restart camera after configuration
                camera.start()

                camera.capture_file(file_path)
                photo_count += 1
                logging.info(f"Automatic photo {photo_count} captured: {filename}")
        except Exception as e:
            logging.error(f"Automatic capture error: {e}")

        threading.Event().wait(interval_seconds)

    auto_capture_active = False
    logging.info(f"Automatic capture completed. Total photos: {photo_count}")

def start_auto_capture(data):
    """Starts an automatic capture sequence."""
    global auto_capture_active, auto_capture_thread
    try:
        interval = int(data.get('interval', 60))
        duration = int(data.get('duration', 60))

        if interval < 5:
            return jsonify({'success': False, 'error': "Minimum interval is 5 seconds"}), 400

        with capture_lock:
            if auto_capture_active:
                return jsonify({'success': False, 'error': "Automatic capture is already running"}), 400

            auto_capture_active = True
            auto_capture_thread = threading.Thread(target=auto_capture_task, args=(interval, duration))
            auto_capture_thread.start()
            logging.info(f"Automatic capture started: {duration}min, interval {interval}s")
            return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error starting automatic capture: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def stop_auto_capture():
    """Stops automatic capture."""
    global auto_capture_active
    with capture_lock:
        auto_capture_active = False
    logging.info("Automatic capture stopped")
    return jsonify({'success': True})
