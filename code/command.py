# ce code envoie les commandes au drone, il faut le démarrer en premier.
# penser à adapter les adresses

import socket
from pathlib import Path
import os

path = Path('command.txt')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)

sock.bind(('', 9000))
command = "command"

command = command.encode()
streamon = 'streamon'
streamon = streamon.encode()

while True:
    if path.is_file():
        text_file = open('command.txt', 'r')
        msg = text_file.read()
        print(msg)  # nous permet de suivre si le message est bien lu
        msg = msg.encode()
        sent = sock.sendto(command, tello_address)  # envoie l'ordre au drone ("command" + l'ordre)
        text_file.close()
        sent = sock.sendto(msg, tello_address)
        sent = sock.sendto(command, tello_address)
        sent = sock.sendto(streamon, tello_address)  # on lance automatiquement le stream
        os.remove('command.txt')
