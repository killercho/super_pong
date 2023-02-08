""" Constants file that holds all the constants needed for the game """

import pygame_menu
from math import pi

BLACK: tuple = (0, 0, 0)
RED: tuple = (255, 0, 0)
GREEN: tuple = (0, 255, 0)
BLUE: tuple = (0, 0, 255)
WHITE: tuple = (255, 255, 255)

SCREEN_SIZE: tuple = (1280, 720)

ASSETS_FOLDER = "assets"

GAME_BREAK_AFTER_POINT: float = 3

LINES_WIDTH: int = 8
MIDDLE_LINES_COUNT: int = 10
MIDDLE_LINES_STEP: int = int(SCREEN_SIZE[1] / MIDDLE_LINES_COUNT)

PADDLE_LENGTH: int = 100
PADDLE_WIDTH: int = 10

TOP_LINE_Y: int = 100
BOTTOM_LINE_Y: int = SCREEN_SIZE[1] - PADDLE_LENGTH

BALL_RADIUS: int = 10
BALL_X: int = SCREEN_SIZE[0] / 2 - BALL_RADIUS
BALL_Y: int = (SCREEN_SIZE[1] + TOP_LINE_Y / 2) / 2
BALL_MIN_VEL: int = 3
BALL_MAX_VEL: int = 8
BALL_MAX_BOUNCE: int = 5*pi/12

PADDLES_OFFSET_X: int = 30
PADDLE_1_X: int = PADDLES_OFFSET_X
PADDLE_1_Y: int = (SCREEN_SIZE[1] - PADDLE_LENGTH) / 2

PADDLE_2_X: int = SCREEN_SIZE[0] - PADDLES_OFFSET_X
PADDLE_2_Y: int = (SCREEN_SIZE[1] - PADDLE_LENGTH) / 2

PADDLE_SPEED: int = 6

MENU_THEME = pygame_menu.themes.THEME_DARK

DEFAULT_NAME_1: str = "Player 1"
DEFAULT_NAME_2: str = "Player 2"
MAX_NAME_SYMBOLS: int = 10

# Power ups and their constants
POWER_UP_SIDE: int = 20
POWER_UP_CD: float = 1  # was 3
POWER_OFFSET: int = 100
ACTIVE_POWER_CD: float = 4

SPEED_INCREASE: float = 1.5 * PADDLE_SPEED
SPEED_DECREASE: float = 0.5 * PADDLE_SPEED
SPEED_TIMER: float = 4.5

PADDLE_SIZE_TIMER: float = 3
INCREASED_LENGHT: float = 1.5 * PADDLE_LENGTH
DECREASED_LENGHT: float = 0.5 * PADDLE_LENGTH

BALL_SIZE_TIMER: float = 3
BALL_INCREASED_RADIUS: float = 1.5 * BALL_RADIUS
BALL_DECREASED_RADIUS: float = 0.5 * BALL_RADIUS

BALL_INVISIBILITY_TIMER: float = 1

REVERSED_CONTROLS_TIMER: float = 3

GRAVITY_STRENGHT: int = 5
GRAVITY_TIMER: float = 3
