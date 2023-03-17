import requests
from bs4 import BeautifulSoup


def getHTML(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    return soup
