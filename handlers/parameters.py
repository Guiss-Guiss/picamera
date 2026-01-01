import logging
from flask import jsonify
from core.camera import get_camera

def get_parameters():
    """Retrieves current camera settings."""
    try:
        camera = get_camera()
        if not camera:
            return jsonify({'success': False, 'error': "Camera not available"}), 500

        metadata = camera.capture_metadata()
        if not isinstance(metadata, dict):
            return jsonify({'success': False, 'error': "Invalid metadata"}), 500

        return jsonify({
            'success': True,
            'parameters': {
                'exposure': metadata.get('ExposureTime', 0),
                'gain': metadata.get('AnalogueGain', 1.0),
                'brightness': metadata.get('Brightness', 0.0),
                'contrast': metadata.get('Contrast', 1.0),
                'saturation': metadata.get('Saturation', 1.0),
                'sharpness': metadata.get('Sharpness', 1.0)
            }
        }), 200
    except Exception as e:
        logging.error(f"Error in get_parameters: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def update_parameters(data):
    """Updates camera settings with error handling."""
    try:
        camera = get_camera()
        if not camera:
            return jsonify({'success': False, 'error': "Camera not available"}), 500

        camera_params = {}

        # Safe processing of exposure time
        try:
            if 'exposure' in data and data['exposure'] is not None:
                exposure_time = int(data['exposure'])
                if exposure_time >= 0:
                    camera_params['ExposureTime'] = exposure_time
        except (ValueError, TypeError):
            logging.warning(f"Invalid exposure value: {data.get('exposure')}")

        # Processing float parameters
        float_params = {
            'gain': 'AnalogueGain',
            'brightness': 'Brightness',
            'contrast': 'Contrast',
            'saturation': 'Saturation',
            'sharpness': 'Sharpness'
        }

        for param_key, system_param in float_params.items():
            try:
                if param_key in data and data[param_key] is not None:
                    value = float(data[param_key])
                    camera_params[system_param] = value
            except (ValueError, TypeError):
                logging.warning(f"Invalid value for {param_key}: {data.get(param_key)}")

        if camera_params:
            camera.set_controls(camera_params)
            logging.info(f"Camera settings updated: {camera_params}")
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': "No valid settings provided"}), 400

    except Exception as error:
        logging.error(f"Error in update_parameters: {error}")
        return jsonify({'success': False, 'error': str(error)}), 500
