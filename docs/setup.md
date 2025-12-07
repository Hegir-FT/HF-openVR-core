# Настройка VR системы на Orange Pi 5

## Оглавление
1. [Требования к системе](https://github.com/Hegir-FT/HF-openVR-core/blob/main/software/setup.md#1-%D1%82%D1%80%D0%B5%D0%B1%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F-%D0%BA-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B5)
2. [Базовая настройка Orange Pi 5](https://github.com/Hegir-FT/HF-openVR-core/blob/main/software/setup.md#2-%D0%B1%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D1%8F-%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0-orange-pi-5-%D0%B1%D0%B0%D0%B7%D0%BE%D0%B2%D0%B0%D1%8F-%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0)
3. [Настройка дисплеев](https://github.com/Hegir-FT/HF-openVR-core/blob/main/software/setup.md#3-%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0-%D0%B4%D0%B8%D1%81%D0%BF%D0%BB%D0%B5%D0%B5%D0%B2-%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0-%D0%B4%D0%B8%D1%81%D0%BF%D0%BB%D0%B5%D0%B5%D0%B2)
4. [Установка VR окружения](https://github.com/Hegir-FT/HF-openVR-core/blob/main/software/setup.md#4-%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-vr-%D0%BE%D0%BA%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F-vr-%D0%BE%D0%BA%D1%80%D1%83%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5)
5. [Средства разработки](https://github.com/Hegir-FT/HF-openVR-core/blob/main/software/setup.md#5-%D1%81%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B2%D0%B0-%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8-%D1%81%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B2%D0%B0-%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8)
6. [Оптимизация для VR](https://github.com/Hegir-FT/HF-openVR-core/blob/main/software/setup.md#6-%D0%BE%D0%BF%D1%82%D0%B8%D0%BC%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F-%D0%B4%D0%BB%D1%8F-vr-%D0%BE%D0%BF%D1%82%D0%B8%D0%BC%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F)
7. [Настройка звука](https://github.com/Hegir-FT/HF-openVR-core/blob/main/software/setup.md#7-%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0-%D0%B7%D0%B2%D1%83%D0%BA%D0%B0-%D0%B7%D0%B2%D1%83%D0%BA)
8. [Инструменты разработки](https://github.com/Hegir-FT/HF-openVR-core/blob/main/software/setup.md#8-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B-%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B8-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B)
9. [Резервное копирование](https://github.com/Hegir-FT/HF-openVR-core/blob/main/software/setup.md#9-%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B5-%D0%BA%D0%BE%D0%BF%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D1%80%D0%B5%D0%B7%D0%B5%D1%80%D0%B2%D0%BD%D0%BE%D0%B5-%D0%BA%D0%BE%D0%BF%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5)
10. [Дополнительные инструменты](https://github.com/Hegir-FT/HF-openVR-core/blob/main/software/setup.md#10-%D0%B4%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B-%D0%B4%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5-%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B)
11. [Проверка системы](https://github.com/Hegir-FT/HF-openVR-core/blob/main/software/setup.md#11-%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%8B-%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0)

---

# 1. Требования к системе 

### Аппаратные требования:
- Orange Pi 5 (8GB RAM или 16GB)
- 2 дисплея 5.5-7" с HDMI входом
- Power Bank 20000mAh с PD 12V
- MicroSD карта 64GB+ (или eMMC модуль)
- Клавиатура и мышь для начальной настройки

### Программные требования:
- Armbian 23.08 или новее
- Доступ в интернет (Wi-Fi/Ethernet)
- Базовые знания Linux

### Проверка перед началом:

### Убедитесь, что Orange Pi 5 загружается
sudo systemctl is-system-running

### Проверьте версию ОС
cat /etc/os-release

### Проверьте свободное место
df -h 2
# 2. Базовая настройка Orange Pi 5 {#базовая-настройка}
### 2.1 Первый запуск и обновление

### Логин по умолчанию (первые 3 минуты после установки):
### Логин: root
### Пароль: 1234

### Создайте обычного пользователя
adduser vruser
usermod -aG sudo vruser

### Обновите систему
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget build-essential

### Установите необходимые утилиты
sudo apt install -y htop neofetch screen tmux
## 2.2 Настройка сети

### Настройка Wi-Fi (если нужно)
sudo nmtui

### Статический IP (рекомендуется для VR)
sudo nano /etc/netplan/01-netcfg.yaml
### Добавьте:
network:
  version: 2
  ethernets:
    eth0:
      dhcp4: no
      addresses: [192.168.1.100/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]

### Применить настройки
sudo netplan apply
## 2.3 Настройка SSH

### Установите SSH сервер
sudo apt install -y openssh-server

### Настройка безопасности
sudo nano /etc/ssh/sshd_config
### Измените:
Port 2222
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes

### Создайте SSH ключ на клиенте
ssh-keygen -t ed25519 -C "vr@orangepi5"

### Скопируйте ключ на Orange Pi 5
ssh-copy-id -p 2222 vruser@192.168.1.100

### Перезапустите SSH
sudo systemctl restart sshd
# 3. Настройка дисплеев {#настройка-дисплеев}
## 3.1 Базовая конфигурация

### Отредактируйте конфигурацию Orange Pi 5
sudo nano /boot/orangepiEnv.txt

### Добавьте или измените:
overlays=hdmi0 hdmi1
param_hdmi0_edid=1
param_hdmi1_edid=1
hdmi0_output_mode=1920x1080p60
hdmi1_output_mode=1920x1080p60
hdmi0_hpd=0
hdmi1_hpd=0
hdmi0_ddc=1
hdmi1_ddc=1

### Сохраните и перезагрузите
sudo reboot
## 3.2 Проверка дисплеев

### После перезагрузки проверьте
xrandr --query
### Должны быть HDMI-1 и HDMI-2

### Тест обоих дисплеев
xrandr --output HDMI-1 --primary --mode 1920x1080 --pos 0x0 \
       --output HDMI-2 --mode 1920x1080 --pos 1920x0
## 3.3 Автоматическая настройка при загрузке

### Создайте скрипт настройки
sudo nano /usr/local/bin/setup-displays.sh

###!/bin/bash
sleep 5  # Ждем инициализации дисплеев
xrandr --output HDMI-1 --primary --mode 1920x1080 --pos 0x0
xrandr --output HDMI-2 --mode 1920x1080 --pos 1920x0
exit 0

### Сделайте исполняемым
sudo chmod +x /usr/local/bin/setup-displays.sh

### Добавьте в автозагрузку
sudo nano /etc/xdg/autostart/vr-displays.desktop

[Desktop Entry]
Type=Application
Name=VR Display Setup
Exec=/usr/local/bin/setup-displays.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
## 3.4 Калибровка дисплеев

### Установите инструменты калибровки
sudo apt install -y xcalib argyll

### Калибровка цветов (если дисплеи отличаются)
dispcal -v -yl -t 6500 -g 2.2

### Настройка гаммы
xgamma -gamma 2.2

### Выравнивание яркости
xrandr --output HDMI-1 --brightness 1.0
xrandr --output HDMI-2 --brightness 1.0
# 4. Установка VR окружения {#vr-окружение}
## 4.1 Установка OpenGL и графических драйверов

### Для Mali-G610 GPU
sudo apt install -y mesa-utils libgl1-mesa-dri libgl1-mesa-glx
sudo apt install -y libgles2-mesa libgles2-mesa-dev

### Установка драйверов Rockchip
sudo add-apt-repository ppa:liujianfeng1994/rockchip-multimedia
sudo apt update
sudo apt install -y rockchip-multimedia-config

### Проверка OpenGL
glxinfo | grep "OpenGL version"
glmark2-es2 --fullscreen
4.2 Установка OpenXR (Monado)

### Установите зависимости
sudo apt install -y cmake ninja-build pkg-config libxrandr-dev \
libxxf86vm-dev libxinerama-dev libxcursor-dev libudev-dev \
libvulkan-dev libwayland-dev libjpeg-dev libopenexr-dev \
libeigen3-dev libcjson-dev

### Клонируйте Monado
git clone https://gitlab.freedesktop.org/monado/monado.git
cd monado

### Сборка
mkdir build && cd build
cmake .. -DBUILD_DEPENDENCIES=ON
make -j$(nproc)
sudo make install

### Проверка установки
monado-service --help

## 4.3 Настройка Monado для DIY VR шлема

### Создайте конфигурационный файл
mkdir -p ~/.config/monado
nano ~/.config/monado/services.json

{
  "trackers": [
    {
      "name": "head",
      "driver": "mock",
      "position": [0, 1.6, 0],
      "orientation": [1, 0, 0, 0]
    }
  ],
  "hmds": [
    {
      "name": "hf-vr-helmet",
      "driver": "screen",
      "tracker": "head",
      "screen": {
        "display": 0,
        "viewport": [0, 0, 1920, 1080]
      }
    },
    {
      "name": "hf-vr-helmet-right",
      "driver": "screen",
      "tracker": "head",
      "screen": {
        "display": 1,
        "viewport": [0, 0, 1920, 1080]
      }
    }
  ]
}

### Запустите службу Monado
monado-service &
## 4.4 Установка OpenVR/SteamVR драйвера (опционально)

### Для совместимости со SteamVR
git clone https://github.com/ValveSoftware/SteamVR-for-Linux.git
cd SteamVR-for-Linux

### Установите зависимости
sudo apt install -y libusb-1.0-0-dev libudev-dev libvulkan-dev

### Сборка
mkdir build && cd build
cmake ..
make -j$(nproc)

### Установка
sudo make install
# 5. Средства разработки {#средства-разработки}
## 5.1 Установка Godot Engine

### Скачайте Godot для ARM64
wget https://github.com/godotengine/godot/releases/download/4.2-stable/Godot_v4.2-stable_linux.x86_64.zip

### Распакуйте
unzip Godot_v4.2-stable_linux.x86_64.zip
sudo mv Godot_v4.2-stable_linux.x86_64 /usr/local/bin/godot

### Создайте ярлык
sudo nano /usr/share/applications/godot.desktop

[Desktop Entry]
Type=Application
Name=Godot Engine
Exec=godot
Icon=/usr/local/bin/godot/icon.png
Terminal=false
Categories=Development;

### Проверьте установку
godot --version
## 5.2 Установка Unity Hub (через Box64)

### Установите Box64 для эмуляции x86_64
git clone https://github.com/ptitSeb/box64
cd box64
mkdir build && cd build
cmake .. -DRK3588=1 -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j$(nproc)
sudo make install

### Загрузите Unity Hub
wget https://public-cdn.cloud.unity3d.com/hub/prod/UnityHub.AppImage

### Сделайте исполняемым
chmod +x UnityHub.AppImage

### Запуск через Box64
box64 ./UnityHub.AppImage
## 5.3 Установка Python и библиотек VR

### Установите Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev

### Создайте виртуальное окружение
python3.11 -m venv ~/vr-venv
source ~/vr-venv/bin/activate

### Установите VR библиотеки
pip install openvr pyopengl pygame numpy opencv-python

### Установите Jupyter для экспериментов
pip install jupyter matplotlib ipywidgets

### Создайте ярлык для запуска
nano ~/Desktop/vr-python.desktop

[Desktop Entry]
Type=Application
Name=VR Python Environment
Exec=bash -c "source ~/vr-venv/bin/activate && jupyter notebook"
Icon=python
# 6. Оптимизация для VR {#оптимизация}
## 6.1 Настройка ядра для низкой задержки

### Установите ядро с низкой задержкой
sudo apt install -y linux-image-lowlatency

### Настройте параметры ядра
sudo nano /etc/default/grub
### Добавьте к GRUB_CMDLINE_LINUX_DEFAULT:
threadirqs isolcpus=2,3 nohz_full=2,3 rcu_nocbs=2,3

### Обновите GRUB
sudo update-grub

### Настройте планировщик в реальном времени
sudo nano /etc/security/limits.conf
### Добавьте:
@vr-user - rtprio 99
@vr-user - memlock unlimited
@vr-user - nice -20

### Создайте группу
sudo groupadd vr-user
sudo usermod -aG vr-user vruser

## 6.2 Оптимизация GPU

### Настройка частоты GPU
sudo nano /etc/default/orangepi5-gpu

### Добавьте:
GPU_MIN_FREQ=400000000
GPU_MAX_FREQ=1000000000
GPU_GOVERNOR=performance

### Создайте скрипт для управления GPU
sudo nano /usr/local/bin/gpu-optimize.sh

# !/bin/bash
- echo performance | sudo tee /sys/devices/platform/ffe40000.gpu/devfreq/ffe40000.gpu/governor
- echo 1000000000 | sudo tee /sys/devices/platform/ffe40000.gpu/devfreq/ffe40000.gpu/max_freq

### Сделайте исполняемым
sudo chmod +x /usr/local/bin/gpu-optimize.sh
# 6.3 Оптимизация памяти и swap

### Увеличьте размер swap
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

### Добавьте в fstab
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

### Настройка swappiness
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
# 7. Настройка звука {#звук}
## 7.1 Установка PulseAudio с HRTF

### Установите PulseAudio и плагины
sudo apt install -y pulseaudio pulseaudio-module-zeroconf \
pavucontrol pulseaudio-module-jack

### Настройте HRTF
sudo nano /etc/pulse/daemon.conf

### Измените:
default-sample-format = float32le
default-sample-rate = 48000
alternate-sample-rate = 44100
default-sample-channels = 2
default-channel-map = front-left,front-right
resample-method = speex-float-10
enable-remixing = yes
enable-lfe-remixing = no
default-fragments = 4
default-fragment-size-msec = 5

### Перезапустите PulseAudio
pulseaudio -k
pulseaudio --start

# 7.2 Установка OpenAL Soft

sudo apt install -y libopenal-dev openal-soft

### Настройка HRTF для OpenAL
sudo nano /etc/openal/alsoft.conf

### Добавьте:
hrtf = true
hrtf-paths = /usr/share/openal/hrtf

### Тест 3D звука
sudo apt install -y openal-examples
alffplay ~/Music/test.wav
# 8. Инструменты разработки {#инструменты}
## 8.1 Установка Vulkan

### Установите Vulkan для ARM64
sudo apt install -y vulkan-tools libvulkan-dev mesa-vulkan-drivers

### Проверьте установку
vulkaninfo | grep -A5 "GPU"

### Тест Vulkan
sudo apt install -y vkmark
vkmark --benchmark cube
8.2 Профилирование и отладка

### Установите инструменты профилирования
sudo apt install -y perf linux-tools-generic renderdoc gdb

### Установите инструменты OpenGL
sudo apt install -y apitrace glslviewer

### Мониторинг системы
sudo apt install -y btop glances nmon

### Создайте скрипт для быстрой проверки
sudo nano /usr/local/bin/vr-status.sh

# !/bin/bash
- echo "=== VR System Status ==="
- echo "CPU Temp: $(sensors | grep 'Package id' | awk '{print $4}')"
- echo "GPU Freq: $(cat /sys/devices/platform/ffe40000.gpu/devfreq/ffe40000.gpu/cur_freq)"
- echo "RAM Usage: $(free -h | grep Mem | awk '{print $3"/"$2}')"
- echo "VRAM Usage: $(cat /sys/kernel/debug/mali0/usage)"
- 8.3 Настройка IDE

### Установите VS Code через Snap
sudo snap install code --classic

### Или установите VSCodium
wget -qO - https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo/raw/master/pub.gpg | gpg --dearmor | sudo dd of=/usr/share/keyrings/vscodium-archive-keyring.gpg
echo 'deb [ signed-by=/usr/share/keyrings/vscodium-archive-keyring.gpg ] https://download.vscodium.com/debs vscodium main' | sudo tee /etc/apt/sources.list.d/vscodium.list
sudo apt update
sudo apt install -y codium

### Установите расширения для VR разработки
code --install-extension ms-python.python
code --install-extension monada.monado-debug
code --install-extension godotengine.godot-tools
# 9. Резервное копирование {#резервное-копирование}
## 9.1 Создание образа системы

### Установите утилиты
sudo apt install -y pv

### Создайте полный бэкап
sudo dd if=/dev/mmcblk0 | gzip -c | pv > /backup/orangepi5-vr-full.img.gz

### Создайте скрипт для инкрементального бэкапа
sudo nano /usr/local/bin/backup-vr-system.sh

#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup"
SYSTEM_DEV="/dev/mmcblk0"

echo "Начинаем резервное копирование системы..."
sudo dd if=$SYSTEM_DEV bs=1M status=progress | gzip -c > $BACKUP_DIR/vr-system-$DATE.img.gz
echo "Бэкап создан: $BACKUP_DIR/vr-system-$DATE.img.gz"

### Сделайте исполняемым
sudo chmod +x /usr/local/bin/backup-vr-system.sh
## 9.2 Настройка автоматического бэкапа

### Создайте задание cron
crontab -e

### Добавьте:
0 2 * * * /usr/local/bin/backup-vr-system.sh >> /var/log/vr-backup.log

### Создайте службу для мониторинга бэкапов
sudo nano /etc/systemd/system/vr-backup.service

[Unit]
Description=VR System Backup Service
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup-vr-system.sh
User=root

[Install]
WantedBy=multi-user.target
# 10. Дополнительные инструменты {#дополнительные-инструменты}
## 10.1 3D моделирование и CAD

### Установите Blender для ARM64
wget https://builder.blender.org/download/daily/blender-4.2.0-linux-aarch64.tar.xz
tar -xf blender-4.2.0-linux-aarch64.tar.xz
sudo mv blender-4.2.0-linux-aarch64 /opt/blender
sudo ln -s /opt/blender/blender /usr/local/bin/blender

### Установите FreeCAD
sudo apt install -y freecad

### Установите OpenSCAD
sudo apt install -y openscad

### Создайте папку для моделей
mkdir -p ~/VR-Models/{headset,controllers,accessories}
## 10.2 Калибровка оборудования

### Установите инструменты для калибровки IMU
sudo apt install -y i2c-tools libi2c-dev

### Калибровка MPU-6050/9250
git clone https://github.com/jrowberg/i2cdevlib.git
cd i2cdevlib/Arduino/MPU6050/
make
sudo ./MPU6050_calibration

### Калибровка камер (если есть)
sudo apt install -y guvcview uvcdynctrl
uvcdynctrl -f
# 11. Проверка системы {#проверка}
## 11.1 Полный тест системы

### Создайте файл полной проверки
sudo nano /usr/local/bin/vr-system-test.sh

#!/bin/bash
echo "=== Полная проверка VR системы ==="
echo ""

echo "1. Проверка CPU..."
lscpu | grep -E "(Model name|CPU\(s\)|MHz)"
echo ""

echo "2. Проверка RAM..."
free -h
echo ""

echo "3. Проверка GPU..."
glxinfo | grep -E "(OpenGL|renderer|version)" | head -5
echo ""

echo "4. Проверка дисплеев..."
xrandr --query | grep -E "(connected|1920x1080)"
echo ""

echo "5. Тест OpenGL (30 сек)..."
timeout 30 glmark2-es2 --fullscreen 2>&1 | tail -3
echo ""

echo "6. Проверка температуры..."
sensors | grep -E "(temp|Package)"
echo ""

echo "7. Проверка дисков..."
df -h | grep -E "(Filesystem|/dev/root)"
echo ""

echo "8. Проверка сети..."
ip addr show | grep -E "(inet|state)" | head -5
echo ""

echo "9. Проверка VR сервисов..."
systemctl is-active monado 2>/dev/null && echo "Monado: активен" || echo "Monado: не активен"
echo ""

echo "10. Тест производительности..."
time glxgears > /dev/null 2>&1 &
sleep 5
killall glxgears
echo "Тест завершен"

### Сделайте исполняемым
sudo chmod +x /usr/local/bin/vr-system-test.sh
## 11.2 Тестовые приложения
bash
### Создайте тестовую VR демо
mkdir ~/vr-demos
cd ~/vr-demos

### Скачайте примеры
git clone https://github.com/OpenHMD/OpenHMD.git
cd OpenHMD/examples
make
./opengl-example

### Запустите тест стерео
cd ~/software/demos
./test-stereo-opengl
