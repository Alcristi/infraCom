from Udp.udp import *
from os import listdir, path


class FTPUDPClient:
    def __init__(self, udp_client):
        self.udp_client = udp_client

    def send_command(self, command):
        self.udp_client.send(command.encode('utf-8'))

    def list_files(self):
        self.send_command("LIST")
        data = self.udp_client.receive()
        print(data.decode('utf-8'))

    def upload_file(self, filename):
        self.send_command(f"UPLOAD {filename}")
        with open(filename, "rb") as file:
            while True:
                data = file.read(self.udp_client.buffer_size)
                if not data:
                    break
                self.udp_client.send(data)
        self.udp_client.send(b"END")
        print(f"Arquivo {filename} enviado com sucesso.")

    def download_file(self, filename):
        self.send_command(f"DOWNLOAD {filename}")
        with open(f"downloaded_{filename}", "wb") as file:
            while True:
                data = self.udp_client.receive()
                if data == b"END":
                    print(f"Arquivo {filename} baixado com sucesso.")
                    break
                elif data.startswith(b"ERROR"):
                    print(data.decode('utf-8'))
                    break
                file.write(data)

    def quit(self):
        self.send_command("QUIT")
        data = self.udp_client.receive()
        print(data.decode('utf-8'))

    def close(self):
        self.udp_client.close()
