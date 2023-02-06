""" Power up file holding the main logic of a power up."""

import os
import pygame
from random import randrange
import constants as c


class Power_Up(pygame.sprite.Sprite):
    """Power up class holding the main logic needef for a power up."""

    def __init__(self, spawn_x: int, spawn_y: int) -> None:
        super().__init__()

        self.__power: str = self.__get_random_power()

        self.__despawn_timer: float = c.ACTIVE_POWER_CD
        self.__active_timer: float = self.__get_active_timer()
        self.__active: bool = False

        self.image: pygame.Surface = pygame.image.load(
            os.path.join("assets", f"{self.__power}.png"))

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = spawn_x
        self.rect.y = spawn_y

    def __get_active_timer(self) -> float:
        if self.__power == "up_speed_player" \
                or self.__power == "down_speed_player":
            return c.SPEED_TIMER
        elif self.__power == "increase_own_paddle" \
                or self.__power == "decrease_opponent_paddle":
            return c.PADDLE_SIZE_TIMER
        elif self.__power == "smaller_ball" \
                or self.__power == "bigger_ball":
            return c.BALL_SIZE_TIMER
        return 0.0

    def __get_random_power(self) -> str:
        rand_index = randrange(0, len(c.AVALIABLE_POWERS))
        return c.AVALIABLE_POWERS[rand_index]

    def get_effect(self) -> str:
        return self.__power

    def set_active(self) -> None:
        self.__active = True

    def set_timer(self, new_timer: float) -> None:
        self.__active_timer = new_timer

    def get_timer(self) -> float:
        return self.__active_timer

    def is_ball_power(self) -> bool:
        if self.__power in ["smaller_ball", "bigger_ball"]:
            return True
        return False

    def delete_power(self) -> None:
        self.kill()

    def update_validity(self) -> str:
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
        return ""
