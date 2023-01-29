""" Power up file holding the main logic of a power up."""

import pygame
from random import randrange
import constants as c


class Power_Up(pygame.sprite.Sprite):
    """Power up class holding the main logic needef for a power up."""

    def __init__(self, side_lenght: int, spawn_x: int, spawn_y: int) -> None:
        super().__init__()

        self.__power = self.__get_random_power()

        self.image = pygame.Surface([side_lenght, side_lenght])
        self.image.fill(c.BLACK)
        self.image.set_colorkey(c.BLACK)

        pygame.draw.rect(self.image, c.WHITE, [0, 0, side_lenght, side_lenght])

        self.rect = self.image.get_rect()
        self.rect.x = spawn_x
        self.rect.y = spawn_y

    def __get_random_power(self):
        rand_index = randrange(0, len(c.AVALIABLE_POWERS))
        return c.AVALIABLE_POWERS[rand_index]

    def get_effect(self):
        return self.__power