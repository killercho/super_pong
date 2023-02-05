"""Paddle file containing the Paddle class and all of it's logic."""

import pygame
import constants as c
from power_up import Power_Up


class Paddle(pygame.sprite.Sprite):
    """Paddle class implementing the logic behind the paddles in Pong."""

    def __init__(self, color, width, height):
        super().__init__()

        self.__height: int = height
        self.__width: int = width
        self.__color = color
        self.__speed: float = c.PADDLE_SPEED
        self.__velocity: int = 0

        self.__powers = []

        self.image = pygame.Surface([self.__width, self.__height])
        self.image.fill(c.BLACK)
        self.image.set_colorkey(c.BLACK)

        pygame.draw.rect(self.image, color, [
                         0, 0, self.__width, self.__height])

        self.rect = self.image.get_rect()

    def __change_size(self, new_size: int):
        self.__height = new_size
        self.image = pygame.Surface([self.__width, self.__height])
        self.image.fill(c.BLACK)
        self.image.set_colorkey(c.BLACK)
        pygame.draw.rect(self.image, self.__color, [
                         0, 0, self.__width, self.__height])
        old_x = self.rect.x
        old_y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.rect.y = old_y

    def __apply_power(self, power: Power_Up):
        effect = power.get_effect()
        if effect == "up_speed_player":
            self.__speed = c.SPEED_INCREASE
        elif effect == "down_speed_player":
            self.__speed = c.SPEED_DECREASE
        elif effect == "increase_own_paddle":
            self.__change_size(c.INCREASED_LENGHT)
        elif effect == "decrease_opponent_paddle":
            self.__change_size(c.DECREASED_LENGHT)

    def __reverse_effects(self, effect: str):
        if effect == "up_speed_player" or effect == "down_speed_player":
            self.__speed = c.PADDLE_SPEED
        elif effect == "increase_own_paddle" or effect == "decrease_opponent_paddle":
            self.__change_size(c.PADDLE_LENGTH)

    def get_coordinates(self):
        return (self.rect.x, self.rect.y)

    def set_coordinates(self, new_x, new_y):
        """Method implementing a way to set the coordinates of the paddle whenever needed."""
        self.rect.x = new_x
        self.rect.y = new_y

    def get_speed(self):
        return self.__speed

    def set_speed(self, new_speed: int):
        self.__speed = new_speed

    def get_velocity(self):
        return self.__velocity

    def add_power(self, power: Power_Up):
        powers_arr = [p.get_effect() for p in self.__powers]
        if power.get_effect() not in powers_arr:
            self.__powers.append(power)
            self.__apply_power(power)
        else:
            pass

    def reverse_all_powers(self):
        for power in self.__powers:
            self.__reverse_effects(power.get_effect())
        self.__powers.clear()

    def update_powers(self):
        for power in self.__powers:
            effect = power.update_validity()
            if effect != "":
                self.__powers.remove(power)
                self.__reverse_effects(effect)

    def update(self):
        self.__velocity = 0

    def move_up(self):
        """Method allowing for the paddles to move up."""
        self.rect.y -= self.__speed
        self.__velocity = self.__speed

        if self.rect.y < c.TOP_LINE_Y:
            self.rect.y = c.TOP_LINE_Y

    def move_down(self):
        """Method allowing for the paddles to move down."""
        self.rect.y += self.__speed
        self.__velocity = self.__speed

        bottom_correction: int = 0
        if self.__height > c.PADDLE_LENGTH:
            bottom_correction = -(c.INCREASED_LENGHT - c.PADDLE_LENGTH)
        elif self.__height < c.PADDLE_LENGTH:
            bottom_correction = c.DECREASED_LENGHT

        if self.rect.y > c.BOTTOM_LINE_Y + bottom_correction:
            self.rect.y = c.BOTTOM_LINE_Y + bottom_correction
