""" Client class which operates the game on the client side. """

import sys
import pygame
import constants as c
from paddle import Paddle
from ball import Ball
from network import Network

pygame.init()


class Client:
    """ Client class which holds the client side of the game. """

    def __init__(self, screen, name_1_data):
        self.__screen = screen
        self.__name_1 = name_1_data

        self.__network = Network()
        self.__player = int(self.__network.get_player())

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
        self.__start_game()

    def __start_game(self):
        score_1: int = 0
        score_2: int = 0

        if self.__player == 1:
            name_2: str = "1"
        else:
            name_2: str = "2"
        target_score: int = 10  # game.end_points

        game_running: bool = True
        while game_running:
            try:
                game = self.__network.send("get")
            except:
                print("Coundn't get game...")
                game_running = False
                break

            if self.__player == 2:
                self.__paddle_1.set_coordinates(game.get_pos_1())
            if self.__player == 1:
                self.__paddle_2.set_coordinates(game.get_pos_2())
            self.__ball.set_coordinates(game.get_ball_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_running = False

            if score_1 >= target_score or score_2 >= target_score:
                game_running = False
                print("Someone won")

            pressed_keys = pygame.key.get_pressed()
            if self.__player == 1:
                if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
                    game = self.__network.send("one_up")
                if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
                    game = self.__network.send("one_down")
            if self.__player == 2:
                if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
                    game = self.__network.send("two_up")
                if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
                    game = self.__network.send("two_down")

            if self.__player == 1:
                if self.__ball.get_ball_position()[0] >= c.SCREEN_SIZE[0] - c.BALL_RADIUS * 2:
                    game = self.__network.send("score_one")
            elif self.__player == 2:
                if self.__ball.get_ball_position()[0] <= 0:
                    game = self.__network.send("score_two")
            if self.__player == 1 and (self.__ball.get_ball_position()[1] < c.TOP_LINE_Y + 5 or
                                       self.__ball.get_ball_position()[1] >= c.SCREEN_SIZE[1] - c.BALL_RADIUS * 2):
                game = self.__network.send("reverse_y")

            hit_paddle_1 = pygame.sprite.collide_mask(
                self.__ball, self.__paddle_1)
            hit_paddle_2 = pygame.sprite.collide_mask(
                self.__ball, self.__paddle_2)
            if self.__player == 1 and (hit_paddle_1 or hit_paddle_2):
                game = self.__network.send("bounce")

            self.__all_sprites_list.update()
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

            text = self.__INGAME_TEXT_FONT.render(self.__name_1, 1, c.WHITE)
            self.__screen.blit(text, (100, 20))
            text = self.__INGAME_TEXT_FONT.render(name_2, 1, c.WHITE)
            self.__screen.blit(text, (854, 20))

            pygame.display.flip()

            self.__clock.tick(60)

        pygame.quit()
        sys.exit()
