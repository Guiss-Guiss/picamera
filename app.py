from flask import Flask, render_template, jsonify, request, Response
from config.configuration import CONFIG
from noyau.journalisation import configurer_journalisation
from gestionnaires.capture import capturer, demarrer_capture_auto, arreter_capture_auto
from gestionnaires.flux import demarrer_flux, arreter_flux, generer_images
from gestionnaires.parametres import obtenir_parametres, mettre_a_jour_parametres
from gestionnaires.photos import api_photos, supprimer_photo
import atexit

# Initialisation de l'application Flask
app = Flask(__name__)

# Chargement de la configuration
app.config.update(CONFIG)

# Configuration de la journalisation
configurer_journalisation()

# Routes principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/galerie')
def galerie():
    return render_template('galerie.html')

@app.route('/flux')
def flux():
    """Route pour le flux vidéo"""
    return Response(
        generer_images(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/arreter_flux')
def route_arreter_flux():
    """Route pour arrêter le flux vidéo"""
    resultat = arreter_flux()
    return jsonify(resultat)

@app.route('/capture', methods=['POST'])
def route_capturer():
    return capturer()

@app.route('/demarrer_capture_auto', methods=['POST'])
def route_demarrer_capture_auto():
    return demarrer_capture_auto(request.json)

@app.route('/arreter_capture_auto')
def route_arreter_capture_auto():
    return arreter_capture_auto()

@app.route('/parametres', methods=['GET', 'POST'])
def route_parametres():
    if request.method == 'GET':
        return obtenir_parametres()
    elif request.method == 'POST':
        return mettre_a_jour_parametres(request.json)

@app.route('/photos')
def route_api_photos():
    return api_photos()

@app.route('/supprimer', methods=['POST'])
def route_supprimer_photo():
    return supprimer_photo(request.json)

# Gestion des erreurs
@app.errorhandler(404)
def erreur_non_trouve(erreur):
    return jsonify({'succes': False, 'erreur': 'Ressource non trouvée'}), 404

@app.errorhandler(500)
def erreur_interne(erreur):
    return jsonify({'succes': False, 'erreur': 'Erreur interne du serveur'}), 500

# Nettoyage à la sortie
atexit.register(lambda: print("Nettoyage des ressources"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
