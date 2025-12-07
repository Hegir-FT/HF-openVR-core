/*
 * Test Stereo для VR шлема на Orange Pi 5
 * Компиляция: g++ test-stereo-opengl.cpp -o test-stereo -lglfw -lGL -lGLEW
 */

#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <cmath>

// Размеры окна (под дисплей 1920x1080)
const int WIDTH = 1920;
const int HEIGHT = 1080;

// Цвета для левого и правого глаз
const GLfloat LEFT_EYE_COLOR[] = {1.0f, 0.0f, 0.0f, 1.0f};  // Красный
const GLfloat RIGHT_EYE_COLOR[] = {0.0f, 0.0f, 1.0f, 1.0f}; // Синий

// Вершины треугольника
const GLfloat vertices[] = {
     0.0f,  0.5f, 0.0f,  // Верхняя вершина
    -0.5f, -0.5f, 0.0f,  // Левая нижняя
     0.5f, -0.5f, 0.0f   // Правая нижняя
};

// Простой вершинный шейдер
const char* vertexShaderSource = R"(
    #version 330 core
    layout (location = 0) in vec3 aPos;
    
    uniform float time;
    uniform int eye;  // 0 - левый, 1 - правый
    
    void main()
    {
        // Добавляем параллакс для стереоэффекта
        float parallax = 0.05;
        vec3 pos = aPos;
        
        if (eye == 0) {
            pos.x -= parallax * sin(time);
        } else {
            pos.x += parallax * sin(time);
        }
        
        // Вращение по Y
        float angle = time;
        mat2 rotation = mat2(cos(angle), -sin(angle),
                             sin(angle), cos(angle));
        
        pos.xz = rotation * pos.xz;
        
        gl_Position = vec4(pos, 1.0);
    }
)";

// Простой фрагментный шейдер
const char* fragmentShaderSource = R"(
    #version 330 core
    out vec4 FragColor;
    
    uniform vec4 color;
    uniform float time;
    
    void main()
    {
        // Добавляем пульсацию цвета
        float pulse = 0.5 + 0.5 * sin(time * 2.0);
        FragColor = vec4(color.rgb * pulse, 1.0);
    }
)";

// Компиляция шейдера
GLuint compileShader(GLenum type, const char* source) {
    GLuint shader = glCreateShader(type);
    glShaderSource(shader, 1, &source, NULL);
    glCompileShader(shader);
    
    // Проверка ошибок
    GLint success;
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
    if (!success) {
        char infoLog[512];
        glGetShaderInfoLog(shader, 512, NULL, infoLog);
        std::cerr << "Ошибка компиляции шейдера:\n" << infoLog << std::endl;
    }
    
    return shader;
}

// Создание шейдерной программы
GLuint createShaderProgram() {
    GLuint vertexShader = compileShader(GL_VERTEX_SHADER, vertexShaderSource);
    GLuint fragmentShader = compileShader(GL_FRAGMENT_SHADER, fragmentShaderSource);
    
    GLuint program = glCreateProgram();
    glAttachShader(program, vertexShader);
    glAttachShader(program, fragmentShader);
    glLinkProgram(program);
    
    // Проверка ошибок линковки
    GLint success;
    glGetProgramiv(program, GL_LINK_STATUS, &success);
    if (!success) {
        char infoLog[512];
        glGetProgramInfoLog(program, 512, NULL, infoLog);
        std::cerr << "Ошибка линковки шейдерной программы:\n" << infoLog << std::endl;
    }
    
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);
    
    return program;
}

int main() {
    std::cout << "Запуск стерео теста для VR шлема" << std::endl;
    std::cout << "=================================" << std::endl;
    std::cout << "Левый глаз: Красный треугольник" << std::endl;
    std::cout << "Правый глаз: Синий треугольник" << std::endl;
    std::cout << "Нажмите ESC для выхода" << std::endl;
    
    // Инициализация GLFW
    if (!glfwInit()) {
        std::cerr << "Ошибка инициализации GLFW" << std::endl;
        return -1;
    }
    
    // Настройка OpenGL контекста
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    
    // Создание окон для левого и правого глаз
    GLFWwindow* leftWindow = glfwCreateWindow(WIDTH, HEIGHT, "VR Test - Левый глаз", NULL, NULL);
    GLFWwindow* rightWindow = glfwCreateWindow(WIDTH, HEIGHT, "VR Test - Правый глаз", NULL, NULL);
    
    if (!leftWindow || !rightWindow) {
        std::cerr << "Ошибка создания окон" << std::endl;
        glfwTerminate();
        return -1;
    }
    
    // Настройка левого окна
    glfwMakeContextCurrent(leftWindow);
    glfwSetWindowPos(leftWindow, 0, 0);
    
    // Инициализация GLEW для левого окна
    glewExperimental = GL_TRUE;
    if (glewInit() != GLEW_OK) {
        std::cerr << "Ошибка инициализации GLEW" << std::endl;
        return -1;
    }
    
    // Создание шейдерной программы
    GLuint shaderProgram = createShaderProgram();
    glUseProgram(shaderProgram);
    
    // Создание VAO и VBO
    GLuint VAO, VBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    
    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    
    // Настройка атрибутов вершин
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    
    // Получение uniform-переменных
    GLint timeLoc = glGetUniformLocation(shaderProgram, "time");
    GLint colorLoc = glGetUniformLocation(shaderProgram, "color");
    GLint eyeLoc = glGetUniformLocation(shaderProgram, "eye");
    
    // Основной цикл
    while (!glfwWindowShouldClose(leftWindow) && !glfwWindowShouldClose(rightWindow)) {
        float time = glfwGetTime();
        
        // Рендеринг для левого глаза
        glfwMakeContextCurrent(leftWindow);
        glClearColor(0.1f, 0.1f, 0.1f, 1.0f);  // Темно-серый фон
        glClear(GL_COLOR_BUFFER_BIT);
        
        glUseProgram(shaderProgram);
        glUniform1f(timeLoc, time);
        glUniform4fv(colorLoc, 1, LEFT_EYE_COLOR);
        glUniform1i(eyeLoc, 0);  // Левый глаз
        
        glBindVertexArray(VAO);
        glDrawArrays(GL_TRIANGLES, 0, 3);
        
        // Рендеринг для правого глаза
        glfwMakeContextCurrent(rightWindow);
        glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        
        glUniform4fv(colorLoc, 1, RIGHT_EYE_COLOR);
        glUniform1i(eyeLoc, 1);  // Правый глаз
        
        glDrawArrays(GL_TRIANGLES, 0, 3);
        
        // Обмен буферов
        glfwSwapBuffers(leftWindow);
        glfwSwapBuffers(rightWindow);
        
        // Обработка событий
        glfwPollEvents();
        
        // Проверка нажатия ESC
        if (glfwGetKey(leftWindow, GLFW_KEY_ESCAPE) == GLFW_PRESS ||
            glfwGetKey(rightWindow, GLFW_KEY_ESCAPE) == GLFW_PRESS) {
            break;
        }
        
        // FPS ограничение
        glfwWaitEventsTimeout(0.016);  // ~60 FPS
    }
    
    // Очистка
    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteProgram(shaderProgram);
    
    glfwDestroyWindow(leftWindow);
    glfwDestroyWindow(rightWindow);
    glfwTerminate();
    
    std::cout << "Тест завершен" << std::endl;
    return 0;
}
