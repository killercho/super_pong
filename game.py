""" Game class from where the game is ran. """

from sys import exit
import pygame
import pygame_menu
import constants as c
from paddle import Paddle
from ball import Ball

pygame.init()

class Game:
    """ Game class which starts and operates the game. """

    def __init__(self):
        self.__screen = pygame.display.set_mode(c.SCREEN_SIZE)
        pygame.display.set_caption("Super Pong")
        self.__paddle_1: Paddle = Paddle(
            c.WHITE, c.PADDLE_WIDTH, c.PADDLE_LENGTH)
        self.__paddle_1.set_coordinates(c.A_PADDLE_X, c.A_PADDLE_Y)

        self.__paddle_2: Paddle = Paddle(
            c.WHITE, c.PADDLE_WIDTH, c.PADDLE_LENGTH)
        self.__paddle_2.set_coordinates(c.B_PADDLE_X, c.B_PADDLE_Y)

        self.__ball: Ball = Ball(c.WHITE, c.BALL_RADIUS)
        self.__ball.set_coordinates(c.SCREEN_SIZE[0] / 2 - 5,
                                    (c.SCREEN_SIZE[1] + c.TOP_LINE_Y / 2) / 2)

        self.__all_sprites_list = pygame.sprite.Group()
        self.__all_sprites_list.add(self.__paddle_1)
        self.__all_sprites_list.add(self.__paddle_2)
        self.__all_sprites_list.add(self.__ball)

        self.__INGAME_TEXT_FONT = pygame.font.Font(None, 100)

        self.__clock = pygame.time.Clock()

        # Menu Declarations
        # Main menu
        self.__main_menu = pygame_menu.Menu("Super Pong", c.SCREEN_SIZE[0], c.SCREEN_SIZE[1],
                                            theme=c.MENU_THEME)
        self.__main_menu.add.button("Play", self.__game_settings_menu)
        self.__main_menu.add.button("Options", self.__options_menu_func)
        self.__main_menu.add.button("Quit", pygame_menu.events.EXIT)

        # Start menu
        self.__start_menu = pygame_menu.Menu("Game settings", c.SCREEN_SIZE[0],
                                             c.SCREEN_SIZE[1], theme=c.MENU_THEME)

        self.__name_1_input_field = self.__start_menu.add.text_input(
            "Player 1 name: ", default="")
        self.__name_1_input_field._alignment = pygame_menu.locals.ALIGN_LEFT
        self.__name_1_input_field._margin = (c.SCREEN_SIZE[0] / 10, 0)
        self.__name_2_input_field = self.__start_menu.add.text_input(
            "Player 2 name: ", default="")
        self.__name_2_input_field._alignment = pygame_menu.locals.ALIGN_RIGHT

        self.__start_menu.add.button("Start game", self.__start_game)

        # Options menu
        self.__options_menu = pygame_menu.Menu("Options", c.SCREEN_SIZE[0], c.SCREEN_SIZE[1],
                                               theme=c.MENU_THEME)
        # Options idea -> Music volume and sounds volume,
        #       selector for what power-ups are in the game

        self.__main_menu.mainloop(self.__screen)

    def __game_settings_menu(self):
        self.__main_menu._open(self.__start_menu)

    def __options_menu_func(self):
        self.__main_menu._open(self.__options_menu)

    def __start_game(self):
        name_1_data: str = self.__name_1_input_field.get_value()[:c.MAX_NAME_SYMBOLS]
        name_2_data: str = self.__name_2_input_field.get_value()[:c.MAX_NAME_SYMBOLS]
        name_1: str = c.DEFAULT_NAME_1 if name_1_data == "" else name_1_data
        name_2: str = c.DEFAULT_NAME_2 if name_2_data == "" else name_2_data

        score_1: int = 0
        score_2: int = 0

        target_score: int = 50

        game_running: bool = True
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_running = False

            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_w]:
                self.__paddle_1.move_up(c.PADDLE_SPEED)
            if pressed_keys[pygame.K_s]:
                self.__paddle_1.move_down(c.PADDLE_SPEED)
            if pressed_keys[pygame.K_UP]:
                self.__paddle_2.move_up(c.PADDLE_SPEED)
            if pressed_keys[pygame.K_DOWN]:
                self.__paddle_2.move_down(c.PADDLE_SPEED)

            self.__all_sprites_list.update()

            if self.__ball.get_ball_position()[0] >= c.SCREEN_SIZE[0] - c.BALL_RADIUS * 2:
                score_1 += 1
                self.__ball.reverse_velocity_x()
            elif self.__ball.get_ball_position()[0] <= 0:
                score_2 += 1
                self.__ball.reverse_velocity_x()
            if self.__ball.get_ball_position()[1] < c.TOP_LINE_Y + 5:
                self.__ball.reverse_velocity_y()
            elif self.__ball.get_ball_position()[1] >= c.SCREEN_SIZE[1] - c.BALL_RADIUS * 2:
                self.__ball.reverse_velocity_y()

            hit_paddle_1 = pygame.sprite.collide_mask(
                self.__ball, self.__paddle_1)
            hit_paddle_2 = pygame.sprite.collide_mask(
                self.__ball, self.__paddle_2)
            if hit_paddle_1 or hit_paddle_2:
                self.__ball.bounce()

            self.__screen.fill(c.BLACK)

            self.__all_sprites_list.draw(self.__screen)

            # creating punctured line
            for i in range(0, c.SCREEN_SIZE[1], c.MIDDLE_LINES_STEP):
                vertical_line_size = (c.LINES_WIDTH, 64)
                vertical_line = pygame.Surface(
                    vertical_line_size, pygame.SRCALPHA)
                vertical_line.fill((255, 255, 255, 70))
                self.__screen.blit(vertical_line, (636, i))

            pygame.draw.line(self.__screen, c.WHITE, [0, c.TOP_LINE_Y],
                             [c.SCREEN_SIZE[0], c.TOP_LINE_Y], c.LINES_WIDTH)
            pygame.draw.line(self.__screen, c.WHITE, [639, 0], [639, 100],
                             c.LINES_WIDTH)

            text = self.__INGAME_TEXT_FONT.render(str(score_1), 1, c.WHITE)
            self.__screen.blit(text, (532, 20))
            text = self.__INGAME_TEXT_FONT.render(str(score_2), 1, c.WHITE)
            self.__screen.blit(text, (722, 20))

            text = self.__INGAME_TEXT_FONT.render(name_1, 1, c.WHITE)
            self.__screen.blit(text, (100, 20))
            text = self.__INGAME_TEXT_FONT.render(name_2, 1, c.WHITE)
            self.__screen.blit(text, (854, 20))

            pygame.display.flip()

            if score_1 >= target_score or score_2 >= target_score:
                game_running = False

            self.__clock.tick(60)

        pygame.quit()
        exit()