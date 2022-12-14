""" Game class holding the entirety of the game. """

from sys import exit
import pygame
import pygame_menu
import constants as c
from paddle import Paddle

pygame.init()

screen = pygame.display.set_mode(c.SCREEN_SIZE)
pygame.display.set_caption("Super Pong")

a_paddle = Paddle(c.WHITE, c.PADDLE_WIDTH, c.PADDLE_LENGTH)
a_paddle.rect.x = c.A_PADDLE_X
a_paddle.rect.y = c.A_PADDLE_Y

b_paddle = Paddle(c.WHITE, c.PADDLE_WIDTH, c.PADDLE_LENGTH)
b_paddle.rect.x = c.B_PADDLE_X
b_paddle.rect.y = c.B_PADDLE_Y

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(a_paddle)
all_sprites_list.add(b_paddle)

INGAME_TEXT_FONT = pygame.font.Font(None, 100)

clock = pygame.time.Clock()


def start_game():
    name_1_data = name_1_input_field.get_value()[:c.MAX_NAME_SYMBOLS]
    name_2_data = name_2_input_field.get_value()[:c.MAX_NAME_SYMBOLS]
    name_1 = c.DEFAULT_NAME_1 if name_1_data == "" else name_1_data
    name_2 = c.DEFAULT_NAME_2 if name_2_data == "" else name_2_data

    score_1 = 0
    score_2 = 0

    game_running = True
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            a_paddle.move_up(c.PADDLE_SPEED)
        if pressed_keys[pygame.K_s]:
            a_paddle.move_down(c.PADDLE_SPEED)
        if pressed_keys[pygame.K_UP]:
            b_paddle.move_up(c.PADDLE_SPEED)
        if pressed_keys[pygame.K_DOWN]:
            b_paddle.move_down(c.PADDLE_SPEED)

        all_sprites_list.update()

        screen.fill(c.BLACK)

        all_sprites_list.draw(screen)

        # creating punctured line
        for i in range(0, c.SCREEN_SIZE[1], c.MIDDLE_LINES_STEP):
            vertical_line_size = (c.LINES_WIDTH, 64)
            vertical_line = pygame.Surface(vertical_line_size, pygame.SRCALPHA)
            vertical_line.fill((255, 255, 255, 70))
            screen.blit(vertical_line, (636, i))

        pygame.draw.line(screen, c.WHITE, [0, c.TOP_LINE_Y],
                         [c.SCREEN_SIZE[0], c.TOP_LINE_Y], c.LINES_WIDTH)
        pygame.draw.line(screen, c.WHITE, [639, 0], [639, 100],
                         c.LINES_WIDTH)

        text = INGAME_TEXT_FONT.render(str(score_1), 1, c.WHITE)
        screen.blit(text, (532, 20))
        text = INGAME_TEXT_FONT.render(str(score_2), 1, c.WHITE)
        screen.blit(text, (722, 20))

        text = INGAME_TEXT_FONT.render(name_1, 1, c.WHITE)
        screen.blit(text, (100, 20))
        text = INGAME_TEXT_FONT.render(name_2, 1, c.WHITE)
        screen.blit(text, (854, 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    exit()


def game_settings_menu():
    main_menu._open(start_menu)


def options_menu_func():
    main_menu._open(options_menu)


def quit_game():
    pygame.quit()
    exit()


# Menu Declarations


main_menu = pygame_menu.Menu("Super Pong", c.SCREEN_SIZE[0], c.SCREEN_SIZE[1],
                             theme=c.MENU_THEME)
main_menu.add.button("Play", game_settings_menu)
main_menu.add.button("Options", options_menu_func)
main_menu.add.button("Quit", pygame_menu.events.EXIT)

start_menu = pygame_menu.Menu("Game settings", c.SCREEN_SIZE[0],
                              c.SCREEN_SIZE[1], theme=c.MENU_THEME)
name_1_input_field = start_menu.add.text_input("Player 1 name: ", default="")
name_2_input_field = start_menu.add.text_input("Player 2 name: ", default="")
start_menu.add.button("Start game", start_game)

options_menu = pygame_menu.Menu("Options", c.SCREEN_SIZE[0], c.SCREEN_SIZE[1],
                                theme=c.MENU_THEME)
# Options idea -> Music volume and sounds volume,
#       selector for what power-ups are in the game

main_menu.mainloop(screen)
