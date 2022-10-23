# -------- Boilerplate Code and Previous class Code Start ------
from multiprocessing.connection import Client
import socket
from sqlite3 import connect
from  threading import Thread
import time
from typing import Counter

IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
BUFFER_SIZE = 4096

clients = {}
# Teacher Activity
def handleShowList(client):
    global clients
    counter = 0
    for i in clients:
        counter = counter+1
        client_add = clients[i]["address"][0]
        connected_with=clients[i]["connected_with"]
        msg = ""
        if(connected_with):
            msg=f"{counter},{i},{client_add},{connected_with},tiul\n"
        else:
            msg=f"{counter},{i},{client_add},available,tiul,\n"
        client.send(msg.encode())
        time.sleep(1)



# Boilerlate Code
def handleMessges(client, message, client_name):
    if(message == 'show list'):
        handleShowList(client)
    


# Bolierplate Code
def handleClient(client, client_name):
    global clients
    global BUFFER_SIZE
    global SERVER

    # Sending welcome message
    banner1 = "Welcome, You are now connected to Server!\nClick on Refresh to see all available users.\nSelect the user and click on Connect to start chatting."
    client.send(banner1.encode())

    while True:
        try:
            BUFFER_SIZE = clients[client_name]["file_size"]
            chunk = client.recv(BUFFER_SIZE)
            message = chunk.decode().strip().lower()
            if(message):
                handleMessges(client, message, client_name)
            else:
                removeClient(client_name)
        except:
            pass

def removeClient(client):
    pass
    

# Boilerplate Code
def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()

        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
                "client"         : client,
                "address"        : addr,
                "connected_with" : "",
                "file_name"      : "",
                "file_size"      : 4096
            }

        print(f"Connection established with {client_name} : {addr}")

        thread = Thread(target = handleClient, args=(client,client_name,))
        thread.start()


def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    # Getting global values
    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    # Listening incomming connections
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()



setup_thread = Thread(target=setup)           #receiving multiple messages
setup_thread.start()
