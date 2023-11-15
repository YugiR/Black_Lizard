from collections import deque
import re
import pyfiglet
from bs4 import BeautifulSoup
import requests
import urllib.parse

ascii_banner = pyfiglet.figlet_format("Black_Lizard")
print(ascii_banner)
print("created by @Yugi")
print("https://example.com/")
user_url = str(input("[*] Enter Domain: "))
urls = deque([user_url])
scraped_urls = set()
emails = set()
count = 0

try:
    while True:
        count += 1
        if count > 100:
            break
        url = urls.popleft()
        scraped_urls.add(url)
        parts = urllib.parse.urlsplit(url)
        base_url = f'{parts.scheme}://{parts.netloc}'
        path = url[:url.rfind('/')+1] if '/' in parts.path else url
        
        print(f'{count} processing {url}')
        try:
            response = requests.get(url)
        except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue
        new_emails = set(re.findall(r'[a-z0-9\.\-+_]+@\w+\.+[a-z\.]+', response.text, re.I))
        emails.update(new_emails)
        soup = BeautifulSoup(response.text, 'html.parser')
        for anchor in soup.find_all('a'):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
                
            if not link in urls and not link in scraped_urls:
                urls.append(link)
        
except KeyboardInterrupt:
    print("[-] Closing!")
    
print("\n Process done! ")
print(f'\n{len(emails)} Emails Found ')

for mail in emails:
    print('  ' + mail)
print('\n')