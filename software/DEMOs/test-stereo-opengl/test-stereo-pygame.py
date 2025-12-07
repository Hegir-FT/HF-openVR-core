#!/usr/bin/env python3
"""
Test Stereo для VR шлема на Orange Pi 5
Требуется: pip3 install pygame numpy
"""

import pygame
import sys
import numpy as np
import math
from pygame.locals import *

# Настройки
WIDTH, HEIGHT = 1920, 1080
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LEFT_EYE_COLOR = (255, 100, 100)    # Красный
RIGHT_EYE_COLOR = (100, 100, 255)   # Синий
LEFT_BG = (30, 30, 30)              # Темный фон для левого глаза
RIGHT_BG = (30, 30, 30)             # Темный фон для правого глаза

class StereoTest:
    def __init__(self):
        pygame.init()
        
        # Создаем два окна
        self.left_screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
        self.right_screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME, 
                                                    pygame.display.get_surface().get_rect().move(WIDTH, 0))
        
        # Устанавливаем позиции окон
        pygame.display.set_caption("VR Stereo Test - Левый глаз")
        pygame.display.set_caption("VR Stereo Test - Правый глаз")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.time = 0
        
        # Координаты треугольника
        self.triangle_points = np.array([
            [0, -150],   # Верхняя вершина
            [-130, 150], # Левая нижняя
            [130, 150]   # Правая нижняя
        ])
        
        # Центр экрана
        self.center_x = WIDTH // 2
        self.center_y = HEIGHT // 2
        
        print("=" * 50)
        print("VR Stereo Test запущен")
        print("Левый глаз: Красный треугольник")
        print("Правый глаз: Синий треугольник")
        print("Нажмите ESC для выхода")
        print("=" * 50)
    
    def rotate_point(self, point, angle):
        """Вращение точки вокруг центра"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        x = point[0] * cos_a - point[1] * sin_a
        y = point[0] * sin_a + point[1] * cos_a
        return np.array([x, y])
    
    def draw_triangle(self, surface, color, eye_offset=0):
        """Рисует треугольник с параллаксом"""
        # Параллакс для стереоэффекта
        parallax = 50 * math.sin(self.time * 0.5)
        
        # Разный параллакс для левого и правого глаза
        if eye_offset == 0:  # Левый глаз
            offset_x = -parallax
        else:  # Правый глаз
            offset_x = parallax
        
        # Вращаем треугольник
        angle = self.time
        rotated_points = [self.rotate_point(p, angle) for p in self.triangle_points]
        
        # Собираем точки для отрисовки
        draw_points = []
        for point in rotated_points:
            x = int(self.center_x + point[0] + offset_x)
            y = int(self.center_y + point[1])
            draw_points.append((x, y))
        
        # Рисуем треугольник
        pygame.draw.polygon(surface, color, draw_points)
        
        # Рисуем контур
        pygame.draw.polygon(surface, WHITE, draw_points, 3)
        
        # Рисуем информацию
        font = pygame.font.Font(None, 36)
        if eye_offset == 0:
            eye_text = "ЛЕВЫЙ ГЛАЗ"
            fps_text = f"FPS: {int(self.clock.get_fps())}"
            color_text = "Цвет: Красный"
        else:
            eye_text = "ПРАВЫЙ ГЛАЗ"
            fps_text = f"FPS: {int(self.clock.get_fps())}"
            color_text = "Цвет: Синий"
        
        # Вывод текста
        texts = [
            font.render(eye_text, True, WHITE),
            font.render(fps_text, True, WHITE),
            font.render(color_text, True, WHITE),
            font.render("ESC - выход", True, WHITE)
        ]
        
        for i, text in enumerate(texts):
            surface.blit(text, (50, 50 + i * 40))
    
    def run(self):
        """Основной игровой цикл"""
        while self.running:
            self.time += 0.016  # Время для анимации
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
            
            # Рисуем левый глаз
            self.left_screen.fill(LEFT_BG)
            self.draw_triangle(self.left_screen, LEFT_EYE_COLOR, 0)
            
            # Рисуем правый глаз
            self.right_screen.fill(RIGHT_BG)
            self.draw_triangle(self.right_screen, RIGHT_EYE_COLOR, 1)
            
            # Обновляем экраны
            pygame.display.flip()
            pygame.display.update()
            
            # Ограничение FPS
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = StereoTest()
    app.run()