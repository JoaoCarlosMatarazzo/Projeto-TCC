import pygame
import time

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
FPS = 60

# Cores
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Posição inicial dos pontos vermelho e azul
red_x, red_y = 400, 100
blue_x, blue_y = 400, 70

# Posição inicial dos pontos amarelos
yellow_points_top = [{'x': x, 'y': 280, 'direction': 1} for x in range(200, 600, 100)]
yellow_points_bottom = [{'x': x, 'y': 320, 'direction': -1} for x in range(200, 600, 100)]

# Estados de movimento
red_moving_down = True
waiting = False
returning = False
wait_start = 0
signal_green = False
signal_timer = None

# Coordenadas da linha de parada
initial_position = 100
stop_position_down = 230
stop_position_up = 370
final_position = 510


def swap_positions():
    global red_y, blue_y
    red_y, blue_y = blue_y, red_y  # Troca de posição verticalmente

# Inicializa o pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulação de Encruzilhada")
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)
    
    # Eventos para fechar a tela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Desenha as paredes (corredores)
    pygame.draw.rect(screen, BLACK, (150, 250, 500, 100))  # Corredor horizontal
    pygame.draw.rect(screen, BLACK, (350, 50, 100, 500))   # Corredor vertical
    
    # Controle das linhas de sinalização
    if signal_timer:
        elapsed = time.time() - signal_timer
        if elapsed >= 2:
            signal_green = True  # Muda para verde após 2 segundos
        if elapsed >= 5:
            signal_green = False  # Volta para vermelho após mais 3 segundos
            signal_timer = None
    
    signal_color = GREEN if signal_green else RED
    pygame.draw.line(screen, signal_color, (350, 250), (450, 250), 5)
    pygame.draw.line(screen, signal_color, (350, 350), (450, 350), 5)
    
    # Movimento dos pontos vermelho e azul
    if not waiting:
        if red_moving_down and not returning:
            if red_y == stop_position_down and signal_timer is None:
                waiting = True
                signal_timer = time.time()  # Inicia temporizador da linha de sinalização
                red_moving_down = True
                wait_start = time.time()
            elif signal_green and time.time() - wait_start >= 3:
                waiting = False  # Após 3s no verde, os pontos continuam
            else:
                red_y += 2
                blue_y += 2
                if red_y >= final_position:
                    red_moving_down = False
                    swap_positions()
                    waiting = True
                    wait_start = time.time()
                    returning = True
        elif returning:
            if red_y == stop_position_up and signal_timer is None:
                waiting = True
                signal_timer = time.time()
                wait_start = time.time()
            elif signal_green and time.time() - wait_start >= 3:
                waiting = False
            else:
                red_y -= 2
                blue_y -= 2
                if red_y <= initial_position:
                    returning = False
                    swap_positions()
                    waiting = True
                    wait_start = time.time()
                    red_moving_down = True
    
    # Movimento dos pontos amarelos
    yellow_moving = not (250 <= red_y <= 350)
    if yellow_moving or waiting:
        for point in yellow_points_top + yellow_points_bottom:
            point['x'] += 2 * point['direction']
            if point['x'] >= 600 or point['x'] <= 200:
                point['direction'] *= -1
    
    # Desenha os pontos
    pygame.draw.circle(screen, RED, (red_x, red_y), 10)
    pygame.draw.circle(screen, BLUE, (blue_x, blue_y), 10)
    
    for point in yellow_points_top + yellow_points_bottom:
        pygame.draw.circle(screen, YELLOW, (point['x'], point['y']), 10)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
