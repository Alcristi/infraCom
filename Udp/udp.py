from socket import socket, AF_INET, SOCK_DGRAM
from dotenv import load_dotenv
from os import getenv
from typing import Callable

load_dotenv()

class UDP:
    def __init__(self, ip, port, buffer_size=1024):
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))
        self.data_buffer = {}

    def send(self, data, addr):
        self.socket.sendto(data, addr)

    def receive(self):
        data, addr = self.socket.recvfrom(self.buffer_size)
        return data, addr

    def close(self):
        self.socket.close()

