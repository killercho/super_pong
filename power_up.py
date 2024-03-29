""" Power up file holding the main logic of a power up and an enum with all the powers avaliable."""

import os
from enum import Enum
import pygame
from random import randrange, choice
import constants as c


class Powers(Enum):
    """ Enum used to represend all the avaliable powers."""
    NULL_POWER = 0
    UP_SPEED_PLAYER = 1
    DOWN_SPEED_PLAYER = 2
    INCREASE_OWN_PADDLE = 3
    DECREASE_OPPONENT_PADDLE = 4
    SMALLER_BALL = 5
    BIGGER_BALL = 6
    REVERSED_CONTROLS = 7
    INVISIBLE_BALL = 8
    GRAVITY = 9


class Power_Up(pygame.sprite.Sprite):
    """ Power up class holding the main logic needed for a power up."""

    def __init__(self, spawn_x: int, spawn_y: int) -> None:
        super().__init__()

        self.__power: Powers = self.__get_random_power()
        self.__is_hidden: bool = self.__determine_hidden()
        self.__effects_opponent: bool = self.__get_effect_target()

        self.__despawn_timer: float = c.ACTIVE_POWER_CD
        self.__active_timer: float = self.__get_active_timer()
        self.__active: bool = False

        self.image: pygame.Surface = self.__get_icon()

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = spawn_x
        self.rect.y = spawn_y

    def __get_icon(self) -> pygame.Surface:
        """ Method to get the image needed for the specific power."""
        if self.__is_hidden:
            return pygame.image.load(
                os.path.join(c.ASSETS_FOLDER, "random_power.png"))
        if self.__power is Powers.UP_SPEED_PLAYER:
            return pygame.image.load(
                os.path.join(c.ASSETS_FOLDER, "up_speed_player.png"))
        if self.__power is Powers.DOWN_SPEED_PLAYER:
            return pygame.image.load(
                os.path.join(c.ASSETS_FOLDER, "down_speed_player.png"))
        if self.__power is Powers.INCREASE_OWN_PADDLE:
            return pygame.image.load(
                os.path.join(c.ASSETS_FOLDER, "increase_own_paddle.png"))
        if self.__power is Powers.DECREASE_OPPONENT_PADDLE:
            return pygame.image.load(
                os.path.join(c.ASSETS_FOLDER, "decrease_opponent_paddle.png"))
        if self.__power is Powers.SMALLER_BALL:
            return pygame.image.load(
                os.path.join(c.ASSETS_FOLDER, "smaller_ball.png"))
        if self.__power is Powers.BIGGER_BALL:
            return pygame.image.load(
                os.path.join(c.ASSETS_FOLDER, "bigger_ball.png"))
        if self.__power is Powers.REVERSED_CONTROLS:
            return pygame.image.load(
                os.path.join(c.ASSETS_FOLDER, "reversed_controls.png"))
        if self.__power is Powers.INVISIBLE_BALL:
            return pygame.image.load(
                os.path.join(c.ASSETS_FOLDER, "invisible_ball.png"))
        if self.__power is Powers.GRAVITY:
            return pygame.image.load(
                os.path.join(c.ASSETS_FOLDER, "gravity.png"))

    def __get_active_timer(self) -> float:
        """ Method to get the specific power's cooldown."""
        if self.__power is Powers.UP_SPEED_PLAYER \
                or self.__power is Powers.DOWN_SPEED_PLAYER:
            return c.SPEED_TIMER
        elif self.__power is Powers.INCREASE_OWN_PADDLE \
                or self.__power is Powers.DECREASE_OPPONENT_PADDLE:
            return c.PADDLE_SIZE_TIMER
        elif self.__power is Powers.SMALLER_BALL \
                or self.__power is Powers.BIGGER_BALL:
            return c.BALL_SIZE_TIMER
        elif self.__power is Powers.REVERSED_CONTROLS:
            return c.REVERSED_CONTROLS_TIMER
        elif self.__power is Powers.INVISIBLE_BALL:
            return c.BALL_INVISIBILITY_TIMER
        elif self.__power is Powers.GRAVITY:
            return c.GRAVITY_TIMER
        return 0.0

    def __get_effect_target(self) -> bool:
        """ Method to get the effect's target.
            If the effect is 'False' then the target is the current player.
            If the effect is 'True' then the target is the opponent 
            or the ball."""
        if self.__power in [Powers.UP_SPEED_PLAYER,
                            Powers.DOWN_SPEED_PLAYER,
                            Powers.INCREASE_OWN_PADDLE]:
            return False
        return True

    def __get_random_power(self) -> Powers:
        """ Method getting a random power from the enum with powers."""
        power: Powers = choice(list(Powers))
        while (power is Powers.NULL_POWER):
            power = choice(list(Powers))
        return power

    def __determine_hidden(self) -> bool:
        """ Method determining if the power will be hidden or not."""
        number: int = randrange(1, len(Powers))
        return number == 1

    def get_effect(self) -> str:
        """ Public method to get the effect of the power."""
        return self.__power

    def set_active(self) -> None:
        """ Public method to activate the power cooldown after activation."""
        self.__active = True

    def reset_timer(self) -> None:
        """ Public method to reset the timer back to it's original value."""
        self.__active_timer = self.__get_active_timer()

    def effects_opponent(self) -> bool:
        """ Public method to understand if the power effects 
            the opponent or not."""
        return self.__effects_opponent

    def get_timer(self) -> float:
        """ Public method to get the timer for the power."""
        return self.__active_timer

    def get_image(self) -> pygame.Surface:
        """ Public method to get the image of the power."""
        return self.image

    def is_ball_power(self) -> bool:
        """ Public method to understand if the power effects the ball."""
        if self.__power in [Powers.SMALLER_BALL,
                            Powers.BIGGER_BALL,
                            Powers.INVISIBLE_BALL,
                            Powers.GRAVITY]:
            return True
        return False

    def delete_power(self) -> None:
        """ Public method to kill the ball."""
        self.kill()

    def update_validity(self) -> Powers:
        """ Public method to check the validity of the ball.
            If the timer has expired destroy it 
                and return the destroyed power's effect.
            Else just lower the timer with one and return the NULL_POWER."""
        if not self.__active:
            if self.__despawn_timer > 0:
                self.__despawn_timer -= 1
            else:
                self.kill()
                return self.__power
        else:
            if self.__active_timer > 0:
                self.__active_timer -= 1
            else:
                self.kill()
                return self.__power
        return Powers.NULL_POWER
