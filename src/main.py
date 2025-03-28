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
red_moving_down = True  # Define a direção do movimento do vermelho e azul
waiting = False  # Estado de espera dos pontos vermelho e azul
returning = False  # Indica se os pontos estão retornando
wait_start = 0  # Para controle do tempo de espera
signal_start = time.time()  # Tempo inicial da linha de sinalização
signal_green = False  # Indica se a linha está verde
signal_waiting = False  # Indica se os pontos estão esperando na linha vermelha


def swap_positions():
    global red_x, red_y, blue_x, blue_y
    red_y, blue_y = blue_y, red_y  # Troca de posição verticalmente

# Inicializa o pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulação de Encruzilhada")
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)
    
    # Eventos se a tela foi fechada
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Desenha as paredes (corredores)
    pygame.draw.rect(screen, BLACK, (150, 250, 500, 100))  # Corredor horizontal
    pygame.draw.rect(screen, BLACK, (350, 50, 100, 500))   # Corredor vertical
    
    # Controle das linhas de sinalização
    if time.time() - signal_start >= 2:
        signal_green = not signal_green
        signal_start = time.time()
    
    signal_color = GREEN if signal_green else RED
    pygame.draw.line(screen, signal_color, (350, 250), (450, 250), 5)
    pygame.draw.line(screen, signal_color, (350, 350), (450, 350), 5)
    
    # Movimento dos pontos vermelho e azul
    if not waiting:
        if red_moving_down and not returning:
            if 240 <= red_y <= 250 and not signal_green and not signal_waiting:
                signal_waiting = True
                wait_start = time.time()
            elif signal_waiting and time.time() - wait_start >= 1:  # Espera 1 segundo antes de continuar
                signal_waiting = False
            else:
                red_y += 2
                blue_y += 2
                if red_y >= 510:
                    red_moving_down = False
                    swap_positions()
                    waiting = True
                    wait_start = time.time()
                    returning = True
        elif returning:
            if 340 <= red_y <= 350 and not signal_green and not signal_waiting:
                signal_waiting = True
                wait_start = time.time()
            elif signal_waiting and time.time() - wait_start >= 1:  # Espera 1 segundo antes de continuar
                signal_waiting = False
            else:
                red_y -= 2
                blue_y -= 2
                if red_y <= 100:
                    returning = False
                    swap_positions()
                    waiting = True
                    wait_start = time.time()
                    red_moving_down = True
    elif waiting:
        if time.time() - wait_start >= 3.3:  # Espera o tempo necessário e volta a se mover
            waiting = False
    
    # Verifica se os pontos vermelho e azul estão na frente dos amarelos
    yellow_moving = not (250 <= red_y <= 350)
    
    # Movimento dos pontos amarelos
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
