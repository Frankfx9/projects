import socket
import sys
import time

# Just did it only call this function when we connect
joined = False
# Get prerequisites
username = input("Enter your username:> ")

# Define basic functions
def helpMessage():
    print("\t+[+[+[Help Message]+]+]+\n")
    print("1) Basic functions \n\t*help - displays this page \n\t*change username - changes your username\n\t*list users - displays users who are active and haven't hidden their status \n\t*list groups - lists available groups(not hidden)\n\t*set status - changes status to on or offline")


while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    command = input(f"{username}:> ")


# Basic functions
    if command.lower() == "change username":
        username = input("Enter your new username:> ")

    elif command.lower() == "exit" or command.lower() == "quit":
        break
    
    elif command.lower() == "help":
        helpMessage()
    elif command.lower().strip() == "join server":
        ip = input("Enter IP address of server:> ")
        client.connect((ip, 9999))
        client.send(username.encode())
        while True:
            command = input(f"{username}:> ")
            if command.lower().strip() == "list users":
                client.send("list users".encode())
                time.sleep(0.6)
                users = client.recv(10000).decode().strip()
                print(users)
            
            if "message" in command.lower().strip():
                client.send(command.lower().strip().encode())

            

                        