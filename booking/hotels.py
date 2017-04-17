from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities.FIREFOX
#caps["marionette"] = True
caps["binary"] = "/Applications/Firefox.app/Contents/MacOS/firefox"
browser = webdriver.Firefox(capabilities=caps)

browser.get('http://booking.com')
browser.find_element_by_id("ss").send_keys("veria, macedonia, Greece")
browser.find_element_by_css_selector(".-visible > li:nth-child(1)").click()
browser.find_element_by_css_selector(".sb-searchbox__button").submit()

names = browser.find_elements_by_css_selector("span.sr-hotel__name")
scores = browser.find_elements_by_css_selector("span.average.js--hp-scorecard-scoreval")
els = browser.find_elements_by_css_selector("span.score_from_number_of_reviews")

browser.find_element_by_css_selector(".paging-next").click()
names = names + browser.find_elements_by_css_selector("span.sr-hotel__name")
scores = scores + browser.find_elements_by_css_selector("span.average.js--hp-scorecard-scoreval")
els = els + browser.find_elements_by_css_selector("span.score_from_number_of_reviews")

for i in range(len(els)):
    print(names[i].text + ";" + scores[i].text + ";" + els[i].text)


