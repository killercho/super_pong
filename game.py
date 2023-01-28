""" Game class which operates the game. """

import pygame
import constants as c
from paddle import Paddle
from ball import Ball

pygame.init()


class Game:
    """ Game class which holds the game. """

    def __init__(self, id):
        self.__id: int = id
        self.__name_1: str
        self.__name_2: str
        self.__score_1: int = 0
        self.__score_2: int = 0
        self.__paddle_1 = Paddle(c.WHITE, c.PADDLE_WIDTH, c.PADDLE_LENGTH)
        self.__paddle_2 = Paddle(c.WHITE, c.PADDLE_WIDTH, c.PADDLE_LENGTH)
        self.__ball = Ball(c.WHITE, c.BALL_RADIUS)
        self.__ball.set_coordinates(c.SCREEN_SIZE[0] / 2 - 5,
                                    (c.SCREEN_SIZE[1] + c.TOP_LINE_Y / 2) / 2)
        self.__end_points: int = 10  # make dynamic from the host menu!
        self.__ready = False

    def connected(self):
        return self.__ready

    def winner(self):
        if self.__score_1 >= self.__end_points:
            return 1
        return 2

    def ball_update(self):
        self.__ball.update()

    def ball_bounce(self):
        self.__ball.bounce()

    def reverse_ball_x(self):
        self.__ball.reverse_velocity_x

    def reverse_ball_y(self):
        self.__ball.reverse_velocity_y

    def move_one_up(self):
        self.__paddle_1.move_up(c.PADDLE_SPEED)

    def move_one_down(self):
        self.__paddle_1.move_down(c.PADDLE_SPEED)

    def move_two_up(self):
        self.__paddle_2.move_up(c.PADDLE_SPEED)

    def move_two_down(self):
        self.__paddle_2.move_down(c.PADDLE_SPEED)

    def increase_score_one(self):
        self.__score_1 += 1
        # stop the game for some time

    def increase_score_two(self):
        self.__score_2 += 1
        # stop the game for some time

    def set_player_ready(self):
        self.__ready = True

    def get_name_2(self):
        return self.__name_2

    def set_name_2(self, name):
        self.__name_2 = name

    def get_name_1(self):
        return self.__name_1

    def set_name_1(self, name):
        self.__name_1 = name

    def get_end_points(self):
        return self.__end_points

    def get_ball_pos(self):
        return self.__pos_ball

    def set_ball_pos(self, pos):
        self.__pos_ball = pos

    def get_pos_1(self):
        return self.__pos_1

    def set_pos_1(self, pos):
        self.__pos_1 = pos

    def get_pos_2(self):
        return self.__pos_2

    def set_pos_2(self, pos):
        self.__pos_2 = pos
