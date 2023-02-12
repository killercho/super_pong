""" Game class which operates the game. """

import sys
import os
from random import randrange
import pygame
import constants as c
from paddle import Paddle
from ball import Ball
from power_up import Power_Up

pygame.init()


class Game:
    """ Game class which starts and operates the game. """

    def __init__(self,
                 screen: pygame.Surface,
                 name_1_data: str,
                 name_2_data: str,
                 target: int,
                 sound_volume: int,
                 music_volume: int) -> None:
        self.__screen: pygame.Surface = screen
        self.__name_1: str = name_1_data
        self.__name_2: str = name_2_data
        self.__sound_volume: float = sound_volume / 100
        self.__music_volume: float = music_volume / 100

        self.__pickup_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            os.path.join(c.ASSETS_FOLDER, "pickup.wav"))
        self.__pickup_sound.set_volume(self.__sound_volume)

        self.__score_1: int = 0
        self.__score_2: int = 0
        self.__target_score: int = target
        self.__score_break: float = c.GAME_BREAK_AFTER_POINT

        self.__spawned_powers: pygame.sprite.Group = pygame.sprite.Group()
        self.__spawned_powers_count: int = 0

        self.__paddles: list[Paddle] = [Paddle(0, c.WHITE, c.PADDLE_WIDTH, c.PADDLE_LENGTH),
                                        Paddle(1, c.WHITE, c.PADDLE_WIDTH, c.PADDLE_LENGTH)]
        self.__paddles[0].set_coordinates(c.PADDLE_1_X, c.PADDLE_1_Y)
        self.__paddles[1].set_coordinates(c.PADDLE_2_X, c.PADDLE_2_Y)

        self.__ball: Ball = Ball(c.WHITE, c.BALL_RADIUS, self.__sound_volume)
        self.__ball.set_coordinates(c.BALL_X, c.BALL_Y)

        self.__all_sprites_list: pygame.sprite.Group = pygame.sprite.Group()
        self.__all_sprites_list.add(self.__paddles[0])
        self.__all_sprites_list.add(self.__paddles[1])
        self.__all_sprites_list.add(self.__ball)

        self.__INGAME_TEXT_FONT: pygame.font.Font = pygame.font.Font(None, 100)

        self.__clock: pygame.time.Clock = pygame.time.Clock()
        self.__start_game()

    def __spawn_random_power(self) -> None:
        """ Method handling the spawning of powers."""
        new_power_x: int = randrange(
            c.POWER_OFFSET, c.SCREEN_SIZE[0] - c.POWER_OFFSET)
        new_power_y = randrange(
            c.TOP_LINE_Y + c.POWER_OFFSET, c.SCREEN_SIZE[1] - c.POWER_OFFSET)
        new_power: Power_Up = Power_Up(new_power_x, new_power_y)
        self.__spawned_powers.add(new_power)
        self.__spawned_powers_count += 1

    def __clean_spawned_powers(self) -> None:
        """ Method cleaning the spawned powers after a cooldown."""
        for power in self.__spawned_powers:
            power.update_validity()

    def __clean_all_spanwed_powers(self) -> None:
        """ Method forcing all the powers to be deleted."""
        for power in self.__spawned_powers:
            power.delete_power()
        self.__spawned_powers_count = 0
        self.__spawned_powers.empty()

    def __reverse_all_powers(self) -> None:
        """ Method reversing all powers applied to the paddles and the ball."""
        for paddle in self.__paddles:
            paddle.reverse_all_powers()
        self.__ball.reverse_all_powers()

    def __tick_active_powers(self) -> None:
        """ Method used to check the validity of the active powers."""
        for paddle in self.__paddles:
            paddle.update_powers()
        self.__ball.update_powers()

    def __apply_power_effect(self, power: Power_Up, player: int, is_ball_power: bool) -> None:
        """ Method used to apply a power to the correct entity
            depending on the power type."""
        if player != -1 and not is_ball_power:
            effected_player = int(
                not player) if power.effects_opponent() else player
            self.__paddles[effected_player].add_power(power)
            self.__spawned_powers_count -= 1
        elif is_ball_power:
            power.set_active()
            self.__ball.add_power(power)
            self.__spawned_powers_count -= 1

    def __apply_score_break(self) -> None:
        """ Method handling the break after a point is scored."""
        self.__clean_all_spanwed_powers()
        self.__reverse_all_powers()
        self.__paddles[0].set_coordinates(c.PADDLE_1_X, c.PADDLE_1_Y)
        self.__paddles[1].set_coordinates(c.PADDLE_2_X, c.PADDLE_2_Y)
        self.__ball.reset_ball()

    def __handle_ball_movement(self) -> None:
        """ Method handling the ball movement."""
        radius = self.__ball.get_radius()
        if self.__ball.get_ball_position()[0] >= c.SCREEN_SIZE[0] - radius * 2:
            self.__score_1 += 1
            self.__score_break = c.GAME_BREAK_AFTER_POINT
            self.__apply_score_break()
        elif self.__ball.get_ball_position()[0] <= 0:
            self.__score_2 += 1
            self.__score_break = c.GAME_BREAK_AFTER_POINT
            self.__apply_score_break()

    def __handle_collision(self) -> None:
        """ Method handling the collision between the entities."""
        hit_paddle_1 = pygame.sprite.collide_mask(
            self.__ball, self.__paddles[0])
        hit_paddle_2 = pygame.sprite.collide_mask(
            self.__ball, self.__paddles[1])
        if hit_paddle_1:
            self.__ball.bounce(self.__paddles[0].get_velocity(),
                               self.__paddles[0].get_coordinates()[1],
                               self.__paddles[0].get_height())
            self.__ball.set_last_hit(0)
        if hit_paddle_2:
            self.__ball.bounce(self.__paddles[1].get_velocity(),
                               self.__paddles[1].get_coordinates()[1],
                               self.__paddles[1].get_height())
            self.__ball.set_last_hit(1)

        colliding_power: Power_Up | None = pygame.sprite.spritecollideany(
            self.__ball, self.__spawned_powers)
        if colliding_power != None:
            pygame.mixer.Sound.play(self.__pickup_sound)
            self.__apply_power_effect(
                colliding_power, self.__ball.get_last_hit(), colliding_power.is_ball_power())
            colliding_power.delete_power()

    def __handle_input(self) -> None:
        """ Method handling player input."""
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
        """ Method creating and rendering the middle line."""
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
        """ Method rendering the timer during the breaks."""
        font: pygame.font.Font = pygame.font.Font(None, 200)
        text: pygame.Surface = font.render(str(timer), 1, c.WHITE)
        self.__screen.blit(
            text, (c.SCREEN_SIZE[0] / 2 - 35, c.SCREEN_SIZE[1] / 2 - 35))

    def __render_powers_list(self, paddle: Paddle) -> None:
        """ Method rendering the list of all active powers."""
        all_powers: list = paddle.get_powers_images()
        for i in range(0, len(all_powers)):
            location: int = i * c.POWER_UP_SIDE + 350 + 800 * paddle.get_player()
            self.__screen.blit(
                all_powers[i], (location, 40))

    def __render_top_info(self) -> None:
        """ Method rendering all the info on top."""
        text: pygame.Surface = self.__INGAME_TEXT_FONT.render(
            str(self.__score_1), 1, c.WHITE)
        self.__screen.blit(text, (560, 20))
        text: pygame.Surface = self.__INGAME_TEXT_FONT.render(
            str(self.__score_2), 1, c.WHITE)
        self.__screen.blit(text, (680, 20))

        text: pygame.Surface = self.__INGAME_TEXT_FONT.render(
            self.__name_1, 1, c.WHITE)
        self.__screen.blit(text, (50, 20))
        text: pygame.Surface = self.__INGAME_TEXT_FONT.render(
            self.__name_2, 1, c.WHITE)
        self.__screen.blit(text, (765, 20))

        for paddle in self.__paddles:
            self.__render_powers_list(paddle)

    def __start_game(self) -> None:
        """ Method handling the game loop."""
        power_cd: int = c.POWER_UP_CD
        pygame.time.set_timer(pygame.USEREVENT, 1000)

        pygame.mixer.music.load(os.path.join(c.ASSETS_FOLDER, "music.wav"))
        pygame.mixer.music.set_volume(self.__music_volume)
        pygame.mixer.music.play(-1)

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
                self.__spawned_powers.update()

            self.__screen.fill(c.BLACK)
            self.__all_sprites_list.draw(self.__screen)
            self.__spawned_powers.draw(self.__screen)

            # creating punctured line
            self.__create_middle_line()
            self.__render_top_info()
            if self.__score_break > 0:
                self.__render_break_timer(self.__score_break)

            pygame.display.flip()

            if self.__score_1 >= self.__target_score:
                game_running = False
                print("Player one wins!")
            elif self.__score_2 >= self.__target_score:
                game_running = False
                print("Player two wins!")

            self.__clock.tick(60)

        pygame.quit()
        sys.exit()
