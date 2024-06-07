from Udp.udp import *

class UDPClient:
    def __init__(self, server_ip, server_port, buffer_size=1024):
        self.server_ip = server_ip
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        self.socket.sendto(data, (self.server_ip, self.server_port))

    def receive(self):
        data, _ = self.socket.recvfrom(self.buffer_size)
        return data

    def close(self):
        self.socket.close()
