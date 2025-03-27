import pygame
import time

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Cores
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Posição inicial dos pontos
red_x, red_y = 400, 100
blue_x, blue_y = 400, 150

yellow_points = [{'x': x, 'y': 300, 'direction': 1} for x in range(200, 600, 100)]

# Estados de movimento
red_moving_down = True  # Define a direção do movimento do vermelho e azul
waiting = False  # Estado de espera dos pontos vermelho e azul

# Inicializa o pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulação de Encruzilhada")
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Desenha as paredes (corredores)
    pygame.draw.rect(screen, BLACK, (150, 250, 500, 100))  # Corredor horizontal
    pygame.draw.rect(screen, BLACK, (350, 50, 100, 500))   # Corredor vertical
    
    # Movimento dos pontos vermelho e azul
    if not waiting:
        if red_moving_down:
            red_y += 2
            blue_y += 2
            if red_y >= 450:  # Ponto de parada antes de sair do corredor
                red_moving_down = False
                waiting = True
                wait_start = time.time()
        else:
            red_y -= 2
            blue_y -= 2
            if red_y <= 100:  # Ponto de retorno
                red_moving_down = True
                waiting = True
                wait_start = time.time()
    else:
        if time.time() - wait_start >= 5:  # Aguarda 5 segundos
            waiting = False
    
    # Verifica se os pontos vermelho e azul estão na frente dos amarelos
    yellow_moving = not (250 <= red_y <= 350)
    
    # Movimento dos pontos amarelos
    if yellow_moving or waiting:  # Mantém o movimento quando os pontos vermelho e azul estão parados
        for point in yellow_points:
            point['x'] += 2 * point['direction']
            if point['x'] >= 600 or point['x'] <= 200:
                point['direction'] *= -1
    
    # Desenha os pontos
    pygame.draw.circle(screen, RED, (red_x, red_y), 10)
    pygame.draw.circle(screen, BLUE, (blue_x, blue_y), 10)
    
    for point in yellow_points:
        pygame.draw.circle(screen, YELLOW, (point['x'], point['y']), 10)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
