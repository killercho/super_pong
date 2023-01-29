""" Constants file that holds all the constants needed for the game """

import pygame_menu

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

SCREEN_SIZE = (1280, 720)

LINES_WIDTH: int = 8
MIDDLE_LINES_COUNT: int = 10
MIDDLE_LINES_STEP: int = int(SCREEN_SIZE[1] / MIDDLE_LINES_COUNT)

PADDLE_LENGTH: int = 100
PADDLE_WIDTH: int = 10



TOP_LINE_Y: int = 100
BOTTOM_LINE_Y: int = SCREEN_SIZE[1] - PADDLE_LENGTH

PADDLES_OFFSET_X: int = 30
A_PADDLE_X: int = PADDLES_OFFSET_X
A_PADDLE_Y: int = (SCREEN_SIZE[1] - PADDLE_LENGTH) / 2

B_PADDLE_X: int = SCREEN_SIZE[0] - PADDLES_OFFSET_X
B_PADDLE_Y: int = (SCREEN_SIZE[1] - PADDLE_LENGTH) / 2

PADDLE_SPEED: int = 6

BALL_RADIUS = 10

MENU_THEME = pygame_menu.themes.THEME_DARK

DEFAULT_NAME_1: str = "Player 1"
DEFAULT_NAME_2: str = "Player 2"
MAX_NAME_SYMBOLS: int = 10

# Power ups and their constants
POWER_UP_SIDE: int = 20
POWER_UP_CD: int = 5
POWER_OFFSET: int = 100
AVALIABLE_POWERS = ["up_speed_player", "down_speed_player"]
SPEED_INCREASE: int = 1.5
SPEED_DECREASE: int = 0.5