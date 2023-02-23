import requests
from bs4 import BeautifulSoup
import os
import sys
from urllib.parse import urlparse

if len(sys.argv) < 4:
    print("Usage: python download.py <URL> <folder> <extensions>")
    print("e.g.:python download.py https://www.datablist.com/learn/csv/download-sample-csv-files \"c:\Temp\RB\csv_datasets\" zip")
    sys.exit(1)

url, folder, extensions = sys.argv[1], sys.argv[2], sys.argv[3].split(',')
url_parts = urlparse(url)

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

if not os.path.exists(folder):
    os.makedirs(folder)

extensions = [ f".{ext}" for ext in extensions]
links = [link.get('href') for link in soup.find_all('a')]
files_to_download = set()
for link in links:
    for ext in extensions:
        if link.endswith(ext):
            files_to_download.add(link)

print("Count of files to download : ", len(files_to_download))

for i, file in enumerate(files_to_download):
    file_url_parts = urlparse(file)
    # if not file_url_parts.scheme:
    #     file_url = url_parts.scheme + '://' + url_parts.netloc + file
    # else:
    #     file_url = file
    # file_url = f'https:{file}'
    file_url = {file}
    file_path = os.path.join(folder, os.path.basename(file))

    print(f"File : {i}: {file_url} --> {file_path}")
    with requests.get(file_url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
