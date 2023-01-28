""" Main menu class controlling all the other menus. """

import pygame
import pygame_menu
from client import Client
import constants as c


class Menu:
    """ Main menu class with declarations for all other menus. """

    def __init__(self):
        self.__screen = pygame.display.set_mode(c.SCREEN_SIZE)
        pygame.display.set_caption("Super Pong")

        # Menu declarations:
        self.__main_menu = pygame_menu.Menu("Super Pong", c.SCREEN_SIZE[0], c.SCREEN_SIZE[1],
                                            theme=c.MENU_THEME)
        self.__start_menu = pygame_menu.Menu("Game settings", c.SCREEN_SIZE[0],
                                             c.SCREEN_SIZE[1], theme=c.MENU_THEME)
        self.__options_menu = pygame_menu.Menu("Options", c.SCREEN_SIZE[0], c.SCREEN_SIZE[1],
                                               theme=c.MENU_THEME)
        self.__game_id_menu = pygame_menu.Menu(
            "Game Id", c.SCREEN_SIZE[0] // 2, c.SCREEN_SIZE[1] // 2, theme=c.MENU_THEME)
        self.__game_joined_menu = pygame_menu.Menu(
            "Game lobby", c.SCREEN_SIZE[0], c.SCREEN_SIZE[1], theme=c.MENU_THEME)

        # Main menu:
        self.__name_input = self.__main_menu.add.text_input(
            "Name: ", default="Guest")
        self.__main_menu.add.button("Host", self.__start_menu)
        self.__main_menu.add.button("Join", self.__game_id_menu)
        self.__main_menu.add.button("Options", self.__options_menu)
        self.__main_menu.add.button("Quit", pygame_menu.events.EXIT)

        # Game Id menu:
        self.__game_id = self.__game_id_menu.add.text_input("Id: ", default="")
        self.__game_id_menu.add.button("Join game", self.__join_game)

        # Game Joined menu:
        # self.__game_id_label = self.__game_joined_menu.add.label(
        #     "")  # self.__game_id.get_value())
        # self.__game_joined_menu.add.button("Ready", self.__player_ready)

        # Host menu:
        self.__player_label = self.__start_menu.add.label(
            "Waiting for player...")
        self.__player_ready_label = self.__start_menu.add.label(
            "")
        # Changing the message displayed -> self.__player_label.set_title("playert")
        self.__start_menu.add.button("Start game", self.__start_game)

        # Options menu
        # Options idea -> Music volume and sounds volume,

        self.__main_menu.mainloop(self.__screen)

    def __player_ready(self):
        return Client(self.__screen, self.__name_input.get_value())

    def __join_game(self):
        # self.__game_id_label.set_title(self.__game_id.get_value())
        self.__main_menu._open(self.__game_joined_menu)

    def __start_game(self):
        return Client(self.__screen, self.__name_input.get_value())
