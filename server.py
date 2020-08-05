from blockchain import Block
from blockchain import Blockchain
from hashlib import sha256
import json
import time
import socket
import shelve


def see_blocks(blockchain):
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)

    for i in chain_data:
        print(i)


def see_messages(blockchain):
    for block in blockchain.chain:
        print(block.transactions)


def send_messages(blockchain):
    messages = []
    for block in blockchain.chain:
        messages.append(str(block.transactions).strip('[]'))

    return messages


HOST = ''
PORT = 5001

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

blockchain = Blockchain()

bd = shelve.open("data.dat")

while True:
    con, cliente = tcp.accept()
    print('Concetado por', cliente)

    while True:
        signal = con.recv(1024)
        msg = str(signal.decode())

        if msg == 'EXIT':
            break

        elif msg == 'COMMITMESSAGE':
            blockchain.mine()
            bd["blockchain"] = blockchain

        elif msg == 'READMESSAGE':
            stored_blockchain = bd["blockchain"]
            data = send_messages(stored_blockchain)
            message = ' \n'.join(data)
            con.send(message.encode())

        else:
            blockchain.add_new_transaction(msg)

    print('finalizando conexao com', cliente)
    con.close()

    print('BLOCKS:\n')
    see_blocks(blockchain)
