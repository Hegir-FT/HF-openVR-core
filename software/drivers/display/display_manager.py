# software/drivers/display/display_manager.py
"""
Управление дисплеями через Python
Использует xrandr - безопасно и просто!
"""

import subprocess
import json
import time

class DisplayManager:
    """Userspace менеджер дисплеев"""
    
    def __init__(self):
        self.displays = self._detect_displays()
    
    def _detect_displays(self):
        """Обнаружение подключенных дисплеев"""
        result = subprocess.run(
            ['xrandr', '--query'],
            capture_output=True,
            text=True
        )
        
        displays = []
        current_display = None
        
        for line in result.stdout.split('\n'):
            if ' connected' in line:
                parts = line.split()
                name = parts[0]
                connected = 'connected' in line
                primary = 'primary' in line
                
                current_display = {
                    'name': name,
                    'connected': connected,
                    'primary': primary,
                    'modes': []
                }
                displays.append(current_display)
            
            elif 'x' in line and current_display:
                if '*' in line or '+' in line:
                    mode = line.strip().split()[0]
                    current_display['modes'].append(mode)
        
        print(f"✅ Обнаружено дисплеев: {len(displays)}")
        return displays
    
    def setup_vr_mode(self):
        """Настройка режима для VR (2 дисплея)"""
        if len(self.displays) < 2:
            print("❌ Недостаточно дисплеев для VR режима")
            return False
        
        # Получаем первые два дисплея
        display1 = self.displays[0]['name']
        display2 = self.displays[1]['name']
        
        print(f"Настройка VR режима: {display1} + {display2}")
        
        # Устанавливаем разрешение 1920x1080
        commands = [
            ['xrandr', '--output', display1, '--mode', '1920x1080', '--pos', '0x0', '--primary'],
            ['xrandr', '--output', display2, '--mode', '1920x1080', '--pos', '1920x0'],
            ['xrandr', '--fb', '3840x1080']  # Виртуальный фреймбуфер
        ]
        
        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Ошибка: {result.stderr}")
                return False
        
        print("✅ VR режим настроен!")
        return True
    
    def mirror_mode(self):
        """Режим зеркала (если extend не работает)"""
        if len(self.displays) < 2:
            return False
        
        display1 = self.displays[0]['name']
        display2 = self.displays[1]['name']
        
        commands = [
            ['xrandr', '--output', display1, '--mode', '1920x1080'],
            ['xrandr', '--output', display2, '--same-as', display1]
        ]
        
        for cmd in commands:
            subprocess.run(cmd)
        
        print("⚠️  Установлен режим зеркала. Используйте шейдеры для стерео.")
        return True

# Использование
if __name__ == "__main__":
    dm = DisplayManager()
    
    # Пытаемся настроить VR режим
    if not dm.setup_vr_mode():
        print("Пробуем режим зеркала...")
        dm.mirror_mode()