""" A Paddle class implementing the logic behind the paddles in Pong """

import pygame
import constants as c


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(c.BLACK)
        self.image.set_colorkey(c.BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        self.rect.y -= pixels

        if self.rect.y < c.TOP_LINE_Y:
            self.rect.y = c.TOP_LINE_Y

    def move_down(self, pixels):
        self.rect.y += pixels

        if self.rect.y > c.BOTTOM_LINE_Y:
            self.rect.y = c.BOTTOM_LINE_Y

    def set_coordinates(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y
