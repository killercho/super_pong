""" Game class which operates the game. """

import sys
from random import randrange
import pygame
import constants as c
from paddle import Paddle
from ball import Ball
from power_up import Power_Up

pygame.init()


class Game:
    """ Game class which starts and operates the game. """

    def __init__(self, screen: pygame.Surface, name_1_data: str, name_2_data: str) -> None:
        self.__screen: pygame.Surface = screen
        self.__name_1: str = name_1_data
        self.__name_2: str = name_2_data

        self.__score_1: int = 0
        self.__score_2: int = 0
        self.__target_score: int = 50
        self.__score_break: float = c.GAME_BREAK_AFTER_POINT

        self.__spawned_powers: list = []
        self.__spawned_powers_count: int = 0

        self.__paddles: list = [Paddle(c.WHITE, c.PADDLE_WIDTH, c.PADDLE_LENGTH),
                                Paddle(c.WHITE, c.PADDLE_WIDTH, c.PADDLE_LENGTH)]
        self.__paddles[0].set_coordinates(c.PADDLE_1_X, c.PADDLE_1_Y)
        self.__paddles[1].set_coordinates(c.PADDLE_2_X, c.PADDLE_2_Y)

        self.__ball: Ball = Ball(c.WHITE, c.BALL_RADIUS)
        self.__ball.set_coordinates(c.BALL_X, c.BALL_Y)

        self.__all_sprites_list: pygame.sprite.Group = pygame.sprite.Group()
        self.__all_sprites_list.add(self.__paddles[0])
        self.__all_sprites_list.add(self.__paddles[1])
        self.__all_sprites_list.add(self.__ball)

        self.__INGAME_TEXT_FONT: pygame.font.Font = pygame.font.Font(None, 100)

        self.__clock: pygame.time.Clock = pygame.time.Clock()
        self.__start_game()

    def __spawn_random_power(self) -> None:
        new_power_x: int = randrange(
            c.POWER_OFFSET, c.SCREEN_SIZE[0] - c.POWER_OFFSET)
        new_power_y = randrange(
            c.TOP_LINE_Y + c.POWER_OFFSET, c.SCREEN_SIZE[1] - c.POWER_OFFSET)
        new_power: Power_Up = Power_Up(new_power_x, new_power_y)
        self.__spawned_powers.append(new_power)
        self.__spawned_powers_count += 1
        self.__all_sprites_list.add(new_power)

    def __clean_spawned_powers(self) -> None:
        for power in self.__spawned_powers:
            power.update_validity()

    def __clean_all_spanwed_powers(self) -> None:
        for power in self.__spawned_powers:
            power.delete_power()
        self.__spawned_powers_count = 0

    def __reverse_all_powers(self) -> None:
        for paddle in self.__paddles:
            paddle.reverse_all_powers()

    def __tick_active_powers(self) -> None:
        for paddle in self.__paddles:
            paddle.update_powers()

    def __apply_power_effect(self, power: Power_Up, player: int) -> None:
        if player != -1:
            power.set_active()
            self.__paddles[player].add_power(power)
            self.__spawned_powers_count -= 1

    def __apply_score_break(self) -> None:
        self.__clean_all_spanwed_powers()
        self.__reverse_all_powers()
        self.__paddles[0].set_coordinates(c.PADDLE_1_X, c.PADDLE_1_Y)
        self.__paddles[1].set_coordinates(c.PADDLE_2_X, c.PADDLE_2_Y)
        self.__ball.reset_ball()

    def __handle_ball_movement(self) -> None:
        if self.__ball.get_ball_position()[0] >= c.SCREEN_SIZE[0] - c.BALL_RADIUS * 2:
            self.__score_1 += 1
            self.__score_break = c.GAME_BREAK_AFTER_POINT
            self.__apply_score_break()
        elif self.__ball.get_ball_position()[0] <= 0:
            self.__score_2 += 1
            self.__score_break = c.GAME_BREAK_AFTER_POINT
            self.__apply_score_break()
        if self.__ball.get_ball_position()[1] < c.TOP_LINE_Y + 5:
            self.__ball.reverse_velocity_y()
        elif self.__ball.get_ball_position()[1] >= c.SCREEN_SIZE[1] - c.BALL_RADIUS * 2:
            self.__ball.reverse_velocity_y()

    def __handle_collision(self) -> None:
        hit_paddle_1 = pygame.sprite.collide_mask(
            self.__ball, self.__paddles[0])
        hit_paddle_2 = pygame.sprite.collide_mask(
            self.__ball, self.__paddles[1])
        if hit_paddle_1:
            self.__ball.bounce(self.__paddles[0].get_velocity())
            self.__ball.set_last_hit(0)
        if hit_paddle_2:
            self.__ball.bounce(self.__paddles[1].get_velocity())
            self.__ball.set_last_hit(1)

        for power in self.__spawned_powers:
            mask: tuple = pygame.sprite.collide_mask(self.__ball, power)
            if mask:
                self.__apply_power_effect(
                    power, self.__ball.get_last_hit())
                power.delete_power()

    def __handle_input(self) -> None:
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            self.__paddles[0].move_up()
        elif pressed_keys[pygame.K_s]:
            self.__paddles[0].move_down()
        if pressed_keys[pygame.K_UP]:
            self.__paddles[1].move_up()
        elif pressed_keys[pygame.K_DOWN]:
            self.__paddles[1].move_down()

    def __create_middle_line(self) -> None:
        for i in range(0, c.SCREEN_SIZE[1], c.MIDDLE_LINES_STEP):
            vertical_line_size: tuple = (c.LINES_WIDTH, 64)
            vertical_line: pygame.Surface = pygame.Surface(
                vertical_line_size, pygame.SRCALPHA)
            vertical_line.fill((255, 255, 255, 70))
            self.__screen.blit(vertical_line, (636, i))

        pygame.draw.line(self.__screen, c.WHITE, [0, c.TOP_LINE_Y],
                         [c.SCREEN_SIZE[0], c.TOP_LINE_Y], c.LINES_WIDTH)
        pygame.draw.line(self.__screen, c.WHITE, [639, 0], [639, 100],
                         c.LINES_WIDTH)

    def __render_break_timer(self, timer: int) -> None:
        font: pygame.font.Font = pygame.font.Font(None, 200)
        text: pygame.Surface = font.render(str(timer), 1, c.WHITE)
        self.__screen.blit(
            text, (c.SCREEN_SIZE[0] / 2 - 35, c.SCREEN_SIZE[1] / 2 - 35))

    def __render_top_info(self) -> None:
        text: pygame.Surface = self.__INGAME_TEXT_FONT.render(
            str(self.__score_1), 1, c.WHITE)
        self.__screen.blit(text, (532, 20))
        text: pygame.Surface = self.__INGAME_TEXT_FONT.render(
            str(self.__score_2), 1, c.WHITE)
        self.__screen.blit(text, (722, 20))

        text: pygame.Surface = self.__INGAME_TEXT_FONT.render(
            self.__name_1, 1, c.WHITE)
        self.__screen.blit(text, (100, 20))
        text: pygame.Surface = self.__INGAME_TEXT_FONT.render(
            self.__name_2, 1, c.WHITE)
        self.__screen.blit(text, (854, 20))

    def __start_game(self) -> None:
        power_cd: int = c.POWER_UP_CD
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        game_running: bool = True
        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_running = False
                elif event.type == pygame.USEREVENT:
                    if self.__score_break > 0:
                        self.__apply_score_break()
                        self.__score_break -= 1
                    else:
                        self.__tick_active_powers()
                        self.__clean_spawned_powers()
                        if power_cd > 0:
                            power_cd -= 1
                        else:
                            self.__spawn_random_power()
                            power_cd = c.POWER_UP_CD - 1

            if self.__score_break <= 0:
                self.__handle_input()
                self.__handle_ball_movement()
                self.__handle_collision()
                self.__all_sprites_list.update()

            self.__screen.fill(c.BLACK)
            self.__all_sprites_list.draw(self.__screen)

            # creating punctured line
            self.__create_middle_line()
            self.__render_top_info()
            if self.__score_break > 0:
                self.__render_break_timer(self.__score_break)

            pygame.display.flip()

            if self.__score_1 >= self.__target_score or self.__score_2 >= self.__target_score:
                game_running = False

            self.__clock.tick(60)

        pygame.quit()
        sys.exit()
