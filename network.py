""" Python script holding the network class. """
import socket
import pickle
import constants as c


class Network:
    """ Network class managing the sending and receiving data from the server. """

    def __init__(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server: str = c.HOST_IP_ADDRESS
        self.__port: int = c.PORT
        self.__addr = (self.__server, self.__port)
        self.__player = self.__connect()

    def __connect(self):
        try:
            self.__client.connect(self.__addr)
            return self.__client.recv(c.SEND_SIZE).decode()
        except:
            print("E: Client could not connect.")

    def get_player(self):
        return self.__player

    def send(self, data):
        try:
            self.__client.send(str.encode(data))
            return pickle.loads(self.__client.recv(c.SEND_SIZE))
        except socket.error as e:
            print(e)
