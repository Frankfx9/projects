import socket
import sys
import threading


if len(sys.argv) < 2:
    print(f"[-] Usage: python3 {sys.argv[0]} <ip_addr>")
    sys.exit(1)


ip = sys.argv[1]
username_list = []


clients = {}  # Map usernames to client sockets


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, 9999))
server.listen()

def handle_client(client, username):
    clients[username] = client
    while True:
        try:
            command = client.recv(1024).decode().strip()
            if not command: # Upon disconnection command is and empty byte string..this can cause infinte loop errors
                print("Client disconnected.")
                del clients[username] # Deletes user if user is not online or disconnected
                break

            if command == "list users":
                users = "\n".join(username_list)
                client.send(users.encode())


            if "message" in command:
                full_command = command.split()
                if len(full_command) < 2:
                    client.send("Use message {username} to chat\n".encode())
                    continue
                user_to_chat = full_command[-1]
                if user_to_chat not in clients:
                    client.send(f"User {user_to_chat} is not online".encode())
                    
                else:
                    # Prompt target user of incoming chat connection
                    target_client = clients[user_to_chat]
                    target_client.send(f"{username} wants to chat. Accept?(Yes or No):> ".encode())
                    response = target_client.recv(1024).decode().strip()
                    if response.lower() == "yes":
                        client.send(f"User {user_to_chat} has accepted your invitation to chat!".encode())
                        target_client.send(f"You are now in a private chat with {username}!".encode())
                        privateChat(client, target_client)

                    else:
                        client.send(f"User {user_to_chat} has declined your invite!".encode())
            
        except Exception as e:
            print(f"Error: {e}")
            del clients[username]
            break
    client.close()

def privateChat(client1, client2):
    client1.send("You are now in a private chat!\nType 'exit' to leave.\n".encode())
    client2.send("You are now in a private chat!\nType 'exit' to leave.\n".encode())
    while True:
        try:
            message1 = client1.recv(10000).decode().strip()
            if message1.lower() == "exit":
                client1.send("Exiting private chat...".encode())
                client2.send(f"{client1} left the chat".encode())
                break
            client2.send(f"{client1}:> {message1}".encode())

            message2 = client2.recv(10000).decode().strip()
            if message2.lower() == "exit":
                client2.send("Exiting private chat...".encode())
                client1.send(f"{client2} left the chat".encode())
                break
            client1.send(f"{client2}:> {message2}".encode())

        except Exception as e:
            print(f"Private chat error: {e}")
            break



while True:
    client, addr = server.accept()
    print(f"Received conn from {addr}")
    username = client.recv(1024).decode()
    username_list.append(username)


    threading.Thread(target=handle_client, args=(client, username)).start()

        

