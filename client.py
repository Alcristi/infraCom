from Ftp.ftp_udp_client import FTPUDPClient

ftp_client = FTPUDPClient();
ftp_client.set_upload_path('./files')
ftp_client.upload_file_with_dowload('img2.png')
