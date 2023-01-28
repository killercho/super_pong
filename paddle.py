"""Paddle file containing the Paddle class and all of it's logic."""

import pygame
import constants as c


class Paddle(pygame.sprite.Sprite):
    """Paddle class implementing the logic behind the paddles in Pong."""

    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(c.BLACK)
        self.image.set_colorkey(c.BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def move_up(self, pixels):
        """Method allowing for the paddles to move up."""
        self.rect.y -= pixels

        if self.rect.y < c.TOP_LINE_Y:
            self.rect.y = c.TOP_LINE_Y

    def move_down(self, pixels):
        """Method allowing for the paddles to move down."""
        self.rect.y += pixels

        if self.rect.y > c.BOTTOM_LINE_Y:
            self.rect.y = c.BOTTOM_LINE_Y

    def set_coordinates(self, new_x, new_y):
        """Method implementing a way to set the coordinates of the paddle whenever needed."""
        self.rect.x = new_x
        self.rect.y = new_y

    def get_coordinates(self):
        return self.rect.x, self.rect.y
