""" Ball file holding the class Ball. """

import os
from random import randint
from math import cos, sin
import pygame
from power_up import Power_Up, Powers
import constants as c


class Ball(pygame.sprite.Sprite):
    """ Ball class implementing the logic behind all ball movement and physics"""

    def __init__(self, color: tuple[int, int, int], radius: int, sound_volume: float) -> None:
        super().__init__()

        self.__color: tuple[int, int, int] = color
        self.__radius: float = radius

        self.__bounce_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            os.path.join(c.ASSETS_FOLDER, "bounce.wav"))
        self.__bounce_sound.set_volume(sound_volume)

        self.__last_hit: int = -1
        self.__powers: list[Power_Up] = []
        self.__gravity_effected: bool = False

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
        """ Method changing the radius or the colour of the ball. """
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
        """ Method applying a specific power to the ball. """
        effect: Powers = power.get_effect()
        if effect is Powers.SMALLER_BALL:
            self.__change_surface(c.BALL_DECREASED_RADIUS, c.WHITE)
        elif effect is Powers.BIGGER_BALL:
            self.__change_surface(c.BALL_INCREASED_RADIUS, c.WHITE)
        elif effect is Powers.INVISIBLE_BALL:
            self.__change_surface(c.BALL_RADIUS, c.BLACK)
        elif effect is Powers.GRAVITY:
            self.__gravity_effected = True

    def __reverse_effects(self, effect: Powers) -> None:
        """ Method reversing a specific effect applied previously to the ball. """
        if effect is Powers.SMALLER_BALL \
            or effect is Powers.BIGGER_BALL \
                or effect is Powers.INVISIBLE_BALL:
            self.__change_surface(c.BALL_RADIUS, c.WHITE)
        elif effect is Powers.GRAVITY:
            self.__gravity_effected = False

    def add_power(self, new_power: Power_Up) -> None:
        """ Public method for adding a power to the ball. """
        powers_arr: list[Powers] = [p.get_effect() for p in self.__powers]
        if new_power.get_effect() not in powers_arr:
            new_power.set_active()
            self.__powers.append(new_power)
            self.__apply_power(new_power)
        else:
            for power in self.__powers:
                if power.get_effect() == new_power.get_effect():
                    power.reset_timer()

    def reverse_all_powers(self) -> None:
        """ Public method used to reverse all applied powers to the ball. """
        for power in self.__powers:
            self.__reverse_effects(power.get_effect())
        self.__powers.clear()

    def update_powers(self) -> None:
        """ Public method used to track whether a power's effect has ended. """
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
        """ Public method handling the movement of the ball."""
        additional_gravity: int = c.GRAVITY_STRENGHT \
            if self.__gravity_effected else 0

        sign: int = 1 if self.__velocity[1] > 0 else -1

        self.rect.x += self.__velocity[0]
        self.rect.y += self.__velocity[1] + sign * additional_gravity

        if self.rect.y <= c.TOP_LINE_Y + self.__radius:
            pygame.mixer.Sound.play(self.__bounce_sound)
            self.rect.y = c.TOP_LINE_Y + self.__radius + 1
            self.reverse_velocity_y()
        elif self.rect.y >= c.SCREEN_SIZE[1] - self.__radius * 2:
            pygame.mixer.Sound.play(self.__bounce_sound)
            self.rect.y = c.SCREEN_SIZE[1] - self.__radius * 2 - 1
            self.reverse_velocity_y()

    def bounce(self, additional_velocity: int, paddle_y: int, paddle_height: int) -> None:
        """ Public method handling the bounce of the ball."""
        pygame.mixer.Sound.play(self.__bounce_sound)
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
        """ Public method to get the last player that touched the ball. """
        return self.__last_hit

    def set_last_hit(self, player: int) -> None:
        """ Public method to set the last player that touched the ball. """
        self.__last_hit = player

    def set_coordinates(self, new_x: int, new_y: int) -> None:
        """ Public method implementing a way to set coordinates to the ball when needed."""
        self.rect.x = new_x
        self.rect.y = new_y

    def get_ball_position(self) -> None:
        """Public method allowing for the ball position to be accessed."""
        return self.rect.x, self.rect.y

    def get_radius(self) -> float:
        """ Public method to get the radius of the ball."""
        return self.__radius

    def reverse_velocity_x(self) -> None:
        """ Public method reversing x velocity of the ball."""
        self.__velocity[0] = -self.__velocity[0]

    def reverse_velocity_y(self) -> None:
        """ Public method reversing y velocity of the ball."""
        self.__velocity[1] = -self.__velocity[1]
