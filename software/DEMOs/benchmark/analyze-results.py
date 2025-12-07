#!/usr/bin/env python3
"""
Анализатор результатов бенчмарка VR
Визуализирует результаты тестов
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

class BenchmarkAnalyzer:
    def __init__(self, results_file="benchmark_results/results.json"):
        self.results_file = results_file
        self.data = None
        self.output_dir = "benchmark_results/plots"
        
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_results(self):
        """Загрузка результатов из JSON"""
        try:
            with open(self.results_file, 'r') as f:
                self.data = json.load(f)
            print(f"✓ Загружены результаты от {self.data['benchmark']['date']}")
            return True
        except Exception as e:
            print(f"✗ Ошибка загрузки результатов: {e}")
            return False
    
    def plot_cpu_performance(self):
        """Визуализация производительности CPU"""
        if not self.data or '2d' not in self.data['benchmark']['results']:
            return
        
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))
        
        # Данные CPU
        cpu_data = []
        cpu_labels = []
        
        for test in self.data['benchmark']['results']['2d']:
            if 'cpu' in test['test']:
                cpu_data.append(test['score'])
                label = test['test'].replace('_', ' ').title()
                cpu_labels.append(label)
        
        # График 1: Столбчатая диаграмма
        bars = ax[0].bar(range(len(cpu_data)), cpu_data)
        ax[0].set_title('Производительность CPU')
        ax[0].set_ylabel('Событий/сек')
        ax[0].set_xticks(range(len(cpu_data)))
        ax[0].set_xticklabels(cpu_labels, rotation=45, ha='right')
        
        # Добавление значений на столбцы
        for bar, value in zip(bars, cpu_data):
            ax[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                      f'{value:.0f}', ha='center', va='bottom')
        
        # График 2: Сравнение одноядерной и многоядерной
        if len(cpu_data) >= 2:
            single_core = cpu_data[0] if 'single' in cpu_labels[0].lower() else cpu_data[1]
            multi_core = cpu_data[1] if 'multi' in cpu_labels[1].lower() else cpu_data[0]
            
            speedup = multi_core / single_core
            efficiency = (speedup / 4) * 100  # Для 4 ядер
            
            labels = ['Одно ядро', '4 ядра']
            values = [single_core, multi_core]
            
            bars2 = ax[1].bar(labels, values, color=['skyblue', 'lightgreen'])
            ax[1].set_title(f'Масштабирование: x{speedup:.1f} (Эффективность: {efficiency:.0f}%)')
            ax[1].set_ylabel('Событий/сек')
            
            for bar, value in zip(bars2, values):
                ax[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                          f'{value:.0f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/cpu_performance.png', dpi=150)
        print(f"✓ График CPU сохранен: {self.output_dir}/cpu_performance.png")
        plt.close()
    
    def plot_gpu_performance(self):
        """Визуализация производительности GPU"""
        if not self.data or '3d' not in self.data['benchmark']['results']:
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Данные GPU
        scenes = []
        fps_values = []
        scores = []
        
        for test in self.data['benchmark']['results']['3d']:
            scenes.append(test['scene'])
            fps_values.append(test['fps'])
            scores.append(test['score'])
        
        x = np.arange(len(scenes))
        width = 0.35
        
        # Два графика: FPS и Score
        bars1 = ax.bar(x - width/2, fps_values, width, label='FPS', color='lightcoral')
        bars2 = ax.bar(x + width/2, scores, width, label='Score', color='lightblue')
        
        ax.set_title('Производительность GPU (OpenGL ES)')
        ax.set_xlabel('Сцена')
        ax.set_ylabel('Значение')
        ax.set_xticks(x)
        ax.set_xticklabels(scenes, rotation=45, ha='right')
        ax.legend()
        
        # Линия целевого FPS для VR
        target_fps = 72
        ax.axhline(y=target_fps, color='red', linestyle='--', alpha=0.5, label=f'Цель VR ({target_fps} FPS)')
        ax.legend()
        
        # Добавление значений
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 2,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/gpu_performance.png', dpi=150)
        print(f"✓ График GPU сохранен: {self.output_dir}/gpu_performance.png")
        plt.close()
    
    def plot_vr_load_test(self):
        """Визуализация результатов нагрузочного теста"""
        if not self.data or 'vr_load' not in self.data['benchmark']['results']:
            return
        
        load_data = self.data['benchmark']['results']['vr_load']
        
        if isinstance(load_data, dict) and 'error' not in load_data:
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            
            # CPU использование
            axes[0, 0].bar(['Среднее', 'Максимум'], 
                          [load_data['cpu_avg_percent'], load_data['cpu_max_percent']],
                          color=['lightgreen', 'orange'])
            axes[0, 0].set_title('Использование CPU')
            axes[0, 0].set_ylabel('%')
            axes[0, 0].set_ylim(0, 100)
            
            # Память
            axes[0, 1].bar(['Среднее', 'Максимум'],
                          [load_data['memory_avg_percent'], load_data['memory_max_percent']],
                          color=['lightblue', 'lightcoral'])
            axes[0, 1].set_title('Использование памяти')
            axes[0, 1].set_ylabel('%')
            axes[0, 1].set_ylim(0, 100)
            
            # Температура
            temp_data = [load_data['final_temp_c'], load_data['max_temp_c']]
            colors = ['lightgreen' if t < 70 else 'orange' if t < 85 else 'red' for t in temp_data]
            
            bars = axes[1, 0].bar(['Финальная', 'Максимум'], temp_data, color=colors)
            axes[1, 0].set_title('Температура CPU')
            axes[1, 0].set_ylabel('°C')
            
            # Добавляем пороговые линии
            axes[1, 0].axhline(y=70, color='green', linestyle='--', alpha=0.5, label='Норма')
            axes[1, 0].axhline(y=85, color='red', linestyle='--', alpha=0.5, label='Предел')
            axes[1, 0].legend()
            
            # Общая оценка
            stability = "✓ Стабильно" if load_data.get('stable', True) else "⚠️ Перегрев"
            axes[1, 1].text(0.1, 0.5, 
                           f'Длительность: {load_data["duration_seconds"]}с\n'
                           f'CPU: {load_data["cpu_avg_percent"]}% (ср.)\n'
                           f'Память: {load_data["memory_avg_percent"]}% (ср.)\n'
                           f'Температура: {load_data["max_temp_c"]}°C\n'
                           f'\n{stability}',
                           fontsize=12, 
                           verticalalignment='center',
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            axes[1, 1].set_title('Общая оценка')
            axes[1, 1].axis('off')
            
            plt.suptitle('VR Нагрузочный тест', fontsize=16)
            plt.tight_layout()
            plt.savefig(f'{self.output_dir}/vr_load_test.png', dpi=150)
            print(f"✓ График нагрузочного теста сохранен: {self.output_dir}/vr_load_test.png")
            plt.close()
    
    def generate_html_report(self):
        """Генерация HTML отчета"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>VR Benchmark Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                         color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
                .card {{ background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                       padding: 20px; margin-bottom: 20px; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                       gap: 20px; }}
                img {{ max-width: 100%; height: auto; border-radius: 5px; }}
                .good {{ color: #4CAF50; font-weight: bold; }}
                .warning {{ color: #FF9800; font-weight: bold; }}
                .bad {{ color: #F44336; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎮 Отчет о производительности VR</h1>
                    <p>Orange Pi 5 | {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
                </div>
                
                <div class="card">
                    <h2>📊 Сводка результатов</h2>
                    <div class="grid">
        """
        
        # Добавляем графики
        plots = ['cpu_performance.png', 'gpu_performance.png', 'vr_load_test.png']
        
        for plot in plots:
            if os.path.exists(f'{self.output_dir}/{plot}'):
                html_content += f"""
                        <div>
                            <h3>{plot.replace('_', ' ').replace('.png', '').title()}</h3>
                            <img src="{plot}" alt="{plot}">
                        </div>
                """
        
        html_content += """
                    </div>
                </div>
                
                <div class="card">
                    <h2>📈 Рекомендации</h2>
        """
        
        # Анализируем результаты
        recommendations = []
        
        # Проверка FPS
        if self.data and '3d' in self.data['benchmark']['results']:
            fps_values = [t['fps'] for t in self.data['benchmark']['results']['3d']]
            avg_fps = np.mean(fps_values) if fps_values else 0
            
            if avg_fps >= 72:
                recommendations.append(("FPS", f"<span class='good'>{avg_fps:.1f} FPS - отлично для VR</span>"))
            elif avg_fps >= 60:
                recommendations.append(("FPS", f"<span class='warning'>{avg_fps:.1f} FPS - приемлемо, но лучше 72+</span>"))
            else:
                recommendations.append(("FPS", f"<span class='bad'>{avg_fps:.1f} FPS - недостаточно для комфортного VR</span>"))
        
        # Проверка температуры
        if self.data and 'vr_load' in self.data['benchmark']['results']:
            load_data = self.data['benchmark']['results']['vr_load']
            if isinstance(load_data, dict) and 'max_temp_c' in load_data:
                temp = load_data['max_temp_c']
                if temp < 70:
                    recommendations.append(("Температура", f"<span class='good'>{temp}°C - хорошая термодинамика</span>"))
                elif temp < 85:
                    recommendations.append(("Температура", f"<span class='warning'>{temp}°C - близко к пределу</span>"))
                else:
                    recommendations.append(("Температура", f"<span class='bad'>{temp}°C - требуется охлаждение</span>"))
        
        for title, value in recommendations:
            html_content += f"<p><strong>{title}:</strong> {value}</p>"
        
        html_content += """
                    <h3>Оптимизации:</h3>
                    <ul>
                        <li>Использовать драйвер Panfrost Mali для лучшей производительности OpenGL ES</li>
                        <li>Настроить CPU governor на 'performance' во время VR сессий</li>
                        <li>Добавить активное охлаждение (вентилятор) для Orange Pi 5</li>
                        <li>Использовать легковесный оконный менеджер (Openbox, i3)</li>
                        <li>Оптимизировать настройки разрешения для целевого FPS</li>
                    </ul>
                </div>
                
                <div class="card">
                    <h2>📋 Следующие шаги</h2>
                    <ol>
                        <li>Запустить бенчмарк после каждой оптимизации</li>
                        <li>Тестировать с разными разрешениями (1080p, 1440p)</li>
                        <li>Проверить стерео-рендеринг с двумя дисплеями</li>
                        <li>Измерить реальную задержку end-to-end</li>
                        <li>Сравнить с другими платформами (Raspberry Pi 4/5)</li>
                    </ol>
                </div>
                
                <div class="card">
                    <p><em>Отчет сгенерирован автоматически. Для подробностей смотрите JSON файлы в benchmark_results/</em></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(f'{self.output_dir}/report.html', 'w') as f:
            f.write(html_content)
        
        print(f"✓ HTML отчет сохранен: {self.output_dir}/report.html")
        print(f"   Откройте в браузере: firefox {self.output_dir}/report.html")
    
    def run(self):
        """Запуск анализа"""
        if not self.load_results():
            return
        
        print("🔄 Анализ результатов...")
        
        self.plot_cpu_performance()
        self.plot_gpu_performance()
        self.plot_vr_load_test()
        self.generate_html_report()
        
        print("\n✅ Анализ завершен!")
        print(f"📁 Результаты в: {self.output_dir}/")

if __name__ == "__main__":
    analyzer = BenchmarkAnalyzer()
    analyzer.run()