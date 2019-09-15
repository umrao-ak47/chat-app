import socket
import select
import sys

IP = "127.0.0.1"
PORT = 1234
HEADER_LENGHT = 10


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets_list = [self.server_socket]
        self.clients = {}

    def bind(self):
        self.server_socket.bind((IP, PORT))
        self.server_socket.listen()

    def add_new_client(self):
        client_socket, address = self.server_socket.accept()
        print(address)
        user = self.recieve_msg(client_socket)
        print("User",user)
        if user is False:
            return
        print(f"Got Connection from {user['data'].decode('utf-8')} at {address[0]}:{address[1]}")
        self.sockets_list.append(client_socket)
        self.clients[client_socket] = user

    def remove_client(self,client):
        self.sockets_list.remove(client)
        del self.clients[client]

    def recieve_msg(self,client_socket):
        try:
            msg_header = client_socket.recv(HEADER_LENGHT)
            msg_length = int(msg_header.decode('utf-8').strip())
            msg = client_socket.recv(msg_length)
            if not len(msg):
                return False
            return {"header": msg_header, "data": msg}
        except Exception as e:
            #print("Exception",str(e))
            return False

    def distribute_msg_of(self,client):
        msg = self.recieve_msg(client)
        user = self.clients[client]
        if msg is False:
            print(f"Closed Connection from {user['data'].decode('utf-8')}")
            self.remove_client(client)
            return
        for client_socket in self.clients.keys():
            client_socket.send(user['header']+user['data']+msg['header']+msg['data'])

    def listen(self):
        read_sockets,wait_sockets,exception_sockets = select.select(self.sockets_list,[],self.sockets_list)
        for informed_socket in read_sockets:
            if informed_socket == self.server_socket:
                self.add_new_client()
            else:
                self.distribute_msg_of(informed_socket)
        for informed_socket in exception_sockets:
            print(f"Closed Connection from {self.clients[informed_socket]['data']}")
            self.remove_client(informed_socket)

    def run(self):
        self.bind()
        print(f"Server Started at {IP}:{PORT} .....",end='\n')
        while True:
            self.listen()

if __name__=="__main__":
    Server().run()
