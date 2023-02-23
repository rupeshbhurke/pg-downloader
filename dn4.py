import os
import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup

def download_links():
    # Get the webpage link
    webpage_link = link_entry.get()
    # Get the folder path
    folder_path = folder_entry.get()
    
    # Check if the folder exists, if not create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Disable the link and folder entry widgets
    link_entry.config(state='disable')
    folder_entry.config(state='disable')
    download_button.config(state='disable')
    folder_button.config(state='disable')
    
    # Send a request to the webpage and get the response
    response = requests.get(webpage_link)
    
    # Parse the HTML of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the links on the webpage
    links = [link.get('href') for link in soup.find_all('a')]
    
    # Download each link and save it to the selected folder
    for index, link in enumerate(links):
        response = requests.get(link)
        filename, file_extension = os.path.splitext(link)
        with open(f'{folder_path}/link_{index}{file_extension}', 'wb') as f:
            f.write(response.content)
    
    # Enable the link and folder entry widgets
    link_entry.config(state='normal')
    folder_entry.config(state='normal')
    download_button.config(state='normal')
    folder_button.config(state='normal')

def open_folder_dialog():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

# Create the GUI
root = tk.Tk()
root.title("Link Downloader")

# Create a label and an entry widget to accept the webpage link
link_label = tk.Label(root, text="Webpage Link:")
link_label.grid(row=0, column=0, pady=5, padx=5)
link_entry = tk.Entry(root)
link_entry.grid(row=0, column=1, pady=5, padx=5, columnspan=2)

# Create a label and an entry widget to accept the folder path
folder_label = tk.Label(root, text="Save to folder:")
folder_label.grid(row=1, column=0, pady=5, padx=5)
folder_entry = tk.Entry(root)
folder_entry.grid(row=1, column=1, pady=5, padx=5)

# Create a button to open folder dialog
folder_button = tk.Button(root, text="Browse", command=open_folder_dialog)
folder_button.grid(row=1, column=2, pady=5, padx=5)

# Create a button to start downloading the links
download_button = tk.Button(root, text="Download", command=download_links)
download_button.grid(row=2, column=1, pady=5, padx=5)

# Create a label to display status of the download
status_label = tk.Label(root, text="")
status_label.grid(row=3, column=0, columnspan=3, pady=5, padx=5)

root.mainloop()
