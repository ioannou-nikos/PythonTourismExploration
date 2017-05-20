from bs4 import BeautifulSoup
import re
import requests
import csv


class Crawler():
    def __init__(self):
        self.locations = ()
        self.phrases = ()
        self.results = ""
        self.period_starts = None
        self.period_ends = None
        self.url = None
        self.params = None

    def read_locations(self, filename='locations.txt'):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            self.locations = list(reader)

    def read_phrases(self, filename='phrases.txt'):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            self.phrases = list(reader)

    def set_url(self, url, params):
        self.url = url
        self.params = params

    def add_param(self, key, value):
        self.params[key] = value

    def get_count(self, phrase):
        pass

    def crawl(self):
        txt = "Location, Phrase, Results Count \n"
        for loc in self.locations:
            for keyword in self.phrases:
                if keyword != '':
                    if keyword.endswith(' '):
                        phrase = keyword + loc
                    else:
                        phrase = loc + keyword
                else:
                    phrase = loc
                cnt = self.get_count(phrase=phrase)
                txt += "%s, %s, %s \n" % (loc.strip(), keyword.strip(), cnt)
        self.results = txt

    def print_results(self, filename=None):
        if filename is None:
            print(self.results)
        else:
            with open(filename, 'w') as f:
                f.write(self.results)
                f.close()
