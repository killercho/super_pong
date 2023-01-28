""" Server file that includes the logic for the server. """

import socket
from _thread import *
import pickle
from game import Game
import constants as c

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((c.HOST_IP_ADDRESS, c.PORT))
except socket.error as e:
    print(e)

server.listen()
print("Server started.")
print("Waiting for a connection...")

connected = set()
games = {}
id_count: int = 0


def threaded_client(connection, player, game_id):
    connection.send(str.encode(str(player)))
    global id_count

    while True:
        try:
            data = connection.recv(c.SEND_SIZE).decode()
            print(data + " first receiver")

            if game_id in games:
                game = games[game_id]

                print("found game with id" + game_id)

                if not data:
                    print("breaks because no data")
                    break
                else:
                    if data == "one_up":
                        game.move_one_up()
                    elif data == "one_down":
                        game.move_one_down()
                    elif data == "two_up":
                        game.move_two_up()
                    elif data == "two_down":
                        game.move_two_down()
                    elif data == "score_one":
                        game.increase_score_one()
                        game.reverse_ball_x()
                    elif data == "score_two":
                        game.increase_score_two()
                        game.reverse_ball_x()
                    elif data == "reverse_y":
                        game.reverse_ball_y()
                    elif data == "bounce":
                        game.bounce_ball()

                    game.update_ball()
                    connection.sendall(pickle.dumps(game))
            else:
                print("break because no game")
                break
        except:
            print("break on the first get")
            break

    print("Lost connection.")
    try:
        del games[game_id]
        print("Closing game", game_id)
    except:
        pass

    id_count -= 1
    connection.close()


while True:
    connection, addr = server.accept()
    # get the id from the second client and compare it to existing game here
    print("Connected to: ", addr)

    id_count += 1
    player: int = 1
    game_id: int = (id_count - 1) // 2
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    else:
        player = 2
        games[game_id].set_player_ready()
        # add the player to the game

    start_new_thread(threaded_client, (connection, player, game_id))
