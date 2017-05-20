import requests
import re
from bs4 import BeautifulSoup
from crawler import Crawler


class CGoogle(Crawler):
    def __init__(self):
        Crawler.__init__(self)
        self.url = 'http://www.google.com/search'
        self.params = {"tbs": "li:1"}

    def get_count(self, phrase):
        self.params['q'] = "'" + phrase + "'"
        req = requests.get(self.url, self.params)
        soup = BeautifulSoup(req.text, "html.parser")
        try:
            res = soup.find('div', {'id': 'b_tween'}).text
            print(res)
        except AttributeError:
            print("Bing Problem")
            return 0
        words = res.split(" ")
        for word in words:
            if re.match(r'^[0-9.,]*$', word):
                return word.replace(',', '').replace('.', '')
        return 0

