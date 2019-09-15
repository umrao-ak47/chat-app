import socket
import select

HEADER_LENGTH = 10


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, name, ip, port):
        self.client_socket.connect((ip, port))
        self.client_socket.setblocking(False)
        self.send_msg(name)

    def close(self):
        self.client_socket.close()

    def send_msg(self,msg):
        msg = msg.encode('utf-8')
        msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(msg_header+msg)

    def recieve_msg(self):
        username_header = self.client_socket.recv(HEADER_LENGTH)
        if not len(username_header):
            print("Connection Closed by Server")
            return False
        username_length = int(username_header.decode('utf-8').strip())
        user_name = self.client_socket.recv(username_length).decode('utf-8')
        msg_header = self.client_socket.recv(HEADER_LENGTH)
        msg_length = int(msg_header.decode('utf-8').strip())
        msg = self.client_socket.recv(msg_length).decode('utf-8')
        msg = f"{user_name} >> {msg}"
        # print("Msg:",msg)
        return msg
