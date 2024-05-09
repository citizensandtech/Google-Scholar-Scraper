import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import datetime

def scrape_scholar_articles(query, num_pages):
    articles = []
    page = 0

    query_date = datetime.datetime.now().strftime("%Y-%m-%d")

    while page < num_pages:
        url = f"https://scholar.google.com/scholar?start={page*10}&q={query}&hl=en&as_sdt=0,5"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("div", class_="gs_ri")

        for result in results:
            title = result.find("h3", class_="gs_rt").text
            authorship_string = result.find("div", class_="gs_a").text
            authors = authorship_string[0:authorship_string.find("-")].strip()
            publication_string = authorship_string[authorship_string.find("-")+1:-1]
            link = result.find("a")["href"]
            articles.append({"Query Date": query_date,"Title": title, "Authors": authors, "PublicationString": publication_string, "Link": link})

        page += 1

    return articles

def save_to_excel(articles, filename):
    df = pd.DataFrame(articles)
    df.to_excel(filename, index=False)

def browse_folder():
    folder_path = filedialog.askdirectory()
    entry_folder.delete(0, tk.END)
    entry_folder.insert(tk.END, folder_path)

def scrape_articles():
    query = entry_query.get()
    num_pages = int(entry_pages.get())

    articles = scrape_scholar_articles(query, num_pages)

    folder_path = entry_folder.get()
  
    unix_timestamp = int(datetime.datetime.now().timestamp())

    filename_string = str(unix_timestamp) + "-scholar_articles.xlsx"
    if folder_path:
        filename = f"{folder_path}/" + filename_string
    else:
        filename = filename_string

    save_to_excel(articles, filename)
    label_status.config(text="Extraction complete. Data saved to" + filename_string)

# Create the main window
window = tk.Tk()
window.title("Google Scholar Scraper")
window.geometry("400x250")

# Create input fields and labels
label_query = tk.Label(window, text="Article Title or Keyword:")
label_query.pack()
entry_query = tk.Entry(window, width=40)
entry_query.pack()

label_pages = tk.Label(window, text="Number of Pages:")
label_pages.pack()
entry_pages = tk.Entry(window, width=40)
entry_pages.pack()

label_folder = tk.Label(window, text="Output Folder (optional):")
label_folder.pack()
entry_folder = tk.Entry(window, width=40)
entry_folder.pack()

# Create browse button
button_browse = tk.Button(window, text="Browse", command=browse_folder)
button_browse.pack()

# Create extract button
button_extract = tk.Button(window, text="Extract Data", command=scrape_articles)
button_extract.pack()

# Create status label
label_status = tk.Label(window, text="")
label_status.pack()

# Run the main window loop
window.mainloop()
