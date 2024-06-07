from Udp.udp import *
from os import listdir, path


class FtpUdpServe():
    def __init__(self):
        self.udp = UDP('',8080)
    def handle_client(self):
        print(f"Servidor FTP UDP aguardando na porta {self.udp_server.port}...")
        while True:
            data, addr = self.udp_server.receive()
            command = data.decode('utf-8').strip().split()

            if not command:
                continue

            if command[0] == 'LIST':
                self.send_list(addr)
            elif command[0] == 'UPLOAD':
                self.receive_file(command[1], addr)
            elif command[0] == 'DOWNLOAD':
                self.send_file(command[1], addr)
            elif command[0] == 'QUIT':
                self.udp_server.send(b"Goodbye", addr)
                break

    def send_list(self, addr):
            files = listdir('./database/server/')
            files_list = "\n".join(files)
            self.udp_server.send(files_list.encode('utf-8'), addr)

    def receive_file(self, filename, addr):
        with open(filename, "wb") as file:
            while True:
                data, _ = self.udp_server.receive()
                if data == b"END":
                    print(f"Arquivo {filename} recebido com sucesso.")
                    break
                file.write(data)

    def send_file(self, filename, addr):
        if not path.exists(filename):
            self.udp_server.send(b"ERROR: File not found", addr)
            return

        with open(filename, "rb") as file:
            while True:
                data = file.read(self.udp_server.buffer_size)
                if not data:
                    break
                self.udp_server.send(data, addr)
        self.udp_server.send(b"END", addr)
        print(f"Arquivo {filename} enviado com sucesso.")