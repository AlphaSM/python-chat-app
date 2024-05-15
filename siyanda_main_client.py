from socket import * 
import threading
from random import randint
import os

#get available ports 
def find_open_ports():
    #improved searching free port 
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('',0))
    port = sock.getsockname()[1]
    yield port 
    """
    for port in range(1024,30000):  # Adjust the range as needed
        sock = socket(AF_INET, SOCK_STREAM)
        res = sock.connect_ex(('localhost', port))
        if res ==  0:
            yield port
        sock.close()
    """
#get port 
print("Finding available port")
#list of available ports 
available_ports = list(find_open_ports())
#select the port
random_index = randint(0, len(available_ports) - 1)
#get the port for udp 
udpPort = available_ports[random_index] 
print(f"found available port {udpPort}" )
#get the ip
print("getting my ip")
udpServer = gethostbyname(gethostname())
print(f"got my ip {udpServer}")
#create udp socket 
print("making udp socket")
s = socket(AF_INET , SOCK_DGRAM)
print("made udp socket")
#get the address
address = (udpServer, udpPort)
#bind it to that address
s.bind((address))

#tcp server 
#Server IP: 196.47.217.205
#Server Port: 1200

#get ip and port 
print("Connecting to TCP server")
host = input("Enter server's IP address: ")
port = int(input("Enter server's port number: "))
serverName = host
serverPort = port

#create TCP socket for server  remote port 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
#No need to attach server name, port
clientSocket.connect((serverName,serverPort)) 
#receive Send welcome message to the client for successful connection 
print(clientSocket.recv(1024).decode())

#send udp port to server 
clientSocket.send(str(udpPort).encode()) 


#for username request
username = input(clientSocket.recv(1024).decode())
#send username
clientSocket.send(username.encode())

#send udp port to server 
#clientSocket.send(str(udpPort).encode()) 
#for username prompt
#username = input(clientSocket.recv(1024).decode())
#send username
#clientSocket.send(username.encode()) 
#for availability prompt
availability = input(clientSocket.recv(1024).decode())
#send availability
clientSocket.send(availability.encode()) 
#who do you want to chat too? 

#print(clientSocket.recv(1024).decode())

while True: 
  #get input
  sentence = input("Enter a command:") 
  command_parts = sentence.split(" ")
  #if sentence.lower().strip() == "bye tcp":
  if command_parts[0].lower() == "bye" and command_parts[1].lower() == "tcp":
    clientSocket.send(sentence.encode())
    #close socket
    print("Ending Connection with TCP...")
    clientSocket.close()
    print("Connection Ended")
    break

  #chat to username 
  #command_parts = sentence.split(" ")
  #chat to username
  #make into GET command 
  

  if command_parts[0].lower() == "chat" and command_parts[1].lower() == "to":
    #client to chat to 
    wanted_client = command_parts[2]
    #send message "chat to user"
    clientSocket.send(sentence.encode())
    print("getting information")
    #does the user exist, is the user in the chat or is the chat ready to go 
    
    #receive message
    useraddress = clientSocket.recv(1024).decode()
    #user_IP = clientSocket.recv(1024).decode()
    #user_Port = clientSocket.recv(1024).decode()
    userAddress = useraddress.split(" ")
    print(userAddress)
    user_IP = userAddress[0]
    user_Port = userAddress[1]
    print("Setting up udp connection") 
    nm = command_parts[2]
    print(f"Connecting to {nm}")
    ip = user_IP
    print(f"Connecting at IP: {ip}")
    port = user_Port.split(":")[0]
    print(f"Connecting at Port: {port}")
    #start chat
    def send():
        while True:
          ms = input(">> ")
          if ms.lower().strip() == "quit":
              sm = "{}  : {}".format(username,f"{username} has quit the chat")
              s.sendto(sm.encode() , (ip,int(port)))
              os._exit(1)
          sm = "{}  : {}".format(username,ms)
          s.sendto(sm.encode() , (ip,int(port)))
    def rec():
          while True:
              msg = s.recvfrom(1024)
              if msg[0].lower().strip() == "quit":
                print(f"{nm} has disconnected")
              print("\t\t\t\t >> " +  msg[0].decode()  )
              print(">> ")

    x1 = threading.Thread( target = send )
    x2 = threading.Thread( target = rec )

    x1.start()
    x2.start()

    x1.join()
    x2.join()

  if command_parts[0].lower() == "get" and command_parts[1].lower() == "list":
    clientSocket.send(sentence.encode())
    print("getting list")
    print(clientSocket.recv(1024).decode())

  #send message
  #clientSocket.send(sentence.encode()) 
  #receive message from message
  #modifiedSentence = clientSocket.recv(1024).decode()
  #check for user not for not found
  #display message from server 
  #print ("From Server:", modifiedSentence) 
#close socket 
#clientSocket.close()