# software/drivers/mpu6050/mpu6050_python.py
"""
ПРОСТОЙ Python драйвер MPU-6050
Работает через userspace I2C - безопасно и просто!
"""

import smbus2
import time
import math
from dataclasses import dataclass
from typing import Tuple

@dataclass
class MPU6050Data:
    """Структура данных MPU-6050"""
    accel_x: float  # g
    accel_y: float  # g
    accel_z: float  # g
    gyro_x: float   # °/s
    gyro_y: float   # °/s
    gyro_z: float   # °/s
    temperature: float  # °C
    pitch: float    # градусы
    roll: float     # градусы

class MPU6050Driver:
    """Userspace драйвер MPU-6050 на Python"""
    
    def __init__(self, bus_num=1, address=0x68):
        """
        Инициализация драйвера
        
        Args:
            bus_num: Номер I2C шины (обычно 1 для Orange Pi 5)
            address: Адрес устройства (0x68 или 0x69)
        """
        self.bus = smbus2.SMBus(bus_num)
        self.address = address
        self.calibration = {'accel': [0, 0, 0], 'gyro': [0, 0, 0]}
        
        # Инициализация MPU-6050
        self._initialize()
        print(f"✅ MPU-6050 драйвер инициализирован (адрес 0x{address:x})")
    
    def _initialize(self):
        """Настройка MPU-6050"""
        # Разбудить устройство
        self.bus.write_byte_data(self.address, 0x6B, 0x00)
        
        # Настройка гироскопа (±250 °/s)
        self.bus.write_byte_data(self.address, 0x1B, 0x00)
        
        # Настройка акселерометра (±2g)
        self.bus.write_byte_data(self.address, 0x1C, 0x00)
        
        time.sleep(0.1)
    
    def read_raw(self) -> Tuple[int, ...]:
        """Чтение сырых данных"""
        # Чтение 14 регистров (0x3B - 0x48)
        data = self.bus.read_i2c_block_data(self.address, 0x3B, 14)
        
        # Парсинг данных
        accel_x = (data[0] << 8) | data[1]
        accel_y = (data[2] << 8) | data[3]
        accel_z = (data[4] << 8) | data[5]
        temp = (data[6] << 8) | data[7]
        gyro_x = (data[8] << 8) | data[9]
        gyro_y = (data[10] << 8) | data[11]
        gyro_z = (data[12] << 8) | data[13]
        
        return accel_x, accel_y, accel_z, temp, gyro_x, gyro_y, gyro_z
    
    def calibrate(self, samples=100):
        """Калибровка датчика"""
        print("Калибровка MPU-6050... Лежите ровно!")
        
        accel_sum = [0, 0, 0]
        gyro_sum = [0, 0, 0]
        
        for i in range(samples):
            ax, ay, az, _, gx, gy, gz = self.read_raw()
            
            accel_sum[0] += ax
            accel_sum[1] += ay
            accel_sum[2] += az
            gyro_sum[0] += gx
            gyro_sum[1] += gy
            gyro_sum[2] += gz
            
            time.sleep(0.01)
            if i % 10 == 0:
                print(f"  Прогресс: {i+1}/{samples}")
        
        # Расчет смещений
        self.calibration['accel'][0] = accel_sum[0] / samples
        self.calibration['accel'][1] = accel_sum[1] / samples
        self.calibration['accel'][2] = (accel_sum[2] / samples) - 16384  # 1g
        
        self.calibration['gyro'] = [x / samples for x in gyro_sum]
        
        print("✅ Калибровка завершена!")
    
    def read(self) -> MPU6050Data:
        """Чтение и обработка данных"""
        # Сырые данные
        ax, ay, az, temp, gx, gy, gz = self.read_raw()
        
        # Применение калибровки
        ax -= self.calibration['accel'][0]
        ay -= self.calibration['accel'][1]
        az -= self.calibration['accel'][2]
        gx -= self.calibration['gyro'][0]
        gy -= self.calibration['gyro'][1]
        gz -= self.calibration['gyro'][2]
        
        # Конвертация в физические величины
        accel_x = ax / 16384.0  # ±2g режим
        accel_y = ay / 16384.0
        accel_z = az / 16384.0
        
        gyro_x = gx / 131.0     # ±250 °/s режим
        gyro_y = gy / 131.0
        gyro_z = gz / 131.0
        
        temperature = temp / 340.0 + 36.53
        
        # Расчет углов наклона
        pitch = math.atan2(accel_y, math.sqrt(accel_x**2 + accel_z**2))
        roll = math.atan2(-accel_x, accel_z)
        
        return MPU6050Data(
            accel_x=accel_x,
            accel_y=accel_y,
            accel_z=accel_z,
            gyro_x=gyro_x,
            gyro_y=gyro_y,
            gyro_z=gyro_z,
            temperature=temperature,
            pitch=math.degrees(pitch),
            roll=math.degrees(roll)
        )
    
    def test(self):
        """Тест драйвера"""
        print("Тест MPU-6050 драйвера...")
        print("Двигайте датчик и наблюдайте за значениями")
        print("Ctrl+C для остановки")
        
        try:
            while True:
                data = self.read()
                print(f"\rPitch: {data.pitch:6.1f}° | "
                      f"Roll: {data.roll:6.1f}° | "
                      f"Temp: {data.temperature:5.1f}°C", end="")
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n\n✅ Тест завершен!")

# Простейшее использование
if __name__ == "__main__":
    # Создаем драйвер
    mpu = MPU6050Driver()
    
    # Калибруем (положить на ровную поверхность)
    mpu.calibrate(samples=50)
    
    # Запускаем тест
    mpu.test()