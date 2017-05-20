import argparse
import re
import requests
from bs4 import BeautifulSoup

locations = ('thessaloniki',)
keywords = ('',)


def get_count_bing(phrase):
    """
    Get the search count from Bing
    """
    print(phrase)
    req = requests.get('http://www.bing.com/search',
                       params={'q': '"' + phrase + '"', 'go': 'Search',
                               'qs': 'n', 'form': 'QBRE', 'sp': ''})
    soup = BeautifulSoup(req.text, "html.parser")
    try:
        res = soup.find('div', {'id':'b_tween'}).text
        print(res)
    except AttributeError:
        print("Bing Problem")
        return 0
    words = res.split(" ")
    for word in words:
        if re.match(r"^[0-9.,]*$", word):
            return word.replace(',', '').replace('.', '')
    return 0


def get_count_google(phrase):
    """
    Get the search count from Google
    """
    req = requests.get('http://www.google.com/search',
                       params={'q': '"' + phrase + '"', "tbs":"li:1"})
    print(req.url)
    soup = BeautifulSoup(req.text, "html.parser")
    try:
        res = soup.find('div', {'id': 'resultStats'}).text
    except AttributeError:
        print("MALAKIA")
    # print(res)
    words = res.split(" ")
    for word in words:
        if re.match(r"^[0-9\.]*$", word):
            return word
    return 0


def get_count_from_args():
    """
    Get the search count as a command prompt argument
    """
    parser = argparse.ArgumentParser(description='Get Google Count.')
    parser.add_argument('phrase', help='phrase  to count')
    args = parser.parse_args()

    req = requests.get('http://www.google.com/search',
                       params={'q': '"' + args.word+'"', "tbs":"li:1"})
    soup = BeautifulSoup(req.text, "html.parser")
    print(soup.find('div', {'id':'resultStats'}).text)


def main(target=None, source='google'):
    """
    The main function
    """
    txt = "Location, Phrase, Results Count \n"
    for loc in locations:
        for keyword in keywords:
            if keyword != '':
                if keyword.endswith(' '):
                    phrase = keyword + loc
                else:
                    phrase = loc + keyword
            else:
                phrase = loc
            cnt = 0
            if source == 'bing':
                cnt = get_count_bing(phrase)
            else:
                cnt = get_count_google(phrase)
            txt += "%s, %s, %s \n" % (loc.strip(), keyword.strip(), cnt)
    if target is None:
        print(txt)
    else:
        fout = open(target, "w")
        fout.write(txt)
        fout.close()


if __name__ == "__main__":
    main("results.csv", source='google')
