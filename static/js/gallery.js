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

        if (!result.success) {
            showNotification('Error loading gallery', 'error');
            return;
        }

        const photos = result.photos;

        if (photos.length === 0) {
            gallery.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">No photos available</p>';
            return;
        }

        photos.forEach(photo => {
            const div = document.createElement('div');
            div.className = 'grid-item';
            div.innerHTML = `
                <div class="image-container">
                    <img src="${photo.path}"
                         alt="Photo taken on ${formatDate(photo.date)}"
                         loading="lazy"
                         title="Photo taken on ${formatDate(photo.date)}">
                </div>
                <div class="image-controls">
                    <span class="image-info">Taken on ${formatDate(photo.date)}</span>
                    <button onclick="deletePhoto('${photo.filename}')" class="btn-supprimer">
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
        const result = await request('/delete', 'POST', { filename });
        if (result.success) {
            showNotification('Photo deleted successfully');
            loadGallery();
        } else {
            showNotification('Failed to delete photo', 'error');
        }
    } catch (error) {
        showNotification('Failed to delete photo', 'error');
        console.error('Delete error:', error);
    }
}

function handleImageError(img) {
    img.onerror = null;
    img.src = '/static/images/error-image.png';
    showNotification('Error loading some images', 'error');
}

document.addEventListener('DOMContentLoaded', () => {
    loadGallery();
});
