from TwitterSearch import *
from bs4 import BeautifulSoup
import re
import requests
import facebook
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Searches():
    def __init__(self):
        pass

    @staticmethod
    def get_count_from_words(words):
        for word in words:
            if re.match(r"^[0-9\.,]*$", word):
                return word.replace(',', '').replace('.', '')

    @staticmethod
    def selenium_google(phrase_list, pre_directive='', post_directive=''):
        """
        Performs a google search for the specified phrases returning the results as text
        :param phrase_list: The list of search phrases
        :param pre_directive: Parameters in the form param: to prepend such as allintitle:
        :param post_directive: Paramaters in the form param: to append such as location:
        :return: The number of results found by google as text 
        """
        browser = webdriver.Firefox()  # Open a firefox instance
        txt = ""
        counter = 0
        for phrase in phrase_list:
            counter += 1
            if counter > 200:
                break
            phrase = phrase.strip()
            browser.get('http://www.google.com')  # Go to google home page
            elem = browser.find_element_by_id("lst-ib")  # Find the search box
            elem.send_keys(extra_directive + phrase + Keys.RETURN)
            time.sleep(10)
            try:
                res = browser.find_element_by_id("resultStats").text
                words = res.split(" ")
            except Exception:
                temp = "google," + phrase + ",0\n"
                print(temp)
                txt += temp
                continue
            temp = "google," + phrase + "," + Searches.get_count_from_words(words) + "\n"
            print(temp)
            txt += temp
        browser.quit()
        return txt

    @staticmethod
    def selenium_yahoo(phrase_list):
        browser = webdriver.Firefox()  # Open a firefox instance
        txt = ""
        counter = 0
        for phrase in phrase_list:
            counter += 1
            if counter > 200:
                break
            phrase = phrase.strip()
            browser.get('http://www.yahoo.com')  # Go to google home page
            elem = browser.find_element_by_id("uh-search-box")  # Find the search box
            elem.send_keys(phrase + Keys.RETURN)
            time.sleep(10)
            try:
                div = browser.find_element_by_class_name("compPagination")
                span_list = div.find_elements_by_tag_name("span")
                span = span_list[0]
                res = span.text
                words = res.split(" ")
            except Exception:
                temp = "yahoo," + phrase + ",0\n"
                print(temp)
                txt += temp
                continue
            temp = "yahoo," + phrase + "," + Searches.get_count_from_words(words) + "\n"
            print(temp)
            txt += temp
        browser.quit()
        return txt

    @staticmethod
    def selenium_bing(phrase_list):
        browser = webdriver.Firefox()  # Open a firefox instance
        txt = ""
        counter = 0
        for phrase in phrase_list:
            counter += 1
            if counter > 200:
                break
            phrase = phrase.strip()
            browser.get('http://www.bing.com')  # Go to google home page
            elem = browser.find_element_by_id("sb_form_q")  # Find the search box
            elem.send_keys(phrase + Keys.RETURN)
            time.sleep(10)
            try:
                div = browser.find_element_by_id("b_tween")
                span_list = div.find_elements_by_tag_name("span")
                span = span_list[0]
                res = span.text
                words = res.split(" ")
            except Exception:
                temp = "bing," + phrase + ",0\n"
                print(temp)
                txt += temp
                continue
            temp = "bing," + phrase + "," + Searches.get_count_from_words(words) + "\n"
            print(temp)
            txt += temp
        browser.quit()
        return txt

    @staticmethod
    def google(phrase):
        phrase = phrase.replace(' ', '+')
        #print("google", phrase)
        req = requests.get('http://www.google.com/search',
                           params={'q': '"' + phrase + '"'})
        #print(req.url)
        soup = BeautifulSoup(req.text, "html.parser")
        try:
            res = soup.find('div', {'id': 'resultStats'}).text
        except AttributeError as e:
            print("Google Problem : " + str(e))
            return 0
        #print(res)
        words = res.split(" ")
        for word in words:
            if re.match(r"^[0-9\.]*$", word):
                return word.replace(',', '').replace('.', '')
        return 0

    @staticmethod
    def bing(phrase):
        """ 
        This is the method that searches bing.com and returns the number of occurrences found
        """
        print("bing", phrase)
        req = requests.get('http://www.bing.com/search',
                           params={'q': '"' + phrase + '"', 'go': 'Search',
                                   'qs': 'n', 'form': 'QBRE', 'sp': ''})
        soup = BeautifulSoup(req.text, "html.parser")
        try:
            res = soup.find('div', {'id': 'b_tween'}).text
            print(res)
        except AttributeError:
            print("Bing Problem")
            return 0
        words = res.split(" ")
        for word in words:
            if re.match(r"^[0-9.,]*$", word):
                return word.replace(',', '').replace('.', '')
        return 0

    @staticmethod
    def tripadvisor(phrase):
        print("tripadvisor",phrase)
        req = requests.get()
        soup = BeautifulSoup(req.text, "html.parser")
        try:
            res = soup.find('div', {'class': 'totalContentCount'}).text
            print(res)
        except AttributeError:
            print("Trip Advisor Problem")
            return 0
        return 0

    @staticmethod
    def booking(phrase):
        print("booking", phrase)
        req = requests.get('https://www.booking.com/searchresults.html',
                           params={'dest_type': 'city',
                                   'dtdisc': '0',
                                   'group_adults': 2,
                                   'group_children': 0,
                                   'inac': 0,
                                   'index_postcard': 0,
                                   'label_click': 'undef',
                                   'mih': 0,
                                   'no_rooms': 1,
                                   'offset': 0,
                                   'postcard': 0,
                                   'room1': 'A%2CA',
                                   'sb_price_type': 'total',
                                   'src': 'index',
                                   'src_elem': 'ssb',
                                   'ss': '"' + phrase + '"',
                                   'ss_all': 0,
                                   'ssb': 'empty',
                                   'sshis': 0,
                                   'sxp_will_search_domestic_prediction_probability': 0.264652798125713})
        soup = BeautifulSoup(req.text, "html.parser")
        try:
            res = soup.find('h1', {'class': 'sorth1'}).text
            print(res)
        except AttributeError:
            print("Booking Problem")
            return 0
        words = res.split(" ")
        for word in words:
            if re.match(r"^[0-9.,]*$", word):
                return word.replace(',', '').replace('.', '')
        return 0

    @staticmethod
    def twitter(phrase):
        print("twitter", phrase)
        try:
            tso = TwitterSearchOrder()
            tso.set_keywords(phrase.split(' '))
            tso.set_language('en')
            tso.set_include_entities(False)

            ts = TwitterSearch(
                consumer_key='5fKb0oXnn188AbpHDckeAITgi',
                consumer_secret='KnMB211TgjmDC36oZihONayTHeIIftidwJc3u5Qgmu9PYWuHzi',
                access_token='30289135-xEYFN0uHif4RH03hYXp5W8BedcBFLpon0sIoOKJIz',
                access_token_secret='VRilm9GjJ6s3TmiOsb1YJXe4i5vY52VNMWPSYVGY3MJBC'
            )
            return sum(1 for t in ts.search_tweets_iterable(tso))
        except TwitterSearchException as e:
            print(e)
            return 0
        return 0

    @staticmethod
    def facebook(phrase):
        print("facebook", phrase)
        user_token = 'EAACEdEose0cBALwSwnypuPjZAQHAwe9hIWn4OBKXnZCEzzBI3JOiifxjZC5Or4v8lr95G4liiTcPfrhW71rj35VPHxZARHXUBSvIwBoZAz5wR3iRxlvF6ToqBmkrZBOUofRT8pihKTdjfpoEZCQ9Da1pWgEGtej7n5Ma1pmWAhhqBoPGLObQ51hMojonzj4eQkZD'
        sdk_version = '2.9'
        graph = facebook.GraphAPI(access_token=user_token, version=sdk_version)
        friends = graph.get_connections(id='me', connection_name='likes')['paging']
        for friend in friends:
            print(friend)
        return 0

    @staticmethod
    def youtube(phrase):
        print("youtube", phrase)
        phrase = phrase.strip().replace(' ', '+')
        req = requests.get('https://www.youtube.com/results',
                           params={'search_query': phrase})
        soup = BeautifulSoup(req.text, "html.parser")
        try:
            res = soup.find('p', {'class': 'num-results first-focus'}).text
            print(res)
        except AttributeError:
            print("youTube Problem")
            return 0
        words = res.split(" ")
        for word in words:
            if re.match(r"^[0-9.,]*$", word):
                return word.replace(',', '').replace('.', '')
        return 0
