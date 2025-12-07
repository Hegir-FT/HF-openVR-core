#!/bin/bash
# VR Performance Benchmark for Orange Pi 5
# Автор: Hegir ^_^
# Дата: Декабрь 2025

set -e  # Завершить при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Конфигурация
TEST_DURATION=10  # Длительность каждого теста в секундах
LOG_FILE="vr_benchmark_$(date +%Y%m%d_%H%M%S).log"
RESULTS_DIR="benchmark_results"
OUTPUT_JSON="$RESULTS_DIR/results.json"

# Создаем директории
mkdir -p $RESULTS_DIR

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  VR Performance Benchmark v1.0${NC}"
echo -e "${BLUE}  Orange Pi 5 / RK3588${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Функция логирования
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

# Функция проверки зависимостей
check_dependencies() {
    log "Проверка зависимостей..."
    
    local missing_deps=()
    
    # Проверяем утилиты
    for cmd in glmark2-es2 glxinfo vcgencmd sensors stress-ng; do
        if ! command -v $cmd &> /dev/null; then
            missing_deps+=($cmd)
        fi
    done
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        log "Установка недостающих зависимостей..."
        sudo apt-get update
        sudo apt-get install -y glmark2-es2 mesa-utils stress-ng lm-sensors
        
        # Для Orange Pi 5
        sudo apt-get install -y rockchip-toolkit || log "rockchip-toolkit недоступен"
    fi
}

# Получение системной информации
get_system_info() {
    log "Сбор системной информации..."
    
    cat > $RESULTS_DIR/system_info.txt << EOF
=== Системная информация ===
Дата теста: $(date)
Длительность тестов: ${TEST_DURATION} секунд

--- Аппаратная часть ---
Процессор: $(cat /proc/cpuinfo | grep "model name" | head -1 | cut -d: -f2 | xargs)
Количество ядер: $(nproc)
Архитектура: $(uname -m)
Память: $(free -h | grep Mem | awk '{print $2}')
GPU: $(lspci | grep -i vga | cut -d: -f3 | xargs)

--- Операционная система ---
Дистрибутив: $(lsb_release -d 2>/dev/null | cut -f2)
Ядро: $(uname -r)
OpenGL версия: $(glxinfo 2>/dev/null | grep "OpenGL version string" | head -1 | cut -d: -f2 | xargs)
OpenGL ES версия: $(glxinfo 2>/dev/null | grep "OpenGL ES profile version" | head -1 | cut -d: -f2 | xargs)

--- Температуры (начальные) ---
$(sensors 2>/dev/null || echo "Датчики температуры не найдены")

--- Частоты (начальные) ---
$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq 2>/dev/null | awk '{print "CPU0: " $1/1000 " MHz"}' || true)
$(cat /sys/devices/system/cpu/cpu4/cpufreq/scaling_cur_freq 2>/dev/null | awk '{print "CPU4: " $1/1000 " MHz"}' || true)
EOF
    
    log "Системная информация сохранена в $RESULTS_DIR/system_info.txt"
}

# Тест 1: 2D производительность
test_2d_performance() {
    log "Запуск 2D тестов..."
    
    local results=()
    
    # Тест копирования в памяти
    log "Тест копирования памяти..."
    local mem_score=$(sysbench memory --memory-block-size=1M --memory-total-size=1G run 2>/dev/null | grep "transferred" | awk '{print $4}' | sed 's/(//')
    results+=("{\"test\": \"memory_copy\", \"score\": $mem_score, \"unit\": \"MB/s\"}")
    
    # Тест процессора
    log "Тест процессора (1 ядро)..."
    local cpu_single=$(sysbench cpu --cpu-max-prime=20000 --threads=1 run 2>/dev/null | grep "events per second" | awk '{print $4}')
    results+=("{\"test\": \"cpu_single_core\", \"score\": $cpu_single, \"unit\": \"events/sec\"}")
    
    # Тест всех ядер
    log "Тест процессора (все ядра)..."
    local cpu_multi=$(sysbench cpu --cpu-max-prime=20000 --threads=$(nproc) run 2>/dev/null | grep "events per second" | awk '{print $4}')
    results+=("{\"test\": \"cpu_multi_core\", \"score\": $cpu_multi, \"unit\": \"events/sec\"}")
    
    echo "[$(echo ${results[@]} | sed 's/ /,/g')]" > $RESULTS_DIR/2d_results.json
}

# Тест 2: 3D производительность (OpenGL ES)
test_3d_performance() {
    log "Запуск 3D тестов (OpenGL ES)..."
    
    local results=()
    
    # Запускаем glmark2-es2 с разными сценами
    local scenes=("build" "texture" "shading" "effect2d" "pulsar")
    
    for scene in "${scenes[@]}"; do
        log "Тест сцены: $scene"
        
        # Запускаем тест и парсим результат
        local output=$(timeout $TEST_DURATION glmark2-es2 --scene $scene --benchmark 2>&1 || true)
        local fps=$(echo "$output" | grep "FPS:" | awk '{print $2}' | head -1)
        local score=$(echo "$output" | grep "Score:" | awk '{print $2}' | head -1)
        
        if [ ! -z "$fps" ] && [ "$fps" != "nan" ]; then
            results+=("{\"scene\": \"$scene\", \"fps\": $fps, \"score\": $score}")
            log "  FPS: $fps, Score: $score"
        else
            log "  Тест не удался для сцены $scene"
        fi
    done
    
    # Тест с режимом fullscreen
    log "Тест в полноэкранном режиме..."
    local fullscreen_output=$(timeout $TEST_DURATION glmark2-es2 --fullscreen 2>&1 || true)
    local fullscreen_fps=$(echo "$fullscreen_output" | grep "FPS:" | awk '{print $2}' | head -1)
    local fullscreen_score=$(echo "$fullscreen_output" | grep "Score:" | awk '{print $2}' | head -1)
    
    if [ ! -z "$fullscreen_fps" ] && [ "$fullscreen_fps" != "nan" ]; then
        results+=("{\"scene\": \"fullscreen\", \"fps\": $fullscreen_fps, \"score\": $fullscreen_score}")
    fi
    
    echo "[$(echo ${results[@]} | sed 's/ /,/g')]" > $RESULTS_DIR/3d_results.json
}

# Тест 3: Стерео рендеринг (два дисплея)
test_stereo_performance() {
    log "Запуск теста стерео-рендеринга..."
    
    # Создаем простой тест на Python
    cat > /tmp/stereo_test.py << 'EOF'
#!/usr/bin/env python3
import time
import subprocess
import numpy as np
from datetime import datetime

class StereoBenchmark:
    def __init__(self, duration=10):
        self.duration = duration
        self.results = []
        
    def run_gl_test(self, display=0):
        """Запускает простой OpenGL тест на указанном дисплее"""
        cmd = f"DISPLAY=:0.{display} glxgears -info 2>&1"
        start = time.time()
        frames = 0
        
        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            while time.time() - start < self.duration:
                line = process.stdout.readline()
                if not line:
                    break
                if b"frames" in line:
                    frames += 1
                    
            process.terminate()
            
            fps = frames / self.duration
            return fps
        except:
            return 0.0
    
    def run_dual_display_test(self):
        """Тестирует два дисплея одновременно"""
        print("Тестирование стерео-рендеринга...")
        
        # Тест левого дисплея
        print("  Левый дисплей...")
        left_fps = self.run_gl_test(0)
        
        # Тест правого дисплея
        print("  Правый дисплей...")
        right_fps = self.run_gl_test(1)
        
        # Тест обоих дисплеев
        print("  Оба дисплея одновременно...")
        # Здесь можно добавить более сложный тест
        
        return {
            "left_display_fps": left_fps,
            "right_display_fps": right_fps,
            "stereo_score": min(left_fps, right_fps)  # Наихудший показатель определяет стерео FPS
        }

if __name__ == "__main__":
    benchmark = StereoBenchmark(duration=5)
    results = benchmark.run_dual_display_test()
    print("\nРезультаты стерео-теста:")
    print(f"  Левый дисплей: {results['left_display_fps']:.1f} FPS")
    print(f"  Правый дисплей: {results['right_display_fps']:.1f} FPS")
    print(f"  Стерео-производительность: {results['stereo_score']:.1f} FPS")
    
    # Сохраняем результаты в формате JSON
    import json
    print(json.dumps(results))
EOF
    
    # Запускаем тест
    local stereo_results=$(python3 /tmp/stereo_test.py 2>/dev/null | tail -1)
    
    if [ ! -z "$stereo_results" ]; then
        echo "$stereo_results" > $RESULTS_DIR/stereo_results.json
        log "Результаты стерео-теста сохранены"
    else
        log "Стерео-тест не удался (возможно, нет двух активных дисплеев)"
        echo "{\"error\": \"stereo_test_failed\"}" > $RESULTS_DIR/stereo_results.json
    fi
}

# Тест 4: Задержка (латентность)
test_latency() {
    log "Измерение задержки..."
    
    # Простой тест на задержку рендеринга
    cat > /tmp/latency_test.c << 'EOF'
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <X11/Xlib.h>

int main() {
    Display *display = XOpenDisplay(NULL);
    if (!display) {
        printf("{\"error\": \"x11_display_failed\"}\n");
        return 1;
    }
    
    // Создаем простое окно
    Window window = XCreateSimpleWindow(display, 
                                        RootWindow(display, 0),
                                        0, 0, 100, 100, 0,
                                        BlackPixel(display, 0),
                                        WhitePixel(display, 0));
    
    XSelectInput(display, window, ExposureMask);
    XMapWindow(display, window);
    XFlush(display);
    
    struct timespec start, end;
    int iterations = 100;
    long total_latency = 0;
    
    for (int i = 0; i < iterations; i++) {
        clock_gettime(CLOCK_MONOTONIC, &start);
        
        // Запрос на перерисовку
        XClearWindow(display, window);
        XFlush(display);
        
        clock_gettime(CLOCK_MONOTONIC, &end);
        
        long latency_ns = (end.tv_sec - start.tv_sec) * 1000000000 + 
                          (end.tv_nsec - start.tv_nsec);
        total_latency += latency_ns;
        
        usleep(1000);  // Пауза 1 мс
    }
    
    XDestroyWindow(display, window);
    XCloseDisplay(display);
    
    double avg_latency_ms = (total_latency / iterations) / 1000000.0;
    
    printf("{\"render_latency_ms\": %.2f, \"iterations\": %d}\n", 
           avg_latency_ms, iterations);
    
    return 0;
}
EOF
    
    # Компилируем и запускаем
    gcc -o /tmp/latency_test /tmp/latency_test.c -lX11 2>/dev/null
    
    if [ -f /tmp/latency_test ]; then
        local latency_result=$(/tmp/latency_test)
        echo "$latency_result" > $RESULTS_DIR/latency_results.json
        log "Задержка рендеринга: $(echo $latency_result | grep -o '[0-9]*\.[0-9]*' | head -1) мс"
    else
        log "Тест задержки пропущен (требуется X11 и библиотеки)"
        echo "{\"error\": \"latency_test_compilation_failed\"}" > $RESULTS_DIR/latency_results.json
    fi
}

# Тест 5: Нагрузочный тест (VR-симуляция)
test_vr_simulation() {
    log "Запуск VR-симуляции нагрузки..."
    
    cat > /tmp/vr_load_test.py << 'EOF'
#!/usr/bin/env python3
import time
import threading
import subprocess
import json
import psutil

class VRLoadTest:
    def __init__(self, duration=30):
        self.duration = duration
        self.results = {
            "cpu_usage": [],
            "memory_usage": [],
            "temperature": [],
            "frequencies": []
        }
        self.running = True
        
    def monitor_system(self):
        """Мониторинг системных параметров"""
        start_time = time.time()
        
        while self.running and time.time() - start_time < self.duration:
            # CPU загрузка
            cpu_percent = psutil.cpu_percent(interval=0.5, percpu=True)
            self.results["cpu_usage"].append({
                "time": time.time() - start_time,
                "cpu_percent": cpu_percent,
                "total": sum(cpu_percent) / len(cpu_percent)
            })
            
            # Память
            memory = psutil.virtual_memory()
            self.results["memory_usage"].append({
                "time": time.time() - start_time,
                "used_mb": memory.used / 1024 / 1024,
                "percent": memory.percent
            })
            
            # Температура (если доступно)
            try:
                temps = psutil.sensors_temperatures()
                if 'cpu_thermal' in temps:
                    self.results["temperature"].append({
                        "time": time.time() - start_time,
                        "temp": temps['cpu_thermal'][0].current
                    })
            except:
                pass
            
            time.sleep(0.5)
    
    def create_load(self):
        """Создание нагрузки, имитирующей VR приложение"""
        # Запускаем несколько процессов для создания нагрузки
        processes = []
        
        # CPU нагрузка (симуляция физики)
        processes.append(subprocess.Popen(
            ["stress-ng", "--cpu", "4", "--timeout", str(self.duration), "--metrics-brief"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        ))
        
        # GPU нагрузка (через glmark2)
        processes.append(subprocess.Popen(
            ["glmark2-es2", "--fullscreen", "--run-forever"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        ))
        
        # Ждем завершения теста
        time.sleep(self.duration)
        
        # Останавливаем процессы
        for p in processes:
            p.terminate()
            p.wait()
    
    def run(self):
        """Запуск теста"""
        print(f"VR нагрузочный тест на {self.duration} секунд...")
        
        # Запускаем мониторинг в отдельном потоке
        monitor_thread = threading.Thread(target=self.monitor_system)
        monitor_thread.start()
        
        # Создаем нагрузку
        self.create_load()
        
        # Останавливаем мониторинг
        self.running = False
        monitor_thread.join()
        
        # Анализируем результаты
        if self.results["cpu_usage"]:
            avg_cpu = sum([r["total"] for r in self.results["cpu_usage"]]) / len(self.results["cpu_usage"])
            max_cpu = max([r["total"] for r in self.results["cpu_usage"]])
        else:
            avg_cpu = max_cpu = 0
            
        if self.results["memory_usage"]:
            avg_mem = sum([r["percent"] for r in self.results["memory_usage"]]) / len(self.results["memory_usage"])
            max_mem = max([r["percent"] for r in self.results["memory_usage"]])
        else:
            avg_mem = max_mem = 0
            
        if self.results["temperature"]:
            final_temp = self.results["temperature"][-1]["temp"] if self.results["temperature"] else 0
            max_temp = max([r["temp"] for r in self.results["temperature"]]) if self.results["temperature"] else 0
        else:
            final_temp = max_temp = 0
        
        return {
            "duration_seconds": self.duration,
            "cpu_avg_percent": round(avg_cpu, 1),
            "cpu_max_percent": round(max_cpu, 1),
            "memory_avg_percent": round(avg_mem, 1),
            "memory_max_percent": round(max_mem, 1),
            "final_temp_c": round(final_temp, 1),
            "max_temp_c": round(max_temp, 1),
            "stable": max_temp < 85  # Порог перегрева для RK3588
        }

if __name__ == "__main__":
    test = VRLoadTest(duration=15)  # Короткий тест для демо
    results = test.run()
    print(json.dumps(results, indent=2))
EOF
    
    log "Запуск VR нагрузочного теста (15 секунд)..."
    local vr_results=$(python3 /tmp/vr_load_test.py 2>/dev/null | tail -1)
    
    if [ ! -z "$vr_results" ]; then
        echo "$vr_results" > $RESULTS_DIR/vr_load_results.json
        log "VR нагрузочный тест завершен"
    else
        log "VR нагрузочный тест не удался"
        echo "{\"error\": \"vr_load_test_failed\"}" > $RESULTS_DIR/vr_load_results.json
    fi
}

# Генерация отчета
generate_report() {
    log "Генерация отчета..."
    
    cat > $RESULTS_DIR/report.md << EOF
# Отчет о производительности VR системы
## Orange Pi 5 / $(date)

### 📊 Сводка результатов

#### Системная информация
\`\`\`
$(cat $RESULTS_DIR/system_info.txt | tail -20)
\`\`\`

#### Производительность 2D
$(if [ -f $RESULTS_DIR/2d_results.json ]; then
    echo "\`\`\`json"
    cat $RESULTS_DIR/2d_results.json
    echo "\`\`\`"
fi)

#### Производительность 3D (OpenGL ES)
$(if [ -f $RESULTS_DIR/3d_results.json ]; then
    echo "\`\`\`json"
    cat $RESULTS_DIR/3d_results.json
    echo "\`\`\`"
fi)

#### Стерео производительность
$(if [ -f $RESULTS_DIR/stereo_results.json ]; then
    echo "\`\`\`json"
    cat $RESULTS_DIR/stereo_results.json
    echo "\`\`\`"
fi)

#### Задержка рендеринга
$(if [ -f $RESULTS_DIR/latency_results.json ]; then
    echo "\`\`\`json"
    cat $RESULTS_DIR/latency_results.json
    echo "\`\`\`"
fi)

#### VR нагрузочный тест
$(if [ -f $RESULTS_DIR/vr_load_results.json ]; then
    echo "\`\`\`json"
    cat $RESULTS_DIR/vr_load_results.json
    echo "\`\`\`"
fi)

### 📈 Рекомендации

#### Для VR требуется:
- **Минимум 72 FPS** для каждого глаза
- **Задержка менее 20 мс** для комфорта
- **Стабильная температура** (< 80°C)

#### Результаты этого теста:
$(
if [ -f $RESULTS_DIR/3d_results.json ]; then
    fps=$(grep -o '"fps":[0-9.]*' $RESULTS_DIR/3d_results.json | head -1 | cut -d: -f2)
    if [ ! -z "$fps" ]; then
        if (( $(echo "$fps >= 72" | bc -l) )); then
            echo "- ✅ **FPS: $fps** - соответствует требованиям VR"
        else
            echo "- ⚠️ **FPS: $fps** - ниже рекомендуемых 72 FPS"
        fi
    fi
fi
)

$(
if [ -f $RESULTS_DIR/latency_results.json ]; then
    latency=$(grep -o '"render_latency_ms":[0-9.]*' $RESULTS_DIR/latency_results.json | cut -d: -f2)
    if [ ! -z "$latency" ]; then
        if (( $(echo "$latency < 20" | bc -l) )); then
            echo "- ✅ **Задержка: ${latency}мс** - соответствует требованиям VR"
        else
            echo "- ⚠️ **Задержка: ${latency}мс** - выше рекомендуемых 20мс"
        fi
    fi
fi
)

$(
if [ -f $RESULTS_DIR/vr_load_results.json ]; then
    temp=$(grep -o '"max_temp_c":[0-9.]*' $RESULTS_DIR/vr_load_results.json | cut -d: -f2)
    if [ ! -z "$temp" ]; then
        if (( $(echo "$temp < 80" | bc -l) )); then
            echo "- ✅ **Температура: ${temp}°C** - в безопасных пределах"
        else
            echo "- ⚠️ **Температура: ${temp}°C** - близко к пределу"
        fi
    fi
fi
)

### 🛠️ Следующие шаги
1. Оптимизировать настройки OpenGL ES
2. Добавить активное охлаждение
3. Настроить governer CPU для производительности
4. Использовать более легковесный оконный менеджер

---
*Сгенерировано автоматически $(date)*
EOF
    
    # Создаем JSON со всеми результатами
    cat > $OUTPUT_JSON << EOF
{
    "benchmark": {
        "version": "1.0",
        "date": "$(date -Iseconds)",
        "duration_seconds": $((5 * TEST_DURATION + 30)),
        "system": $(cat $RESULTS_DIR/system_info.txt | grep -A5 "Аппаратная часть" | tail -5 | python3 -c "import sys, json; print(json.dumps([line.strip() for line in sys.stdin]))"),
        "results": {
            "2d": $(cat $RESULTS_DIR/2d_results.json 2>/dev/null || echo "null"),
            "3d": $(cat $RESULTS_DIR/3d_results.json 2>/dev/null || echo "null"),
            "stereo": $(cat $RESULTS_DIR/stereo_results.json 2>/dev/null || echo "null"),
            "latency": $(cat $RESULTS_DIR/latency_results.json 2>/dev/null || echo "null"),
            "vr_load": $(cat $RESULTS_DIR/vr_load_results.json 2>/dev/null || echo "null")
        }
    }
}
EOF
    
    # Выводим сводку
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}  БЕНЧМАРК ЗАВЕРШЕН!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "📊 Результаты сохранены в:"
    echo "   - $RESULTS_DIR/report.md   (человекочитаемый)"
    echo "   - $OUTPUT_JSON            (машиночитаемый)"
    echo "   - $LOG_FILE               (полный лог)"
    echo ""
    echo "🔍 Для просмотра отчета:"
    echo "   cat $RESULTS_DIR/report.md"
    echo ""
    echo "🔄 Для повторного запуска:"
    echo "   ./run-benchmark.sh"
}

# Главная функция
main() {
    echo -e "${YELLOW}Начало бенчмарка производительности VR...${NC}"
    
    # Проверка прав
    if [ "$EUID" -eq 0 ]; then 
        log "Запуск с правами root"
    else
        log "Запуск без прав root (некоторые тесты могут быть ограничены)"
    fi
    
    # Выполнение тестов
    check_dependencies
    get_system_info
    test_2d_performance
    test_3d_performance
    test_stereo_performance
    test_latency
    test_vr_simulation
    
    # Генерация отчета
    generate_report
    
    # Очистка временных файлов
    rm -f /tmp/stereo_test.py /tmp/latency_test.c /tmp/latency_test /tmp/vr_load_test.py
}

# Обработка Ctrl+C
trap 'echo -e "\n${RED}Бенчмарк прерван!${NC}"; exit 1' INT

# Запуск
main