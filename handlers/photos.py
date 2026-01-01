import os
import logging
from flask import jsonify, url_for

PHOTOS_FOLDER = 'static/media'

def get_photos():
    """Retrieves the list of photo files in a specific directory."""
    try:
        return [
            f for f in os.listdir(PHOTOS_FOLDER)
            if os.path.isfile(os.path.join(PHOTOS_FOLDER, f))
            and f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]
    except Exception as e:
        logging.error(f"Error retrieving photos: {e}")
        return []

def api_photos():
    """Returns the list of captured photos."""
    try:
        files = []
        for filename in get_photos():
            file_path = os.path.join(PHOTOS_FOLDER, filename)
            files.append({
                'filename': filename,
                'path': url_for('static', filename=f'media/{filename}', _external=True),
                'date': os.path.getctime(file_path)
            })

        sorted_files = sorted(files, key=lambda x: x['date'], reverse=True)
        return jsonify({
            'success': True,
            'photos': sorted_files
        })
    except Exception as e:
        logging.error(f"Error in api_photos: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'photos': []
        })

def delete_photo(data):
    """Deletes a specified photo."""
    try:
        filename = data.get('filename')
        if not filename:
            return jsonify({'success': False, 'error': "Missing filename"}), 400

        file_path = os.path.join(PHOTOS_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': "File not found"}), 404

        os.remove(file_path)
        logging.info(f"Photo deleted: {filename}")
        return jsonify({'success': True}), 200
    except Exception as e:
        logging.error(f"Error in delete_photo: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
