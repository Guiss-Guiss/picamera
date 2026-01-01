let streamActive = false;

async function request(url, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);

        if (!response.ok) {
            throw new Error(`HTTP Error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        showNotification(error.message, 'error');
        throw error;
    }
}

function showNotification(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast toast-${type}`;
    toast.style.display = 'block';

    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

function startStream() {
    const img = document.getElementById('stream');
    img.src = `/stream?t=${Date.now()}`;
    streamActive = true;

    img.onerror = () => {
        if (streamActive) {
            setTimeout(() => {
                img.src = `/stream?t=${Date.now()}`;
            }, 1000);
        }
    };
}

function stopStream() {
    if (streamActive) {
        request('/stop_stream')
            .then(() => {
                streamActive = false;
                const img = document.getElementById('stream');
                img.src = '';
            })
            .catch(error => {
                console.error('Error stopping stream:', error);
                showNotification('Error stopping stream', 'error');
            });
    }
}

async function capturePhoto() {
    try {
        const response = await request('/capture', 'POST');
        if (response.success) {
            showNotification('Photo captured successfully');
        }
    } catch (error) {
        showNotification('Capture failed', 'error');
        console.error('Capture error:', error);
    }
}

async function updateParameters() {
    try {
        const data = {
            exposure: parseInt(document.getElementById('exposure').value),
            gain: parseFloat(document.getElementById('gain').value),
            brightness: parseFloat(document.getElementById('brightness').value),
            contrast: parseFloat(document.getElementById('contrast').value),
            saturation: parseFloat(document.getElementById('saturation').value),
            sharpness: parseFloat(document.getElementById('sharpness').value)
        };

        await request('/parameters', 'POST', data);
        showNotification('Settings updated successfully');
    } catch (error) {
        showNotification('Failed to update settings', 'error');
        console.error('Settings update error:', error);
    }
}

async function loadParameters() {
    try {
        const result = await request('/parameters');
        if (result && result.parameters) {
            const parameters = result.parameters;
            document.getElementById('exposure').value = parameters.exposure || 16000;
            document.getElementById('gain').value = parameters.gain || 1.0;
            document.getElementById('brightness').value = parameters.brightness || 0;
            document.getElementById('contrast').value = parameters.contrast || 1.0;
            document.getElementById('saturation').value = parameters.saturation || 1.0;
            document.getElementById('sharpness').value = parameters.sharpness || 1.0;

            document.getElementById('gainValue').textContent = parameters.gain?.toFixed(1) || '1.0';
            document.getElementById('brightnessValue').textContent = parameters.brightness?.toFixed(1) || '0.0';
            document.getElementById('contrastValue').textContent = parameters.contrast?.toFixed(1) || '1.0';
            document.getElementById('saturationValue').textContent = parameters.saturation?.toFixed(1) || '1.0';
            document.getElementById('sharpnessValue').textContent = parameters.sharpness?.toFixed(1) || '1.0';
        }
    } catch (error) {
        showNotification('Failed to load settings', 'error');
        console.error('Settings load error:', error);
    }
}

async function startAutoCapture() {
    try {
        const interval = parseInt(document.getElementById('interval').value);
        const duration = parseInt(document.getElementById('duration').value);

        if (interval < 5) {
            showNotification('Minimum interval is 5 seconds', 'error');
            return;
        }

        await request('/start_auto_capture', 'POST', { interval, duration });
        showNotification('Automatic capture started');
    } catch (error) {
        showNotification('Failed to start automatic capture', 'error');
        console.error('Auto capture start error:', error);
    }
}

async function stopAutoCapture() {
    try {
        await request('/stop_auto_capture');
        showNotification('Automatic capture stopped');
    } catch (error) {
        showNotification('Failed to stop automatic capture', 'error');
        console.error('Auto capture stop error:', error);
    }
}

function toggleSettings() {
    const panel = document.getElementById('settingsPanel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
}

function toggleAutoCapture() {
    const panel = document.getElementById('autoCapturePanel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
}

function formatDate(timestamp) {
    const date = new Date(timestamp * 1000);
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return date.toLocaleDateString('en-US', options);
}

async function loadGallery() {
    try {
        const result = await request('/photos');
        const gallery = document.getElementById('gallery');
        gallery.innerHTML = '';

        if (!result.success || result.photos.length === 0) {
            gallery.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">No photos available</p>';
            return;
        }

        result.photos.forEach(photo => {
            const div = document.createElement('div');
            div.className = 'grid-item';
            div.innerHTML = `
                <img src="${photo.path}"
                     alt="Photo taken on ${formatDate(photo.date)}"
                     loading="lazy"
                     title="Photo taken on ${formatDate(photo.date)}">
                <div class="image-overlay">
                    <button onclick="deletePhoto('${photo.filename}')" class="btn btn-rouge">
                        Delete
                    </button>
                </div>
            `;
            gallery.appendChild(div);
        });
    } catch (error) {
        showNotification('Failed to load gallery', 'error');
        console.error('Gallery load error:', error);
    }
}

async function deletePhoto(filename) {
    if (!confirm('Are you sure you want to delete this photo?')) {
        return;
    }

    try {
        await request('/delete', 'POST', { filename });
        showNotification('Photo deleted successfully');
        loadGallery();
    } catch (error) {
        showNotification('Failed to delete photo', 'error');
        console.error('Delete error:', error);
    }
}

window.onload = () => {
    loadParameters();
    startStream();
};

window.onbeforeunload = () => {
    stopStream();
};
