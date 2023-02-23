import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup

def download_links():
    # Get the webpage link
    webpage_link = link_entry.get()
    
    # Send a request to the webpage and get the response
    response = requests.get(webpage_link)
    
    # Parse the HTML of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the links on the webpage
    links = [link.get('href') for link in soup.find_all('a')]
    
    # Ask the user to select a folder to save the links
    folder_path = filedialog.askdirectory()
    
    # Download each link and save it to the selected folder
    for index, link in enumerate(links):
        response = requests.get(link)
        with open(f'{folder_path}/link_{index}.txt', 'wb') as f:
            f.write(response.content)

# Create the GUI
root = tk.Tk()
root.title("Link Downloader")

# Create a label and an entry widget to accept the webpage link
link_label = tk.Label(root, text="Webpage Link:")
link_label.grid(row=0, column=0)
link_entry = tk.Entry(root)
link_entry.grid(row=0, column=1)

# Create a button to start the download process
download_button = tk.Button(root, text="Download Links", command=download_links)
download_button.grid(row=1, column=0, columnspan=2)

# Run the GUI
root.mainloop()
