# software/drivers/hfopenvr_manager.py
"""
Главный менеджер драйверов HF-openVR-core
Все драйверы в userspace на Python!
"""

import time
import threading
from dataclasses import dataclass
from typing import Optional

# Импортируем наши драйверы
from mpu6050.mpu6050_python import MPU6050Driver, MPU6050Data
from display.display_manager import DisplayManager

@dataclass
class VRState:
    """Состояние VR системы"""
    head_pose: MPU6050Data
    displays_ready: bool
    fps: float
    latency: float

class HFOpenVRManager:
    """Главный менеджер всех драйверов"""
    
    def __init__(self):
        print("=" * 50)
        print("HF-openVR-core Driver Manager")
        print("Все драйверы в userspace на Python")
        print("=" * 50)
        
        # Инициализация драйверов
        self.mpu_driver: Optional[MPU6050Driver] = None
        self.display_manager: Optional[DisplayManager] = None
        
        # Состояние системы
        self.state = VRState(
            head_pose=None,
            displays_ready=False,
            fps=0,
            latency=0
        )
        
        # Потоки
        self.running = False
        self.sensor_thread = None
    
    def initialize(self):
        """Инициализация всех драйверов"""
        print("\n1. Инициализация MPU-6050...")
        try:
            self.mpu_driver = MPU6050Driver()
            self.mpu_driver.calibrate(samples=50)
            print("✅ MPU-6050 готов")
        except Exception as e:
            print(f"❌ Ошибка MPU-6050: {e}")
            self.mpu_driver = None
        
        print("\n2. Настройка дисплеев...")
        try:
            self.display_manager = DisplayManager()
            if self.display_manager.setup_vr_mode():
                self.state.displays_ready = True
                print("✅ Дисплеи готовы")
            else:
                print("⚠️  Дисплеи в режиме зеркала")
        except Exception as e:
            print(f"❌ Ошибка дисплеев: {e}")
        
        print("\n3. Запуск потоков...")
        self.running = True
        self.sensor_thread = threading.Thread(target=self._sensor_loop)
        self.sensor_thread.start()
        
        print("\n" + "=" * 50)
        print("✅ Система инициализирована!")
        print("Используйте start_vr_app() для запуска VR")
        print("=" * 50)
    
    def _sensor_loop(self):
        """Поток чтения сенсоров"""
        last_time = time.time()
        frame_count = 0
        
        while self.running:
            if self.mpu_driver:
                try:
                    # Чтение данных
                    self.state.head_pose = self.mpu_driver.read()
                    
                    # Расчет FPS
                    frame_count += 1
                    current_time = time.time()
                    if current_time - last_time >= 1.0:
                        self.state.fps = frame_count
                        frame_count = 0
                        last_time = current_time
                    
                except Exception as e:
                    print(f"Ошибка чтения сенсора: {e}")
            
            time.sleep(0.01)  # 100Hz
    
    def start_vr_app(self, app_name="test-stereo"):
        """Запуск VR приложения"""
        print(f"\nЗапуск {app_name}...")
        
        if not self.state.displays_ready:
            print("⚠️  Дисплеи не настроены. Запуск может не работать.")
        
        # Здесь будет запуск конкретного приложения
        # Пока просто демонстрация
        print("VR приложение запущено!")
        print("Используйте Ctrl+C для остановки")
        
        try:
            while True:
                if self.state.head_pose:
                    print(f"\rHead: Pitch={self.state.head_pose.pitch:5.1f}° "
                          f"Roll={self.state.head_pose.roll:5.1f}° "
                          f"FPS={self.state.fps:.0f}", end="")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n\nОстановка...")
    
    def shutdown(self):
        """Корректное завершение"""
        print("\nЗавершение работы...")
        self.running = False
        
        if self.sensor_thread:
            self.sensor_thread.join(timeout=2)
        
        print("✅ Система остановлена")

# Простейший запуск
if __name__ == "__main__":
    # Создаем менеджер
    manager = HFOpenVRManager()
    
    # Инициализируем
    manager.initialize()
    
    # Запускаем тестовое приложение
    try:
        manager.start_vr_app()
    finally:
        manager.shutdown()