import socket


HOST = '127.0.0.1'
PORT = 9999


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    message = input('Enter length: ')
    client_socket.send(message.encode())
    message = input('Enter id: ')
    client_socket.send(message.encode())
    message = input('Enter data: ')
    client_socket.send(message.encode())


if __name__ == '__main__':
    main()