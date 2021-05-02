import requests

file_subdo = requests.get("https://raw.githubusercontent.com/rbsec/dnscan/master/subdomains-10000.txt").text
subdomain = file_subdo.rsplit()
domain_to_cheak = input("Enter Domain Name to check: ")

for sub in subdomain:
    url_to_check = f"http://{sub}.{domain_to_cheak}"
    try:
        if requests.get(url_to_check).status_code == 200:
            print("[+] Found This Domain:" + url_to_check)
        else:
            pass

    except requests.ConnectionError:
        pass
