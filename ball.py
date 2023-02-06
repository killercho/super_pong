""" Ball file holding the class Ball. """

from random import randint
import pygame
from power_up import Power_Up
import constants as c


class Ball(pygame.sprite.Sprite):
    """ Ball class implementing the logic behind all ball movement and physics"""

    def __init__(self, color, radius) -> None:
        super().__init__()

        self.__color = color
        self.__radius = radius

        self.__last_hit: int = -1
        self.__powers: list = []

        self.image: pygame.Surface = pygame.Surface(
            [2 * self.__radius, 2 * self.__radius])
        self.image.fill(c.BLACK)

        pygame.draw.circle(self.image, self.__color,
                           (self.__radius, self.__radius), self.__radius)

        random_speed_x: int = randint(-c.BALL_MAX_VEL, c.BALL_MAX_VEL)
        while -c.BALL_MIN_VEL < random_speed_x < c.BALL_MIN_VEL:
            random_speed_x = randint(-c.BALL_MAX_VEL, c.BALL_MAX_VEL)
        self.__velocity: list = [random_speed_x,
                                 randint(-c.BALL_MAX_VEL, c.BALL_MAX_VEL)]

        self.rect: pygame.Rect = self.image.get_rect()

    def __change_size(self, new_radius: float) -> None:
        self.__radius = new_radius
        self.image: pygame.Surface = pygame.Surface(
            [2 * self.__radius, 2 * self.__radius])
        self.image.fill(c.BLACK)

        pygame.draw.circle(self.image, self.__color,
                           (self.__radius, self.__radius), self.__radius)
        old_x: int = self.rect.x
        old_y: int = self.rect.y
        self.rect = self.image.get_rect()
        self.set_coordinates(old_x, old_y)

    def __apply_power(self, power: Power_Up) -> None:
        effect: str = power.get_effect()
        if effect == "smaller_ball":
            self.__change_size(c.BALL_DECREASED_RADIUS)
        elif effect == "bigger_ball":
            self.__change_size(c.BALL_INCREASED_RADIUS)

    def __reverse_effects(self, effect: str) -> None:
        if effect == "smaller_ball" or effect == "bigger_ball":
            self.__change_size(c.BALL_RADIUS)

    def add_power(self, power: Power_Up) -> None:
        powers_arr: list = [p.get_effect() for p in self.__powers]
        if power.get_effect() not in powers_arr:
            self.__powers.append(power)
            self.__apply_power(power)
        else:
            pass

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

    def reset_ball(self) -> None:
        """Method giving the ball a new random velocity, used after the break 
            because of a score."""
        random_speed_x: int = randint(-c.BALL_MAX_VEL, c.BALL_MAX_VEL)
        while -c.BALL_MIN_VEL < random_speed_x < c.BALL_MIN_VEL:
            random_speed_x = randint(-c.BALL_MAX_VEL, c.BALL_MAX_VEL)
        self.__velocity = [random_speed_x,
                           randint(-c.BALL_MAX_VEL, c.BALL_MAX_VEL)]
        self.__last_hit = -1
        self.set_coordinates(c.BALL_X, c.BALL_Y)

    def update(self) -> None:
        """Method updating the movement of the ball."""
        self.rect.x += self.__velocity[0]
        self.rect.y += self.__velocity[1]

    def bounce(self, additional_velocity: int) -> None:
        """Method implementing the bounce of the ball."""
        more_speed: int = randint(
            0, 2) if self.__velocity[0] < 0 else randint(-2, 0)
        self.__velocity[0] = -self.__velocity[0] + more_speed

        y_sign: int = 1 if self.__velocity[1] < 0 else -1
        self.__velocity[1] = y_sign * additional_velocity + randint(0, 4)

    def get_last_hit(self) -> None:
        return self.__last_hit

    def set_last_hit(self, player: int) -> None:
        self.__last_hit = player

    def set_coordinates(self, new_x: int, new_y: int) -> None:
        """Method implementing a way to set coordinates to the ball when needed."""
        self.rect.x = new_x
        self.rect.y = new_y

    def get_ball_position(self) -> None:
        """Method allowing for the ball position to be accessed."""
        return self.rect.x, self.rect.y

    def reverse_velocity_x(self) -> None:
        """Method reversing x velocity of the ball."""
        self.__velocity[0] = -self.__velocity[0]

    def reverse_velocity_y(self) -> None:
        """Method reversing y velocity of the ball."""
        self.__velocity[1] = -self.__velocity[1]
