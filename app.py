from flask import Flask, render_template, jsonify, request, Response
from config.configuration import CONFIG
from core.logging_config import configure_logging
from handlers.capture import capture, start_auto_capture, stop_auto_capture
from handlers.stream import start_stream, stop_stream, generate_images
from handlers.parameters import get_parameters, update_parameters
from handlers.photos import api_photos, delete_photo
import atexit

# Flask application initialization
app = Flask(__name__)

# Load configuration
app.config.update(CONFIG)

# Configure logging
configure_logging()

# Main routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/stream')
def stream():
    """Video stream route"""
    return Response(
        generate_images(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/stop_stream')
def route_stop_stream():
    """Route to stop video stream"""
    result = stop_stream()
    return jsonify(result)

@app.route('/capture', methods=['POST'])
def route_capture():
    return capture()

@app.route('/start_auto_capture', methods=['POST'])
def route_start_auto_capture():
    return start_auto_capture(request.json)

@app.route('/stop_auto_capture')
def route_stop_auto_capture():
    return stop_auto_capture()

@app.route('/parameters', methods=['GET', 'POST'])
def route_parameters():
    if request.method == 'GET':
        return get_parameters()
    elif request.method == 'POST':
        return update_parameters(request.json)

@app.route('/photos')
def route_photos():
    return api_photos()

@app.route('/delete', methods=['POST'])
def route_delete_photo():
    return delete_photo(request.json)

# Error handling
@app.errorhandler(404)
def error_not_found(error):
    return jsonify({'success': False, 'error': 'Resource not found'}), 404

@app.errorhandler(500)
def error_internal(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Cleanup on exit
atexit.register(lambda: print("Cleaning up resources"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
