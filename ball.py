""" Ball file holding the class Ball. """

from random import randint
from math import cos, sin
import pygame
from power_up import Power_Up, Powers
import constants as c


class Ball(pygame.sprite.Sprite):
    """ Ball class implementing the logic behind all ball movement and physics"""

    def __init__(self, color, radius) -> None:
        super().__init__()

        self.__color: tuple = color
        self.__radius: float = radius

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

    def __change_surface(self, new_radius: float, new_color: tuple) -> None:
        self.__radius = new_radius
        self.__color = new_color
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
        effect: Powers = power.get_effect()
        if effect is Powers.SMALLER_BALL:
            self.__change_surface(c.BALL_DECREASED_RADIUS, c.WHITE)
        elif effect is Powers.BIGGER_BALL:
            self.__change_surface(c.BALL_INCREASED_RADIUS, c.WHITE)
        elif effect is Powers.INVISIBLE_BALL:
            self.__change_surface(c.BALL_RADIUS, c.BLACK)

    def __reverse_effects(self, effect: Powers) -> None:
        if effect is Powers.SMALLER_BALL \
            or effect is Powers.BIGGER_BALL \
                or effect is Powers.INVISIBLE_BALL:
            self.__change_surface(c.BALL_RADIUS, c.WHITE)

    def add_power(self, new_power: Power_Up) -> None:
        powers_arr: list = [p.get_effect() for p in self.__powers]
        if new_power.get_effect() not in powers_arr:
            new_power.set_active()
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
            if effect is not Powers.NULL_POWER:
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

    def bounce(self, additional_velocity: int, paddle_y: int, paddle_height: int) -> None:
        """Method implementing the bounce of the ball."""
        intersectionY: int = paddle_y + paddle_height / 2 - self.rect.y
        normalized_intersection: float = intersectionY / (paddle_height / 2)
        bounce_angle: float = normalized_intersection * c.BALL_MAX_BOUNCE

        more_speed: int = randint(
            0, 2) if self.__velocity[0] < 0 else randint(-2, 0)
        self.__velocity[0] = -self.__velocity[0] + more_speed

        y_sign: int = 1 if self.__velocity[1] < 0 else -1
        self.__velocity[1] = y_sign * additional_velocity + \
            self.__velocity[1]*(sin(bounce_angle))

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

    def get_radius(self) -> float:
        return self.__radius

    def reverse_velocity_x(self) -> None:
        """Method reversing x velocity of the ball."""
        self.__velocity[0] = -self.__velocity[0]

    def reverse_velocity_y(self) -> None:
        """Method reversing y velocity of the ball."""
        self.__velocity[1] = -self.__velocity[1]
