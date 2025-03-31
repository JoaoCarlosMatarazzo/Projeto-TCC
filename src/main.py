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
ROXO = (128, 0, 128)
CYAN = (0, 255, 255)

# Posição inicial dos pontos vermelho e azul
red_x, red_y = 400, 100
blue_x, blue_y = 400, 70

# Posição inicial dos pontos amarelos
yellow_points_top = [{'x': x, 'y': 270, 'direction': 1} for x in range(200, 600, 50)]
yellow_points_bottom = [{'x': x, 'y': 330, 'direction': -1} for x in range(200, 600, 50)]

# Estados de movimento
red_moving_down = True
waiting = False
returning = False
wait_start = None  # Tempo de espera dos pontos
signal_timer = None  # Timer para mudar a linha de cor
signal_green = False  # Estado da linha de sinalização

# Coordenadas da linha de parada
initial_position = 100
stop_position_down = 230
stop_position_up = 370
final_position = 510

# Coordenadas da área central da encruzilhada
center_left = 350
center_right = 450

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

    # Desenha a linha roxa vertical no centro do corredor vertical
    pygame.draw.line(screen, CYAN, (400, 100), (400, 510), 5)  # (Roxo)
    
    # Controle das linhas de sinalização
    if signal_timer is not None:
        elapsed_time = time.time() - signal_timer
        if elapsed_time >= 2:  # Após 2s, a linha fica verde
            signal_green = True
        if elapsed_time >= 5:  # Após 5s totais (2s + 3s), a linha volta a ser vermelha
            signal_green = False
            signal_timer = None  # Reseta o temporizador da linha

    # Define a cor da linha de sinalização
    signal_color = GREEN if signal_green else RED
    pygame.draw.line(screen, signal_color, (350, 250), (450, 250), 5)
    pygame.draw.line(screen, signal_color, (350, 350), (450, 350), 5)
    
    # Movimento dos pontos vermelho e azul
    if not waiting:
        if red_moving_down and not returning:
            if red_y == stop_position_down and signal_timer is None:
                waiting = True
                signal_timer = time.time()  # Inicia temporizador da linha de sinalização
                wait_start = time.time()  # Inicia tempo de espera dos pontos
            elif signal_green and wait_start is not None and time.time() - wait_start >= 3:  
                # Após 3s no verde, os pontos continuam
                waiting = False  
                wait_start = None  # Reseta o tempo de espera dos pontos
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
                signal_timer = time.time()  # Inicia temporizador da linha de sinalização
                wait_start = time.time()  # Inicia tempo de espera dos pontos
            elif signal_green and wait_start is not None and time.time() - wait_start >= 3:
                # Após 3s no verde, os pontos continuam
                waiting = False  
                wait_start = None  # Reseta o tempo de espera dos pontos
            else:
                red_y -= 2
                blue_y -= 2
                if red_y <= initial_position:
                    returning = False
                    swap_positions()
                    waiting = True
                    wait_start = time.time()
                    red_moving_down = True

    elif waiting and wait_start is not None:
        if time.time() - wait_start >= 3:  # Tempo de espera dos pontos antes de atravessar
            waiting = False
            wait_start = None
    
    # Movimento dos pontos amarelos
    if not signal_green:
        for point in yellow_points_top + yellow_points_bottom:
            point['x'] += 2 * point['direction']
            if point['x'] > 598:  # Margem de segurança antes de inverter
                point['x'] = 598  # Mantém dentro dos limites
                point['direction'] *= -1
            elif point['x'] < 202:  # Margem de segurança antes de inverter
                point['x'] = 202  # Mantém dentro dos limites
                point['direction'] *= -1

    
    # Desenha os pontos
    pygame.draw.circle(screen, RED, (red_x, red_y), 10)
    pygame.draw.circle(screen, BLUE, (blue_x, blue_y), 10)
    
    for point in yellow_points_top + yellow_points_bottom:
        if not (center_left <= point['x'] <= center_right and signal_green):
            pygame.draw.circle(screen, YELLOW, (point['x'], point['y']), 10)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
