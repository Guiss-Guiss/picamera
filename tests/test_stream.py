import pytest
from app import app
from handlers.stream import start_stream, stop_stream

@pytest.fixture
def app_context():
    """Creates a Flask application context for tests."""
    with app.app_context():
        yield

def test_start_stream(app_context, mock_camera):
    """Tests starting the video stream."""
    response = start_stream()

    assert response['success'], "Video stream start failed"

def test_stop_stream(app_context, mock_camera):
    """Tests stopping the video stream."""
    response = stop_stream()

    assert response['success'], "Video stream stop failed"
    if mock_camera.started:
        mock_camera.stop_recording.assert_called_once()

def test_stream_route_exists(app_context, mock_camera):
    """Tests the stream route is registered."""
    # Check the route is registered in the app
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    assert '/stream' in rules, "Stream route should be registered"
