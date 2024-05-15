import socket
import threading

# Dictionary to keep track of clients
clients = {}
usernames_addresses = {}
udp_ports = {}
peers = []
in_chat = []

def handle_client(connectionSocket, addr):
    global clients
    global usernames_addresses
    global peers
    global in_chat

    #receive udp port 
    udpPort = connectionSocket.recv(1024).decode().strip()

    # Request username from the client
    connectionSocket.send("Please enter your username: ".encode())

    clients[connectionSocket] = addr  # Store the client's socket and address
    #clients[username] = connectionSocket
    #print(f"New connection from {addr}")

    # Receive and decode the username
    username = connectionSocket.recv(1024).decode().strip()

    #add to list 
    #save tcp address to username
    usernames_addresses[username] = connectionSocket
    #save udp port to username
    udp_ports[username] = udpPort
    #save to peers 
    peers.append(username)
    #print announcement 
    print(f"User {username} connected from {addr} is connected")
    print(f"User {username} udp port is {udpPort}")

    # Ask if the user is available to chat
    
    connectionSocket.send("Are you available to chat? (yes/no). If you say yes you will be avaialble. If you say no, type in AVAILABLE): ".encode())
    
    # Receive and decode the availability response
    
    availability = connectionSocket.recv(1024).decode() #receives an answer 
    if availability.lower() == "yes":
        print(f"Client {username} from {addr} is available to chat")
         
    else:
        print(f"Client {username} from {addr} is not available to chat")
    
    #add in privacy 
        
    
    while True:
        try:
            # Receive command from client
            sentence = connectionSocket.recv(1024).decode().strip()

            if not sentence:
                break
            
            command_parts = sentence.split(" ")
            # If the client requests the list of clients, send it
            

            if command_parts[0].lower() == "get" and command_parts[1].lower() == "list":
                print(f"Client {username} from {addr} is requesting the list of peers")
                list = str(peers)
                connectionSocket.send(list.encode())
            

            
            #CONNECT TO USER 
            if command_parts[0].lower() == "chat" and command_parts[1].lower() == "to":
                #gets username of wanted client 
                target_username = command_parts[2]
                #searches in list for the username
                if target_username in usernames_addresses:
                    print(f"{target_username} getting information")
                    #get socket 
                    target_socket = usernames_addresses[target_username]           
                    #gets address
                    target_address = clients[target_socket]
                    target_port = udp_ports[target_username]
                    print(f"{target_username}'s udp port is {target_port}")
                    #print(target_address)
                    #send user found 
                    userIP = target_address[0] 
                    userPort = str(target_port)
                    #send IP 
                    #connectionSocket.send(userIP.encode())
                    #send Port 
                    #connectionSocket.send(userPort.encode())
                    useraddress = userIP+" "+userPort+":"
                    #send user info
                    connectionSocket.send(useraddress.encode())
                    #add wanted user to chat mode 
                    #knownPorts = list(find_open_ports())
                    #knownPort = str(knownPorts[0])
                    #print(knownPort)
                    #connectionSocket.send(knownPort.encode())
                else:
                    response = "User not found."
                    connectionSocket.send(response.encode())
            
            #Disconnect from tcp server
            if command_parts[0].lower() == "bye" and command_parts[1].lower() == "tcp":
                print(f"Client {username} from {addr} is disconnecting")
                break
            else:
                connectionSocket.send("Please enter a command".encode())
        except Exception as e:
            print(f"Error: {e}")
            break
        
    #22107  
    # Print a message indicating the client has disconnected
    print(f"Client {username} from {addr} has disconnected")
    #connectionSocket.close()
    del clients[connectionSocket]  # Remove the client from the list when it disconnects
    del usernames_addresses[username] #Remove username from the list also 
    peers.remove(username)
    in_chat.remove(username)
    connectionSocket.close()

#find available ports 
def find_open_ports():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('',0))
    port = sock.getsockname()[1]
    yield port 
    """
    for port in range(1,8081):  # Adjust the range as needed
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = sock.connect_ex(('localhost', port))
        if res ==  0:
            yield port
        sock.close()
    """

#send the peers available
def list_to_string(list): 
    concatenated_string = ""
    # Iterate over the dictionary items
    for key, value in list.items():
    # Convert each item to a string and concatenate with a separator
        concatenated_string += f"{key}:{value}, "
    # Remove the trailing comma and space from the last item
    concatenated_string = concatenated_string.rstrip(", ")
    return concatenated_string



def start_server():
    
    serverPort = 1200 #available_ports[0]
    serverIP = socket.gethostbyname(socket.gethostname())
    print(f"Server IP: {serverIP}")
    print(f"Server Port: {serverPort}")
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (serverIP, serverPort)
    
    serverSocket.bind(address)
    serverSocket.listen(1)
    print("TCP server is ready to receive")
    
    while True:
        # Accept a connection
        connectionSocket, addr = serverSocket.accept()

        #states is connected
        print(f"{addr} is connected")
        
        # Send welcome message to the client
        welcome_message = "Welcome to TCP server. Your status is connected"
        connectionSocket.send(welcome_message.encode())

        #start thread
        threading.Thread(target=handle_client, args=(connectionSocket, addr)).start()


if __name__ == "__main__":
    start_server()