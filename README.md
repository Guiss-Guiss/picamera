# 📸 Interface Web PiCamera

Une interface web pour contrôler une caméra Raspberry Pi utilisant Python Flask et picamera2.

## ✨ Fonctionnalités

- 🎥 Streaming vidéo en direct
- 📷 Capture de photos avec paramètres ajustables
- ⏱️ Séquences de capture automatique
- 🖼️ Gestion de galerie photos
- 🎛️ Contrôle des paramètres de la caméra (exposition, gain, luminosité, etc.)

## 📋 Prérequis


### 🤖 [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)

### 📷 [Raspberry Pi Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/)

### 🏠 [Boîtier (impression 3D)](https://www.printables.com/model/1090727-case-for-raspberry-pi-zero-2w-and-camera-module-3)



- 💾 Raspberry Pi OS Lite (64-bit)
- 🐍 Python 3.x
- 🌐 Navigateur web

## 🛠️ Installation

1. 💽 Flasher Raspberry Pi OS avec Raspberry Pi Imager
   - Activer SSH pendant la configuration

2. 🔄 Mettre à jour le système et étendre le système de fichiers
```bash
ssh pi@adresse_ip_du_raspberry_pi
sudo raspi-config >> Options avancées >> Expand Filesystem
sudo apt update && sudo apt upgrade -y
sudo apt install python3-picamera2 python3-flask -y
```

3. 📥 Cloner le dépôt
```bash
git clone https://github.com/Guiss-Guiss/picamera.git
cd picamera
```

## 🚀 Configuration du démarrage automatique

1. ⚙️ Créer le fichier de service systemd :
```bash
sudo nano /etc/systemd/system/picamera.service
```

2. 📝 Ajouter le contenu suivant :
```ini
[Unit]
Description=PiCamera
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/picamera
Environment=PYTHONPATH=/home/pi/picamera
ExecStart=/usr/bin/python3 /home/pi/picamera/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. ▶️ Activer et démarrer le service :
```bash
sudo systemctl enable picamera.service
sudo systemctl start picamera.service
```

## 📖 Utilisation

1. 🌐 Accéder à l'interface via `http://ip-du-raspberry-pi:5001`
2. 🎮 Utiliser les contrôles pour :
   - 📸 Capturer des photos
   - ⏱️ Configurer des séquences de capture automatique
   - 🎛️ Ajuster les paramètres de la caméra
   - 🖼️ Visualiser et gérer les photos capturées



## 🤝 Contribution

1. 🔀 Forker le dépôt
2. 🌿 Créer une branche pour votre fonctionnalité
3. ✅ Commiter vos changements
4. ⬆️ Pousser vers la branche
5. 📩 Créer une Pull Request

## 📜 Licence

Ce projet est sous licence MIT.
