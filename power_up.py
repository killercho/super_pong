""" Power up file holding the main logic of a power up."""

import os
import pygame
from random import randrange
import constants as c


class Power_Up(pygame.sprite.Sprite):
    """Power up class holding the main logic needef for a power up."""

    def __init__(self, spawn_x: int, spawn_y: int) -> None:
        super().__init__()

        self.__power = self.__get_random_power()

        self.__despawn_timer = c.ACTIVE_POWER_CD
        self.__active_timer = self.__get_active_timer()
        self.__active = False

        self.image = pygame.image.load(
            os.path.join("assets", f"{self.__power}.png"))

        self.rect = self.image.get_rect()
        self.rect.x = spawn_x
        self.rect.y = spawn_y

    def delete_power(self):
        self.kill()

    def set_active(self):
        self.__active = True

    def get_timer(self):
        return self.__active_timer

    def update_validity(self):
        if not self.__active:
            if self.__despawn_timer > 0:
                self.__despawn_timer -= 1
            else:
                self.kill()
        else:
            if self.__active_timer > 0:
                self.__active_timer -= 1
            else:
                self.kill()

    def __get_active_timer(self):
        if self.__power == "up_speed_player" \
                or self.__power == "down_speed_player":
            return c.SPEED_TIMER
        elif self.__power == "increase_own_paddle" \
                or self.__power == "decrease_opponent_paddle":
            return c.PADDLE_SIZE_TIMER

    def __get_random_power(self):
        rand_index = randrange(0, len(c.AVALIABLE_POWERS))
        return c.AVALIABLE_POWERS[rand_index]

    def get_effect(self):
        return self.__power
