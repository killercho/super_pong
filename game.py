""" Game class holding the entirety of the game. """

import pygame

pygame.init()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

LINES_WIDTH = 8

INGAME_TEXT_FONT = pygame.font.Font(None, 100)

TOP_LINE_Y = 100

size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Super Pong")

a_name = "Player 1"
b_name = "Player 2"
a_score = 0
b_score = 0

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
    for i in range(0, 720, 72):
        vertical_line = pygame.Surface((8, 64), pygame.SRCALPHA)
        vertical_line.fill((255, 255, 255, 70))
        screen.blit(vertical_line, (636, i))

    pygame.draw.line(screen, WHITE, [0, TOP_LINE_Y], [1280, TOP_LINE_Y], 8)
    pygame.draw.line(screen, WHITE, [639, 0], [639, 100], 8)

    text = INGAME_TEXT_FONT.render(str(a_score), 1, WHITE)
    screen.blit(text, (532, 20))
    text = INGAME_TEXT_FONT.render(str(b_score), 1, WHITE)
    screen.blit(text, (722, 20))

    text = INGAME_TEXT_FONT.render(a_name, 1, WHITE)
    screen.blit(text, (100, 20))
    text = INGAME_TEXT_FONT.render(b_name, 1, WHITE)
    screen.blit(text, (854, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
