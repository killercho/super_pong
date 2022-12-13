""" Game class holding the entirety of the game. """

import pygame

pygame.init()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

LINES_WIDTH = 8

size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Super Pong")

clock = pygame.time.Clock()

game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False

    screen.fill(BLACK)

    # creating punctured line
    for i in range(10):
        vertical_line = pygame.Surface((1, 64), pygame.SRCALPHA)
        vertical_line.fill((255, 255, 255, 70))
        screen.blit(vertical_line, (636, i * 72))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
