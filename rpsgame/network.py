import socket
import pickle


class Network:
    #responsible for connecting client to server
    def __init__(self):
        self.client_sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #making a new  client socket for client to send/receive data to and from server socket
        self.server="178.79.174.97"
        self.port=5555
        self.server_addr=(self.server, self.port)
        self.player_num= self.connect_client() 

    def get_player_num(self):
        return self.player_num

    def connect_client(self):
        try:
            self.client_sock.connect(self.server_addr) #connecting client socket to server socket
            received=self.client_sock.recv(2048).decode()
            return received     
        except:
            pass

    def send_data_to_server(self, data):
        try:
            self.client_sock.send(str.encode(data))
            received=pickle.loads(self.client_sock.recv(4096))
            return received
        except socket.error as error:
            print(str(error))
 