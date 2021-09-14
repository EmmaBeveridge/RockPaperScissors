import pickle
import socket
from _thread import *
import sys
from game import Game

server=""
port=5555

sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    sock.bind((server, port))

except socket.error as socket_error:
    print(str(socket_error))



sock.listen(2)
print("Server initialised, waiting for client connection")

connected_clients= set()
games={}
id_count=0 #how maby people connected to server at once


def client_thread(conn, player_num, gameId):
    
    global id_count
    conn.send(str.encode(str(player_num)))
    reply=""
    while True:
        try:
            data=conn.recv(4096).decode()

            if gameId in games: #checks if game still exists, if a client disconnects, their game will be deleted 
                game= games[gameId]
                if not data:
                    break
                else:
                    
                    if data=="reset":
                        game.reset_game()
                    
                    elif data != "get":
                        game.play(player_num, data)

                    
                    conn.sendall(pickle.dumps(game)) #pickle allows for object to be sent over network
            else:
                break
        except:
            break
    
    
    
    print("Lost connection")
    
    try:
        del games[gameId]
        print("Closing game", gameId)
    except:
        pass
    
    id_count-=1
    conn.close()


while True:
    #threading allows for many user connections to be handled and for new users to connect whilst user connections are being handled
    conn, addr= sock.accept()
    print("Connected to:", addr)
    
    id_count+=1
    player_num=0
    gameId=(id_count-1)//2 #
    
    if id_count%2==1: #checks if new game needs to be created
        games[gameId]=Game(gameId)
        print("Creating a new game")
    else:
        games[gameId].game_ready=True
        print("Game is ready:", games[gameId].game_ready )
        player_num=1


    start_new_thread(client_thread, (conn, player_num, gameId))
    
    
