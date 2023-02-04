"""Paddle file containing the Paddle class and all of it's logic."""

import pygame
import constants as c


class Paddle(pygame.sprite.Sprite):
    """Paddle class implementing the logic behind the paddles in Pong."""

    def __init__(self, color, width, height):
        super().__init__()

        self.__height = height

        self.image = pygame.Surface([width, height])
        self.image.fill(c.BLACK)
        self.image.set_colorkey(c.BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def move_up(self, pixels: float):
        """Method allowing for the paddles to move up."""
        self.rect.y -= pixels

        if self.rect.y < c.TOP_LINE_Y:
            self.rect.y = c.TOP_LINE_Y

    def move_down(self, pixels: float):
        """Method allowing for the paddles to move down."""
        self.rect.y += pixels

        bottom_correction: int = 0
        if self.__height > c.PADDLE_LENGTH:
            bottom_correction = -(c.INCREASED_LENGHT - c.PADDLE_LENGTH)
        elif self.__height < c.PADDLE_LENGTH:
            bottom_correction = c.DECREASED_LENGHT

        if self.rect.y > c.BOTTOM_LINE_Y + bottom_correction:
            self.rect.y = c.BOTTOM_LINE_Y + bottom_correction

    def get_coordinates(self):
        return (self.rect.x, self.rect.y)

    def set_coordinates(self, new_x, new_y):
        """Method implementing a way to set the coordinates of the paddle whenever needed."""
        self.rect.x = new_x
        self.rect.y = new_y
