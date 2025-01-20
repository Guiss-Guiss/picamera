import os

# Définir le chemin de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configuration globale
DOSSIER_UPLOAD = os.path.join(BASE_DIR, '..', 'static', 'media')
TAILLE_MAX_CONTENU = 16 * 1024 * 1024  # 16 Mo
DOSSIER_LOGS = os.path.join(BASE_DIR, '..', 'logs')
TAILLE_MAX_LOG = 10 * 1024 * 1024  # 10 Mo
NOMBRE_BACKUP_LOGS = 5  # Nombre de fichiers de sauvegarde

CONFIG = {
    'DOSSIER_UPLOAD': DOSSIER_UPLOAD,
    'TAILLE_MAX_CONTENU': TAILLE_MAX_CONTENU,
    'DOSSIER_LOGS': DOSSIER_LOGS,
    'TAILLE_MAX_LOG': TAILLE_MAX_LOG,
    'NOMBRE_BACKUP_LOGS': NOMBRE_BACKUP_LOGS
}

# Exportation explicite
__all__ = ['DOSSIER_UPLOAD', 'TAILLE_MAX_CONTENU', 'DOSSIER_LOGS', 'TAILLE_MAX_LOG', 'NOMBRE_BACKUP_LOGS', 'CONFIG']
