# 📸 PiCamera Web Interface

A web interface to control a Raspberry Pi camera using Python Flask and picamera2.

## ✨ Features

- 🎥 Live video streaming
- 📷 Photo capture with adjustable settings
- ⏱️ Automatic capture sequences
- 🖼️ Photo gallery management
- 🎛️ Camera settings control (exposure, gain, brightness, etc.)

## 📋 Prerequisites


### 🤖 [Raspberry Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)

### 📷 [Raspberry Pi Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/), or
### 📷 [Raspberry Pi HQ Camera](https://www.raspberrypi.com/products/raspberry-pi-high-quality-camera/)
### 🏠 [Case (3D print)](https://www.printables.com/model/1090727-case-for-raspberry-pi-zero-2w-and-camera-module-3)



- 💾 Raspberry Pi OS Lite (64-bit)
- 🐍 Python 3.x
- 🌐 Web browser

## 🛠️ Installation

1. 💽 Flash Raspberry Pi OS with Raspberry Pi Imager
   - Enable SSH during configuration

2. 🔄 Update the system and expand the filesystem
```bash
ssh pi@raspberry_pi_ip_address
sudo raspi-config # Go to Advanced Options and choose Expand Filesystem
sudo apt update && sudo apt upgrade -y
sudo apt install python3-picamera2 python3-flask git -y
```

3. 📥 Clone the repository
```bash
git clone https://github.com/Guiss-Guiss/picamera.git
cd picamera
```

## 🚀 Auto-start Configuration

1. ⚙️ Create the systemd service file:
```bash
sudo nano /etc/systemd/system/picamera.service
```

2. 📝 Add the following content:
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

3. ▶️ Enable and start the service:
```bash
sudo systemctl enable picamera.service
sudo systemctl start picamera.service
```

## 📖 Usage

1. 🌐 Access the interface at `http://raspberry-pi-ip:5001`
2. 🎮 Use the controls to:
   - 📸 Capture photos
   - ⏱️ Configure automatic capture sequences
   - 🎛️ Adjust camera settings
   - 🖼️ View and manage captured photos



## 🤝 Contributing

1. 🔀 Fork the repository
2. 🌿 Create a branch for your feature
3. ✅ Commit your changes
4. ⬆️ Push to the branch
5. 📩 Create a Pull Request

## 📜 License

This project is licensed under the MIT License.
