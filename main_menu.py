""" Main menu class controlling all the other menus. """

from game import Game
import pygame
import pygame_menu
import constants as c


class Menu:
    """ Main menu class with declarations for all other menus. """

    def __init__(self):
        self.__screen = pygame.display.set_mode(c.SCREEN_SIZE)
        pygame.display.set_caption("Super Pong")

        self.__main_menu = pygame_menu.Menu("Super Pong", c.SCREEN_SIZE[0], c.SCREEN_SIZE[1],
                                            theme=c.MENU_THEME)
        self.__main_menu.add.button("Play", self.__game_settings_menu)
        self.__main_menu.add.button("Options", self.__options_menu_func)
        self.__main_menu.add.button("Quit", pygame_menu.events.EXIT)

        # Start menu
        self.__start_menu = pygame_menu.Menu("Game settings", c.SCREEN_SIZE[0],
                                             c.SCREEN_SIZE[1], theme=c.MENU_THEME)

        self.__name_1_input_field = self.__start_menu.add.text_input(
            "Player 1 name: ", default="")
        self.__name_2_input_field = self.__start_menu.add.text_input(
            "Player 2 name: ", default="")

        self.__start_menu.add.button("Start game", self.__start_game)

        # Options menu
        self.__options_menu = pygame_menu.Menu("Options", c.SCREEN_SIZE[0], c.SCREEN_SIZE[1],
                                               theme=c.MENU_THEME)
        # Options idea -> Music volume and sounds volume,
        #       selector for what power-ups are in the game

        self.__main_menu.mainloop(self.__screen)

    def __game_settings_menu(self):
        self.__main_menu._open(self.__start_menu)

    def __options_menu_func(self):
        self.__main_menu._open(self.__options_menu)

    def __start_game(self):
        name_1_data: str = self.__name_1_input_field.get_value()[:c.MAX_NAME_SYMBOLS]
        name_2_data: str = self.__name_2_input_field.get_value()[:c.MAX_NAME_SYMBOLS]

        name_1: str = c.DEFAULT_NAME_1 if name_1_data == "" else name_1_data
        name_2: str = c.DEFAULT_NAME_2 if name_2_data == "" else name_2_data

        return Game(self.__screen, name_1, name_2)
