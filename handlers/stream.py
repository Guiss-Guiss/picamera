import io
import threading
import logging
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from core.camera import get_camera
import queue
import gc

# Limited queue for images
image_queue = queue.Queue(maxsize=4)
stream_active = False
stream_lock = threading.RLock()
stream_output = None

class StreamOutput(io.BufferedIOBase):
    def write(self, data):
        try:
            # Avoid blocking if queue is full
            if not image_queue.full():
                image_queue.put(data)
            return len(data)
        except:
            return 0

def generate_images():
    global stream_active, stream_output

    camera = get_camera()
    if not camera:
        logging.error("Unable to get camera for video stream")
        return

    try:
        with stream_lock:
            if not stream_output:
                stream_output = StreamOutput()

            if camera.started:
                camera.stop()

            config = camera.create_video_configuration(
                main={"size": (1280, 720),  "format": "XBGR8888"},
                buffer_count=4,
                queue=True
            )
            camera.configure(config)

            # Set basic controls
            controls = {
                "AeEnable": 1,
                "AwbEnable": 1,
                "NoiseReductionMode": 2,
                "FrameRate": 15.0
            }

            # Check if AfMode control is supported
            try:
                # Get supported controls
                supported_controls = camera.camera_controls
                if "AfMode" in supported_controls:
                    controls["AfMode"] = 2
                    logging.info("Autofocus mode enabled")
                else:
                    logging.info("Autofocus mode not supported by this camera")
            except Exception as e:
                logging.warning(f"Unable to check available controls: {e}")

            # Apply controls
            camera.set_controls(controls)

            encoder = JpegEncoder(q=70)
            camera.start_recording(encoder, FileOutput(stream_output))
            stream_active = True

        while stream_active:
            try:
                # Timeout to avoid blocking
                image = image_queue.get(timeout=1.0)
                if image and stream_active:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
                    # Force memory release
                    del image
                    gc.collect()
            except queue.Empty:
                continue
            except Exception as e:
                if stream_active:
                    logging.error(f"Image generation error: {e}")
                    continue

    except Exception as e:
        logging.error(f"Stream error: {e}")

    finally:
        with stream_lock:
            try:
                if camera and camera.started:
                    camera.stop_recording()
                    camera.stop()
                logging.info("Video stream stopped")
            except Exception as e:
                logging.error(f"Stream stop error: {e}")
            stream_output = None
            stream_active = False
            # Empty the queue
            while not image_queue.empty():
                image_queue.get()
            gc.collect()

def start_stream():
    global stream_active
    with stream_lock:
        stream_active = True
    logging.info("Video stream enabled")
    return {'success': True}

def stop_stream():
    global stream_active, stream_output
    with stream_lock:
        stream_active = False
        camera = get_camera()
        if camera and camera.started:
            try:
                camera.stop_recording()
                camera.stop()
                logging.info("Video stream stopped")
            except Exception as e:
                logging.error(f"Stream stop error: {e}")
        stream_output = None
        # Force memory cleanup
        gc.collect()
    return {'success': True}
