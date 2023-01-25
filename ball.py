""" Ball class implementing the logic behind all ball movements """

import pygame
import constants as c
from random import randint


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, radius):
        super().__init__()

        self.image = pygame.Surface([2 * radius, 2 * radius])
        self.image.fill(c.BLACK)

        pygame.draw.circle(self.image, color, (radius, radius), radius)

        self.velocity: int = [randint(4, 8), randint(-8, 8)]

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0] + (randint(0, 10) / 100
                                                if self.velocity[0] < 0
                                                else randint(-10, 0) / 100)
        self.velocity[1] = randint(-8, 8)

    def set_coordinates(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y
