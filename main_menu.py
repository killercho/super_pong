""" Main menu class controlling all the other menus. """

import pygame
import pygame_menu
from game import Game
import constants as c


class Menu:
    """ Main menu class with declarations for all other menus. """

    def __init__(self) -> None:
        self.__screen: pygame.Surface = pygame.display.set_mode(c.SCREEN_SIZE)
        pygame.display.set_caption("Super Pong")

        # Menu declarations:
        self.__main_menu: pygame_menu.Menu = pygame_menu.Menu("Super Pong", c.SCREEN_SIZE[0], c.SCREEN_SIZE[1],
                                                              theme=c.MENU_THEME)
        self.__start_menu: pygame_menu.Menu = pygame_menu.Menu("Game Lobby", c.SCREEN_SIZE[0],
                                                               c.SCREEN_SIZE[1], theme=c.MENU_THEME)
        self.__options_menu: pygame_menu.Menu = pygame_menu.Menu("Options", c.SCREEN_SIZE[0], c.SCREEN_SIZE[1],
                                                                 theme=c.MENU_THEME)
        # Main menu:
        self.__main_menu.add.button("Game Lobby", self.__start_menu)
        self.__main_menu.add.button("Options", self.__options_menu)
        self.__main_menu.add.button("Quit", pygame_menu.events.EXIT)

        # Game menu:
        self.__name_1_input = self.__start_menu.add.text_input(
            "Name 1: ", default=c.DEFAULT_NAME_1)
        self.__name_2_input = self.__start_menu.add.text_input(
            "Name 2: ", default=c.DEFAULT_NAME_2)
        self.__target_score_input = self.__start_menu.add.text_input(
            "Target: ", default="10")
        self.__start_menu.add.button("Start game", self.__start_game)

        # Options menu
        self.__read_file()
        self.__sound_volume_slider = self.__options_menu.add.range_slider(
            "Change sound volume", self.__volume_sound, (0, 100), 1,
            rangeslider_id="sound_volume", value_format=lambda x: str(int(x)))
        self.__music_volume_slider = self.__options_menu.add.range_slider(
            "Change sound volume", self.__volume_music, (0, 100), 1,
            rangeslider_id="music_volume", value_format=lambda x: str(int(x)))
        self.__options_menu.add.button("Save and Apply", self.__save_file)

        self.__main_menu.mainloop(self.__screen)

    def __save_file(self) -> None:
        """ Method saving the settings into a file. """
        self.__volume_music = int(self.__music_volume_slider.get_value())
        self.__volume_sound = int(self.__sound_volume_slider.get_value())
        with open(c.SETTINGS_FILE, "w") as file:
            file.write(
                f"{str(self.__volume_music)} {str(self.__volume_sound)}")

    def __read_file(self) -> None:
        """ Method returning the volume numbers for sound and music."""
        self.__volume_music: int = c.DEFAULT_VOLUME
        self.__volume_sound: int = c.DEFAULT_VOLUME
        try:
            with open(c.SETTINGS_FILE, "r") as file:
                volumes = file.readline().split(" ")
                self.__volume_music = int(volumes[0])
                self.__volume_sound = int(volumes[1])
        except:
            pass

    def __start_game(self) -> Game:
        """ Method starting the game loop."""
        try:
            target_score = int(self.__target_score_input.get_value())
        except ValueError:
            target_score = c.DEFAULT_TARGET

        return Game(self.__screen,
                    self.__name_1_input.get_value()[:c.MAX_NAME_SYMBOLS],
                    self.__name_2_input.get_value()[:c.MAX_NAME_SYMBOLS],
                    target_score,
                    self.__volume_sound,
                    self.__volume_music)
