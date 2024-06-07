from Udp.udp_client import UDPClient
from os import listdir, path,getenv
from dotenv import load_dotenv

load_dotenv ()
server_ip = getenv('SERVER_NAME')
server_port = int(getenv('SERVER_PORT'))

class FTPUDPClient:
    def __init__(self):
        self.udp_client = UDPClient(server_ip,server_port)
        self.upload_path = './files'
        self.download_path = './database/client/'
    def send_command(self, command):
        self.udp_client.send(command.encode('utf-8'))

    def list_files(self):
        self.send_command("LIST")
        data = self.udp_client.receive()
        print(data.decode('utf-8'))

    def upload_file(self, filename):
        self.send_command(f"UPLOAD {filename}")
        with open(self.upload_path + filename, "rb") as file:
            while True:
                data = file.read(self.udp_client.buffer_size)
                if not data:
                    break
                self.udp_client.send(data)
        self.udp_client.send(b"END")
        print(f"Arquivo {filename} enviado com sucesso.")

    def upload_file_with_dowload(self, filename):
        self.send_command(f"UPLOAD_WITH_DOWNLOAD {filename}")
        with open(self.upload_path + filename, "rb") as file:
            while True:
                data = file.read(self.udp_client.buffer_size)
                if not data:
                    break
                self.udp_client.send(data)
        self.udp_client.send(b"END")
        print(f"Arquivo {filename} enviado com sucesso.")
        data = self.udp_client.receive()
        self.download_file(data.decode())

    def download_file(self, filename):
        self.send_command(f"DOWNLOAD {filename}")
        with open(f"{self.download_path}{filename}", "wb") as file:
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

    def set_dowload_path(self,path):
        if path[-1] == '/':
            self.download_path = path
        else:
            self.download_path = path + '/'
            

    def set_upload_path(self,path):
        if path[-1] == '/':
            self.upload_path = path
        else:
            self.upload_path  = path + '/'
