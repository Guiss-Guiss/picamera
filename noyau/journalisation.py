from config.configuration import CONFIG
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def configurer_journalisation():
    """Configuration du système de journalisation avec gestionnaires de fichiers et console."""
    formateur = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s'
    )

    gestionnaire_fichier = RotatingFileHandler(
        os.path.join(CONFIG['DOSSIER_LOGS'], 'app_camera.log'),
        maxBytes=CONFIG['TAILLE_MAX_LOG'],
        backupCount=CONFIG['NOMBRE_BACKUP_LOGS']
    )
    gestionnaire_fichier.setFormatter(formateur)
    gestionnaire_fichier.setLevel(logging.DEBUG)

    gestionnaire_console = logging.StreamHandler(sys.stdout)
    gestionnaire_console.setFormatter(formateur)
    gestionnaire_console.setLevel(logging.INFO)

    gestionnaire_erreurs = RotatingFileHandler(
        os.path.join(CONFIG['DOSSIER_LOGS'], 'erreurs.log'),
        maxBytes=CONFIG['TAILLE_MAX_LOG'],
        backupCount=CONFIG['NOMBRE_BACKUP_LOGS']
    )
    gestionnaire_erreurs.setFormatter(formateur)
    gestionnaire_erreurs.setLevel(logging.ERROR)

    logger_racine = logging.getLogger()
    logger_racine.setLevel(logging.DEBUG)
    for gestionnaire in [gestionnaire_fichier, gestionnaire_console, gestionnaire_erreurs]:
        logger_racine.addHandler(gestionnaire)
