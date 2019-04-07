import requests
import bs4 #for pulling data out of HTML and XML files
import os
import re
cwd = os.getcwd()
url = input("Enter your URL here: ")
def download_lyrics(url):
    """download lyrics form url and return as string format"""
    res = requests.get(url)
    data = bs4.BeautifulSoup(res.text, 'lxml')
    folder_name = data.find("div", class_="grid_6 suffix_6").h1.text
    try:
        os.mkdir("{}/training_data/{}".format(cwd, folder_name))
    except FileExistsError:
        None
    body = data.find('div',id ='popular')
    sub_body = body.find('tbody')
       # print(body.prettify())
    for file_names in sub_body.find_all('a',class_="title hasvidtable"):
        file_name =file_names.get('alt')
        link  = file_names.get("href")
        res1 = requests.get(link)
        soup = bs4.BeautifulSoup(res1.text, 'lxml')
        print(file_name)
        print(link)
        lyrics = " "
        for i in soup.select('.verse'):
            lyrics += i.text
        file_path = os.path.join("{}/training_data/{}".format(cwd, folder_name ), file_name)
        opened_file = open(file_path, 'w')
        opened_file.write(lyrics)
        opened_file.close()
    some_more_lyrics()


def some_more_lyrics():
    res = requests.get(url)
    data = bs4.BeautifulSoup(res.text, 'lxml')
    folder_name = data.find("div", class_="grid_6 suffix_6").h1.text
    try:
        os.mkdir("{}/training_data/{}".format(cwd, folder_name))
    except FileExistsError:
        None
    body = data.find('div',id ='popular')
    sub_body = body.find('tbody')
       # print(body.prettify())
    for file_names in sub_body.find_all('a',class_="title "):
        file_name =file_names.get('alt')
        link  = file_names.get("href")
        res1 = requests.get(link)
        soup = bs4.BeautifulSoup(res1.text, 'lxml')
        print(file_name)
        print(link)
        lyrics = " "
        for i in soup.select('.verse'):
            lyrics += i.text
        file_path = os.path.join("{}/training_data/{}".format(cwd, folder_name), file_name)
        opened_file = open(file_path, 'w')
        opened_file.write(lyrics)
        opened_file.close()

download_lyrics(url)
