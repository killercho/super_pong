""" Ball file holding the class Ball. """

from random import randint
import pygame
import constants as c


class Ball(pygame.sprite.Sprite):
    """ Ball class implementing the logic behind all ball movement and physics"""

    def __init__(self, color, radius):
        super().__init__()

        self.image = pygame.Surface([2 * radius, 2 * radius])
        self.image.fill(c.BLACK)

        pygame.draw.circle(self.image, color, (radius, radius), radius)

        self.velocity: int = [randint(4, 8), randint(-8, 8)]

        self.rect = self.image.get_rect()

    def update(self):
        """Method updating the movement of the ball."""
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        """Method implementing the bounce of the ball."""
        self.velocity[0] = -self.velocity[0] + (randint(0, 10) / 100
                                                if self.velocity[0] < 0
                                                else randint(-10, 0) / 100)
        self.velocity[1] = randint(-8, 8)

    def set_coordinates(self, new_x, new_y):
        """Method implementing a way to set coordinates to the ball when needed."""
        self.rect.x = new_x
        self.rect.y = new_y

    def get_ball_position(self):
        """Method allowing for the ball position to be accessed."""
        return self.rect.x, self.rect.y

    def reverse_velocity_x(self):
        """Method reversing x velocity of the ball."""
        self.velocity[0] = -self.velocity[0]

    def reverse_velocity_y(self):
        """Method reversing y velocity of the ball."""
        self.velocity[1] = -self.velocity[1]
