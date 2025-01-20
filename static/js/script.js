let flux_actif = false;

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

function demarrerFlux() {
    const img = document.getElementById('flux');
    img.src = `/flux?t=${Date.now()}`;
    flux_actif = true;
    
    img.onerror = () => {
        if (flux_actif) {
            setTimeout(() => {
                img.src = `/flux?t=${Date.now()}`;
            }, 1000);
        }
    };
}

function arreterFlux() {
    if (flux_actif) {
        requete('/arreter_flux')
            .then(() => {
                flux_actif = false;
                const img = document.getElementById('flux');
                img.src = '';
            })
            .catch(erreur => {
                console.error('Erreur lors de l\'arrêt du flux:', erreur);
                afficherNotification('Erreur lors de l\'arrêt du flux', 'error');
            });
    }
}

async function capturerPhoto() {
    try {
        const response = await requete('/capture', 'POST');
        if (response.succes) {
            afficherNotification('Photo capturée avec succès');
        }
    } catch (erreur) {
        afficherNotification('Échec de la capture', 'error');
        console.error('Erreur de capture:', erreur);
    }
}

async function mettreAJourParametres() {
    try {
        const donnees = {
            exposition: parseInt(document.getElementById('exposure').value),
            gain: parseFloat(document.getElementById('gain').value),
            luminosite: parseFloat(document.getElementById('brightness').value),
            contraste: parseFloat(document.getElementById('contrast').value),
            saturation: parseFloat(document.getElementById('saturation').value),
            nettete: parseFloat(document.getElementById('sharpness').value)
        };

        await requete('/parametres', 'POST', donnees);
        afficherNotification('Paramètres mis à jour avec succès');
    } catch (erreur) {
        afficherNotification('Échec de la mise à jour des paramètres', 'error');
        console.error('Erreur de mise à jour des paramètres:', erreur);
    }
}

async function chargerParametres() {
    try {
        const parametres = await requete('/parametres');
        if (parametres) {
            document.getElementById('exposure').value = parametres.exposition || 16000;
            document.getElementById('gain').value = parametres.gain || 1.0;
            document.getElementById('brightness').value = parametres.luminosite || 0;
            document.getElementById('contrast').value = parametres.contraste || 1.0;
            document.getElementById('saturation').value = parametres.saturation || 1.0;
            document.getElementById('sharpness').value = parametres.nettete || 1.0;
            
            document.getElementById('gainValue').textContent = parametres.gain?.toFixed(1) || '1.0';
            document.getElementById('brightnessValue').textContent = parametres.luminosite?.toFixed(1) || '0.0';
            document.getElementById('contrastValue').textContent = parametres.contraste?.toFixed(1) || '1.0';
            document.getElementById('saturationValue').textContent = parametres.saturation?.toFixed(1) || '1.0';
            document.getElementById('sharpnessValue').textContent = parametres.nettete?.toFixed(1) || '1.0';
        }
    } catch (erreur) {
        afficherNotification('Échec du chargement des paramètres', 'error');
        console.error('Erreur de chargement des paramètres:', erreur);
    }
}

async function demarrerCaptureAuto() {
    try {
        const intervalle = parseInt(document.getElementById('interval').value);
        const duree = parseInt(document.getElementById('duration').value);
        
        if (intervalle < 5) {
            afficherNotification('L\'intervalle minimum est de 5 secondes', 'error');
            return;
        }
        
        await requete('/demarrer_capture_auto', 'POST', { intervalle, duree });
        afficherNotification('Capture automatique démarrée');
    } catch (erreur) {
        afficherNotification('Échec du démarrage de la capture automatique', 'error');
        console.error('Erreur de démarrage de la capture auto:', erreur);
    }
}

async function arreterCaptureAuto() {
    try {
        await requete('/arreter_capture_auto');
        afficherNotification('Capture automatique arrêtée');
    } catch (erreur) {
        afficherNotification('Échec de l\'arrêt de la capture automatique', 'error');
        console.error('Erreur d\'arrêt de la capture auto:', erreur);
    }
}

function basculerParametres() {
    const panneau = document.getElementById('settingsPanel');
    panneau.style.display = panneau.style.display === 'none' ? 'block' : 'none';
}

function basculerCaptureAuto() {
    const panneau = document.getElementById('autoCapturePanel');
    panneau.style.display = panneau.style.display === 'none' ? 'block' : 'none';
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
        const images = await requete('/photos');
        const galerie = document.getElementById('gallery');
        galerie.innerHTML = '';
        
        if (images.length === 0) {
            galerie.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">Aucune photo disponible</p>';
            return;
        }
        
        images.forEach(image => {
            const div = document.createElement('div');
            div.className = 'grid-item';
            div.innerHTML = `
                <img src="${image.chemin}" 
                     alt="Photo prise le ${formatDate(image.date)}" 
                     loading="lazy"
                     title="Photo prise le ${formatDate(image.date)}">
                <div class="image-overlay">
                    <button onclick="supprimerPhoto('${image.nom_fichier}')" class="btn btn-rouge">
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
        await requete('/supprimer', 'POST', { nom_fichier });
        afficherNotification('Photo supprimée avec succès');
        chargerGalerie();
    } catch (erreur) {
        afficherNotification('Échec de la suppression de la photo', 'error');
        console.error('Erreur de suppression:', erreur);
    }
}

window.onload = () => {
    chargerParametres();
    demarrerFlux();
};

window.onbeforeunload = () => {
    arreterFlux();
};