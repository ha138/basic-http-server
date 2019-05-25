#! /usr/bin/python3.6

import socket
from time import sleep

port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4, TCP
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
while True:
    try:
        server.bind(('0.0.0.0', port))
        break
    except OSError:
        print('Address already in use')
        port = int(input('Enter the new port: '))
        continue
server.listen(5)
print('Server running')

while True:
    try:
        client, (ip, port) = server.accept()  # Connect client
        print('Connected ' + ip + ':' + str(port))
        request = client.recv(1024).decode()  # receive request from client
        request = request.splitlines()[0]  # get line 1
        request = request.split(' ')[1]  # get http address
        print('Request: ' + request)

        header = 'HTTP/1.1 403 forbidden\n\n'
        response = '''
        <head>
            <title>
                forbidden
            </title>
            <meta http-equiv="refresh" content="2; URL=http://www.google.com/"/>
        </head>
        <body>
            <h1>
                <center>
                    forbidden
                </center>
            <h1>
        </body>
        '''

        client.send(header.encode('utf-8') + response.encode('utf-8'))
        client.close()
    except KeyboardInterrupt:
        server.close()
        print('Server is down')
        exit()
    except Exception as e:
        print(repr(e))
        continue
