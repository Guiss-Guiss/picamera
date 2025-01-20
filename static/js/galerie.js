async function requete(url, methode = 'GET', donnees = null) {
    try {
        const options = {
            method: methode,
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };
        
        if (donnees) {
            options.body = JSON.stringify(donnees);
        }

        const reponse = await fetch(url, options);
        
        if (!reponse.ok) {
            throw new Error(`Erreur HTTP! statut: ${reponse.status}`);
        }
        
        return await reponse.json();
    } catch (erreur) {
        afficherNotification(erreur.message, 'error');
        throw erreur;
    }
}

function afficherNotification(message, type = 'success') {
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
    return date.toLocaleDateString('fr-FR', options);
}
async function chargerGalerie() {
    try {
        const resultat = await requete('/photos');
        const galerie = document.getElementById('gallery');
        galerie.innerHTML = '';
        
        if (!resultat.succes) {
            afficherNotification('Erreur lors du chargement de la galerie', 'error');
            return;
        }

        const photos = resultat.photos;
        
        if (photos.length === 0) {
            galerie.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">Aucune photo disponible</p>';
            return;
        }
        
        photos.forEach(photo => {
            const div = document.createElement('div');
            div.className = 'grid-item';
            div.innerHTML = `
                <div class="image-container">
                    <img src="${photo.chemin}" 
                         alt="Photo prise le ${formatDate(photo.date)}" 
                         loading="lazy"
                         title="Photo prise le ${formatDate(photo.date)}">
                </div>
                <div class="image-controls">
                    <span class="image-info">Prise le ${formatDate(photo.date)}</span>
                    <button onclick="supprimerPhoto('${photo.nom_fichier}')" class="btn-supprimer">
                        Supprimer
                    </button>
                </div>
            `;
            galerie.appendChild(div);
        });
    } catch (erreur) {
        afficherNotification('Échec du chargement de la galerie', 'error');
        console.error('Erreur de chargement de la galerie:', erreur);
    }
}

async function supprimerPhoto(nom_fichier) {
    if (!confirm('Voulez-vous vraiment supprimer cette photo ?')) {
        return;
    }

    try {
        const resultat = await requete('/supprimer', 'POST', { nom_fichier });
        if (resultat.succes) {
            afficherNotification('Photo supprimée avec succès');
            chargerGalerie();
        } else {
            afficherNotification('Échec de la suppression de la photo', 'error');
        }
    } catch (erreur) {
        afficherNotification('Échec de la suppression de la photo', 'error');
        console.error('Erreur de suppression:', erreur);
    }
}

function gererErreurImage(img) {
    img.onerror = null;
    img.src = '/static/images/error-image.png';
    afficherNotification('Erreur de chargement de certaines images', 'error');
}

document.addEventListener('DOMContentLoaded', () => {
    chargerGalerie();
});