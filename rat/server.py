import socket
import os

# host = input('please insert your server ip address:\n')
host = socket.gethostname()
host = socket.gethostbyname(host)
print(host)
# host = '127.0.0.1'
# ports = [port for port in range(10,10000) if port % 3 == 0 ]
# print(port)
port = 99

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
    skt.bind((host, port))
    skt.listen()
    connection, addr = skt.accept()
    with connection:
        print(f'connected by :{addr}')
        while True:
            data = connection.recv(4068)
            if not data:
                break
            print(data.decode('utf-8'))  # Decode received data
            command = input('please insert your command:\n')
            connection.sendall(bytes(command, encoding='UTF-8'))
