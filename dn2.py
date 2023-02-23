import tkinter as tk
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup

def download_links():
    # Get the webpage link
    webpage_link = link_entry.get()
    # Get the folder path
    folder_path = folder_entry.get()
    
    # Send a request to the webpage and get the response
    response = requests.get(webpage_link)
    
    # Parse the HTML of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the links on the webpage
    links = [link.get('href') for link in soup.find_all('a')]
    
    # Download each link and save it to the selected folder
    for index, link in enumerate(links):
        response = requests.get(link)
        with open(f'{folder_path}/link_{index}.txt', 'wb') as f:
            f.write(response.content)

def open_folder_dialog():
    folder_path = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)

# Create the GUI
root = tk.Tk()
root.title("Link Downloader")

# Create a label and an entry widget to accept the webpage link
link_label = tk.Label(root, text="Webpage Link:")
link_label.grid(row=0, column=0, pady=5)
link_entry = tk.Entry(root)
link_entry.grid(row=0, column=1, pady=5)

# Create a label and an entry widget to accept the folder path
folder_label = tk.Label(root, text="Save to folder:")
folder_label.grid(row=1, column=0, pady=5)
folder_entry = tk.Entry(root)
folder_entry.grid(row=1, column=1, pady=5)

# Create a button to open folder dialog
folder_button = tk.Button(root, text="Browse", command=open_folder_dialog)
folder_button.grid(row=1, column=2, pady=5)

# Create a button to start the download process
download_button = tk.Button(root, text="Download Links", command=download_links)
download_button.grid(row=2, column=0, columnspan=3, pady=5)

# Run the GUI
root.mainloop()
