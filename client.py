from blockchain import Block
from blockchain import Blockchain
from hashlib import sha256
import json
import time
import socket

HOST = '127.0.0.1'
PORT = 5001
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

name = input('inform your name\n')

# menu
command = int(
    input('1 to write \n2 to commit \n3 to read messages \nanything to exit\n\n'))
while command != 0:
    if command == 1:
        words = input('write a message\n')
        msg = '{name}: {words}'.format(name=name, words=words)
        tcp.send(msg.encode())

    elif command == 2:
        msg = 'COMMITMESSAGE'
        tcp.send(msg.encode())

    elif command == 3:
        msg = 'READMESSAGE'
        tcp.send(msg.encode())
        data = tcp.recv(1024)
        data = data.decode()
        print(data)

    else:
        msg = 'EXIT'
        tcp.send(msg.encode())
        break

    command = int(
        input('\n\n1 to write \n2 to commit \n3 to read messages \nanything to exit\n\n'))

print('going out ...')
tcp.close()
