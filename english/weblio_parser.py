# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

def parse(word):
    res = requests.get("http://ejje.weblio.jp/content/{}".format(word))
    soup = BeautifulSoup(res.text, "lxml")
    return {
        "word": soup.find("title").text.replace("の意味 - 英和辞典 Weblio辞書", "")
        , "meaning": soup.find("div", {"class": "summaryM"}).text.replace("主な意味", "")
    }