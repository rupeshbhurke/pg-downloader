import requests
from bs4 import BeautifulSoup
import os
import sys
from urllib.parse import urlparse
from tqdm import tqdm

if len(sys.argv) < 4:
    print("Usage: python download_links.py <URL> <folder> <extensions>")
    sys.exit(1)

url, folder, extensions = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
url_parts = urlparse(url)

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

if not os.path.exists(folder):
    os.makedirs(folder)

extensions = [ f".{ext}" for ext in extensions]
links = [link.get('href') for link in soup.find_all('a')]
files_to_download = [link for link in links for ext in extensions if link.endswith(ext)]

print("Count of files to download : ", len(files_to_download))

for file in files_to_download:
    file_url_parts = urlparse(file)
    if not file_url_parts.scheme:
        file_url = url_parts.scheme + '://' + url_parts.netloc + file
    else:
        file_url = file
    file_path = os.path.join(folder, os.path.basename(file))
    with open(file_path, 'wb') as f:
        response = requests.get(file_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        # progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        for data in response.iter_content(block_size):
            # progress_bar.update(len(data))
            f.write(data)
        # progress_bar.close()
