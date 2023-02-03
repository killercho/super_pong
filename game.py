""" Game class which operates the game. """

import sys
from random import randrange
from time import sleep
import pygame
import constants as c
from paddle import Paddle
from ball import Ball
from power_up import Power_Up

pygame.init()


class Game:
    """ Game class which starts and operates the game. """

    def __init__(self, screen, name_1_data, name_2_data):
        self.__screen = screen
        self.__name_1: str = name_1_data
        self.__name_2: str = name_2_data

        self.__score_1: int = 0
        self.__score_2: int = 0
        self.__target_score: int = 50
        self.__score_break: int = 0

        self.__spawned_powers = []
        self.__spawned_powers_count = 0

        self.__paddle_speeds = [c.PADDLE_SPEED, c.PADDLE_SPEED]
        self.__paddle_powers = [[[]], [[]]]
        self.__ball_powers = [[]]

        self.__paddle_1: Paddle = Paddle(
            c.WHITE, c.PADDLE_WIDTH, c.PADDLE_LENGTH)
        self.__paddle_1.set_coordinates(c.PADDLE_1_X, c.PADDLE_1_Y)

        self.__paddle_2: Paddle = Paddle(
            c.WHITE, c.PADDLE_WIDTH, c.PADDLE_LENGTH)
        self.__paddle_2.set_coordinates(c.PADDLE_2_X, c.PADDLE_2_Y)

        self.__ball: Ball = Ball(c.WHITE, c.BALL_RADIUS)
        self.__ball.set_coordinates(c.BALL_X, c.BALL_Y)

        self.__all_sprites_list = pygame.sprite.Group()
        self.__all_sprites_list.add(self.__paddle_1)
        self.__all_sprites_list.add(self.__paddle_2)
        self.__all_sprites_list.add(self.__ball)

        self.__INGAME_TEXT_FONT = pygame.font.Font(None, 100)

        self.__clock = pygame.time.Clock()
        self.__start_game()

    def __spawn_random_power(self):
        new_power_x = randrange(
            c.POWER_OFFSET, c.SCREEN_SIZE[0] - c.POWER_OFFSET)
        new_power_y = randrange(
            c.TOP_LINE_Y + c.POWER_OFFSET, c.SCREEN_SIZE[1] - c.POWER_OFFSET)
        new_power: Power_Up = Power_Up(
            c.POWER_UP_SIDE, new_power_x, new_power_y)
        self.__spawned_powers.append([new_power, c.ACTIVE_POWER_CD])
        self.__spawned_powers_count += 1
        self.__all_sprites_list.add(new_power)

    def __create_new_paddle(self, paddle: Paddle, new_length: int) -> Paddle:
        old_x, old_y = paddle.get_coordinates()
        paddle.kill()
        paddle = Paddle(
            c.WHITE, c.PADDLE_WIDTH, new_length)
        paddle.set_coordinates(old_x, old_y)
        self.__all_sprites_list.add(paddle)
        return paddle

    def __clean_spawned_powers(self):
        if self.__spawned_powers_count > 0:
            for power_arr in self.__spawned_powers:
                if power_arr[1] > 0:
                    power_arr[1] -= 1
                else:
                    power_arr[0].kill()

    def __clean_all_spanwed_powers(self):
        for power_arr in self.__spawned_powers:
            power_arr[0].kill()

    def __reverse_power(self, power: str, player: int):
        if player != -1:
            if power == "up_speed_player":
                self.__paddle_speeds[player] = c.PADDLE_SPEED
            elif power == "down_speed_player":
                self.__paddle_speeds[player] = c.PADDLE_SPEED
            elif power == "increase_own_paddle":
                if player == 1:
                    self.__paddle_1 = self.__create_new_paddle(
                        self.__paddle_1, c.PADDLE_LENGTH)
                else:
                    self.__paddle_2 = self.__create_new_paddle(
                        self.__paddle_2, c.PADDLE_LENGTH)
            elif power == "decrease_opponent_paddle":
                if player == 1:
                    self.__paddle_1 = self.__create_new_paddle(
                        self.__paddle_1, c.PADDLE_LENGTH)
                else:
                    self.__paddle_2 = self.__create_new_paddle(
                        self.__paddle_2, c.PADDLE_LENGTH)

    def __reverse_all_powers(self):
        for power_arr in self.__paddle_powers[0]:
            if(len(power_arr) == 0):
                continue
            self.__paddle_powers[0].remove(power_arr)
            self.__reverse_power(power_arr[0], 0)
        for power_arr in self.__paddle_powers[1]:
            if(len(power_arr) == 0):
                continue
            self.__paddle_powers[1].remove(power_arr)
            self.__reverse_power(power_arr[0], 1)
        for power_arr in self.__ball_powers:
            pass

    def __tick_active_powers(self):
        for power_arr in self.__paddle_powers[0]:
            if(len(power_arr) == 0):
                continue
            if power_arr[1] <= 0:
                self.__paddle_powers[0].remove(power_arr)
                self.__reverse_power(power_arr[0], 0)
                continue
            power_arr[1] -= 1
        for power_arr in self.__paddle_powers[1]:
            if(len(power_arr) == 0):
                continue
            if power_arr[1] <= 0:
                self.__paddle_powers[1].remove(power_arr)
                self.__reverse_power(power_arr[0], 1)
                continue
            power_arr[1] -= 1
        for power_arr in self.__ball_powers:
            pass

    def __apply_power_effect(self, power: str, player: int):
        if player != -1:
            all_powers = []
            if len(self.__paddle_powers[player - 1]) != 1:
                all_powers = [arr[0] if len(arr) > 0 else ""
                              for arr in self.__paddle_powers[player - 1]]
            if power not in all_powers:
                if power == "up_speed_player":
                    self.__paddle_speeds[player - 1] *= c.SPEED_INCREASE
                    self.__paddle_powers[player -
                                         1].append([power, c.SPEED_TIMER])
                elif power == "down_speed_player":
                    self.__paddle_speeds[player - 1] *= c.SPEED_DECREASE
                    self.__paddle_powers[player -
                                         1].append([power, c.SPEED_TIMER])
                elif power == "increase_own_paddle":
                    if player == 1:
                        self.__paddle_1 = self.__create_new_paddle(
                            self.__paddle_1, c.INCREASED_LENGHT)
                        self.__paddle_powers[0].append(
                            [power, c.PADDLE_SIZE_TIMER])
                    else:
                        self.__paddle_2 = self.__create_new_paddle(
                            self.__paddle_2, c.INCREASED_LENGHT)
                        self.__paddle_powers[1].append(
                            [power, c.PADDLE_SIZE_TIMER])
                elif power == "decrease_opponent_paddle":
                    if player == 1:
                        self.__paddle_2 = self.__create_new_paddle(
                            self.__paddle_2, c.DECREASED_LENGHT)
                        self.__paddle_powers[1].append(
                            [power, c.PADDLE_SIZE_TIMER])
                    else:
                        self.__paddle_1 = self.__create_new_paddle(
                            self.__paddle_1, c.DECREASED_LENGHT)
                        self.__paddle_powers[0].append(
                            [power, c.PADDLE_SIZE_TIMER])
                self.__spawned_powers_count -= 1

    def __apply_score_break(self):
        self.__clean_all_spanwed_powers()
        self.__reverse_all_powers()
        self.__paddle_1.set_coordinates(c.PADDLE_1_X, c.PADDLE_1_Y)
        self.__paddle_2.set_coordinates(c.PADDLE_2_X, c.PADDLE_2_Y)
        self.__ball.reset_ball()

    def __handle_ball_movement(self):
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

    def __handle_collision(self):
        hit_paddle_1 = pygame.sprite.collide_mask(
            self.__ball, self.__paddle_1)
        hit_paddle_2 = pygame.sprite.collide_mask(
            self.__ball, self.__paddle_2)
        if hit_paddle_1:
            self.__ball.bounce()
            self.__ball.set_last_hit(1)
        if hit_paddle_2:
            self.__ball.bounce()
            self.__ball.set_last_hit(2)

        for power in [arr[0] for arr in self.__spawned_powers]:
            mask = pygame.sprite.collide_mask(self.__ball, power)
            if mask:
                self.__apply_power_effect(
                    power.get_effect(), self.__ball.get_last_hit())
                power.kill()

    def __handle_input(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            self.__paddle_1.move_up(self.__paddle_speeds[0])
        if pressed_keys[pygame.K_s]:
            self.__paddle_1.move_down(self.__paddle_speeds[0])
        if pressed_keys[pygame.K_UP]:
            self.__paddle_2.move_up(self.__paddle_speeds[1])
        if pressed_keys[pygame.K_DOWN]:
            self.__paddle_2.move_down(self.__paddle_speeds[1])

    def __create_middle_line(self):
        for i in range(0, c.SCREEN_SIZE[1], c.MIDDLE_LINES_STEP):
            vertical_line_size = (c.LINES_WIDTH, 64)
            vertical_line = pygame.Surface(
                vertical_line_size, pygame.SRCALPHA)
            vertical_line.fill((255, 255, 255, 70))
            self.__screen.blit(vertical_line, (636, i))

        pygame.draw.line(self.__screen, c.WHITE, [0, c.TOP_LINE_Y],
                         [c.SCREEN_SIZE[0], c.TOP_LINE_Y], c.LINES_WIDTH)
        pygame.draw.line(self.__screen, c.WHITE, [639, 0], [639, 100],
                         c.LINES_WIDTH)

    def __render_top_info(self):
        text = self.__INGAME_TEXT_FONT.render(
            str(self.__score_1), 1, c.WHITE)
        self.__screen.blit(text, (532, 20))
        text = self.__INGAME_TEXT_FONT.render(
            str(self.__score_2), 1, c.WHITE)
        self.__screen.blit(text, (722, 20))

        text = self.__INGAME_TEXT_FONT.render(self.__name_1, 1, c.WHITE)
        self.__screen.blit(text, (100, 20))
        text = self.__INGAME_TEXT_FONT.render(self.__name_2, 1, c.WHITE)
        self.__screen.blit(text, (854, 20))

    def __start_game(self):
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

            pygame.display.flip()

            if self.__score_1 >= self.__target_score or self.__score_2 >= self.__target_score:
                game_running = False

            self.__clock.tick(60)

        pygame.quit()
        sys.exit()
