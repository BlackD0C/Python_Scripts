from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import ARP, Ether
from scapy.all import *

ips = []
target_ip = "192.168.14.1/24"
arp = ARP(pdst=target_ip)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = ether / arp
result = srp(packet, timeout=3, verbose=0)[0]
clients = []
for sent, received in result:
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})
print("Available devices in the network:")
print("IP" + " " * 18 + "MAC")
for client in clients:
    print("{}    {}".format(client['ip'], client['mac']))
    ips.append(client['ip'])

us = input('[?] Scans the ports(Y/n)? ').lower()
if us =='y':
    for x in range(len(ips)):
        ip = ips[x]
        print('\n[+] Start scanig {}'.format(ip))
        for port in range(1024):
                x = (IP(dst=ip) / TCP(dport=[port], flags='S'))
                rec, wrong = sr(x, timeout=0.5, verbose=0)
                if rec:
                    data = '{}'.format(rec[0]).split(" ")[7][6:]
                    if data.isnumeric():
                        pass
                    else:
                        print('\t\t- port {} , service = {}'.format(port, data))
else:
    print('Bye Bye..')
    exit()