"""Paddle file containing the Paddle class and all of it's logic."""

import pygame
import constants as c
from power_up import Power_Up


class Paddle(pygame.sprite.Sprite):
    """Paddle class implementing the logic behind the paddles in Pong."""

    def __init__(self, color: tuple, width: int, height: int) -> None:
        super().__init__()

        self.__height: int = height
        self.__width: int = width
        self.__color: tuple = color
        self.__speed: float = c.PADDLE_SPEED
        self.__velocity: int = 0

        self.__powers: list = []

        self.image: pygame.Surface = pygame.Surface(
            [self.__width, self.__height])
        self.image.fill(c.BLACK)
        self.image.set_colorkey(c.BLACK)

        pygame.draw.rect(self.image, self.__color, [
                         0, 0, self.__width, self.__height])

        self.rect: pygame.Rect = self.image.get_rect()

    def __change_size(self, new_size: int) -> None:
        self.__height = new_size
        self.image = pygame.Surface([self.__width, self.__height])
        self.image.fill(c.BLACK)
        self.image.set_colorkey(c.BLACK)
        pygame.draw.rect(self.image, self.__color, [
                         0, 0, self.__width, self.__height])
        old_x: int = self.rect.x
        old_y: int = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.rect.y = old_y

    def __apply_power(self, power: Power_Up) -> None:
        effect: str = power.get_effect()
        if effect == "up_speed_player":
            self.__speed = c.SPEED_INCREASE
        elif effect == "down_speed_player":
            self.__speed = c.SPEED_DECREASE
        elif effect == "increase_own_paddle":
            self.__change_size(c.INCREASED_LENGHT)
        elif effect == "decrease_opponent_paddle":
            self.__change_size(c.DECREASED_LENGHT)

    def __reverse_effects(self, effect: str) -> None:
        if effect == "up_speed_player" or effect == "down_speed_player":
            self.__speed = c.PADDLE_SPEED
        elif effect == "increase_own_paddle" or effect == "decrease_opponent_paddle":
            self.__change_size(c.PADDLE_LENGTH)

    def get_coordinates(self) -> tuple:
        return (self.rect.x, self.rect.y)

    def set_coordinates(self, new_x: int, new_y: int) -> None:
        """Method implementing a way to set the coordinates of the paddle whenever needed."""
        self.rect.x = new_x
        self.rect.y = new_y

    def get_speed(self) -> int:
        return self.__speed

    def set_speed(self, new_speed: int) -> None:
        self.__speed = new_speed

    def get_velocity(self) -> int:
        return self.__velocity

    def add_power(self, new_power: Power_Up) -> None:
        powers_arr: list = [p.get_effect() for p in self.__powers]
        if new_power.get_effect() not in powers_arr:
            self.__powers.append(new_power)
            self.__apply_power(new_power)
        else:
            for power in self.__powers:
                if power.get_effect() == new_power.get_effect():
                    power.reset_timer()

    def reverse_all_powers(self) -> None:
        for power in self.__powers:
            self.__reverse_effects(power.get_effect())
        self.__powers.clear()

    def update_powers(self) -> None:
        for power in self.__powers:
            effect: str = power.update_validity()
            if effect != "":
                self.__powers.remove(power)
                self.__reverse_effects(effect)

    def update(self) -> None:
        self.__velocity = 0

    def move_up(self) -> None:
        """Method allowing for the paddles to move up."""
        self.rect.y -= self.__speed
        self.__velocity = self.__speed

        if self.rect.y < c.TOP_LINE_Y:
            self.rect.y = c.TOP_LINE_Y

    def move_down(self) -> None:
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
