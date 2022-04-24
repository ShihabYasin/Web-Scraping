import requests
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

############################################################
ua = UserAgent ()
ua_dict = {"User-Agent": ua.random}
selenium_chrome_driver_path = r"./chromedriver"

opts = Options ()
opts.add_argument ("--window-size=2560,1440")  # screen size
opts.add_experimental_option ("useAutomationExtension", False)
opts.add_experimental_option ("excludeSwitches", ["enable-automation"])
opts.add_argument ("--remote-debugging-port=9222")
opts.add_argument ('--user-data-dir=./')
opts.add_argument ('headless')
opts.add_argument ('--no-sandbox')
opts.add_argument ('--disable-dev-shm-usage')


############################################################
def connect():
    try:
        url = "http://google.com"
        payload = {}
        headers = {
            'Cookie': 'NID=511=oyARvm_4awkMlvKjiVnvwxZjhyDdn1XzW6AMcbzU4rL8v0tDEueRHnv9lc-RU9QSgTxZH8E_U5Zy5imYVCa2RtLcabPJwrJ6bHeymzFU-hSreKPUx54E-Jieq_fzl3cxTdJsMfwlQ6QwFa5bypZW0OFeN509n8XTQDpzjp-nRDU'
            }

        response = requests.request ("GET", url, headers=headers, data=payload)
        return True
    except:
        return False


def get_text_from_page_url(start_url):
    text = []
    try:
        r = requests.get (start_url)
        soup = BeautifulSoup (r.content, 'html5lib')
        mydivs = soup.find_all ("div", attrs={"class": "story-element story-element-text"})
        for div in mydivs:
            text.append (div.getText ("div"))
    except Exception as e:
        pass

    return text


def get_driver(url=base_url, implicit_delay_seconds=3, options=opts,
               selenium_chrome_driver_path=selenium_chrome_driver_path):
    print (url, file=open ('all_links.txt', 'a'))
    caps = DesiredCapabilities.CHROME
    driver = webdriver.Chrome (executable_path=selenium_chrome_driver_path, desired_capabilities=caps, options=options)
    driver.maximize_window ()
    driver.implicitly_wait (implicit_delay_seconds)

    try:
        driver.get (url=url)
        return driver
    except Exception as e:
        driver.quit ()
        print (f" A: Loading Problem: {url}")
        print (url, file=open ('url_cant_reach.txt', 'a'))
        return None


def get_all_links_from_page_url(url, scrolling_button_text, include_pattern, exclude_pattern, SCROLL_COUNT, SCROLL_PAUSE_TIME,
                                implicit_delay_seconds, options,
                                base_url, selenium_chrome_driver_path):
    '''

    :param url:
    :param include_pattern: Pattern to follow
    :param exclude_pattern: Pattern not to follow
    :param SCROLL_COUNT: Number of scrolling to load more news
    :param SCROLL_PAUSE_TIME: After scrolling time delay to load elements
    :param implicit_delay_seconds: DOM element loading delay
    :param options: Driver options
    :param base_url: Target domain site url
    :param selenium_chrome_driver_path:
    :return:
    '''

    # Check internet connection .
    print (f'   ==>>> Data Collection start: {url}')
    while True:
        if connect ():
            break

    driver = get_driver (url=url)

    cnt = 0
    while driver is None:
        time.sleep (SCROLL_PAUSE_TIME * 2)
        driver = get_driver (url=url)
        cnt += 1
        if cnt == 6:
            break

    href_set = set ()
    if driver is None:
        print (url, file=open ('url_cant_reach.txt', 'a'))
        print (f'   ==>>> URL NOT REACHABLE: {url}')
        return list (href_set)
    try:
        body_elem = WebDriverWait (driver, SCROLL_PAUSE_TIME * 20).until (EC.presence_of_element_located ((By.TAG_NAME, 'body')))
    except TimeoutException:
        print (f"B: Loading Problem: {url}")
        print (url, file=open ('url_cant_reach.txt', 'a'))
        try:
            driver.close ()
        except Exception as e:
            print (33, e)
        try:
            driver.quit ()
        except Exception as e:
            print (44, e)
        return list (href_set)

    last_height = driver.execute_script ("return document.body.scrollHeight")  # Get scroll height
    new_height = last_height

    for i in range (SCROLL_COUNT):  # scroll down SCROLL_COUNT of times
        ActionChains (driver).send_keys (Keys.END).perform ()
        # print ('ScrolledCount: ', i)
        time.sleep (SCROLL_PAUSE_TIME * 5)  # Wait to load page

        try:
            btn = driver.find_element_by_xpath (f"//*[text()={scrolling_button_text}]")  # Click on btn scrolling_button_text if exists
            if btn:
                btn.click ()
                # print ('আরও  clicked....')
                time.sleep (SCROLL_PAUSE_TIME)  # Wait to load page
        except Exception as e:
            pass
            # print (1, e)

        try:
            new_height = driver.execute_script ("return document.body.scrollHeight")  # Calculate new scroll height and compare with last scroll height
        except Exception as e:
            print (url, file=open ('url_cant_reach.txt', 'a'))
            print (f'2:   ==>>> URL NOT REACHABLE: {url}')
            try:
                driver.close ()
            except Exception as e:
                print (333, e)
            try:
                driver.quit ()
            except Exception as e:
                print (444, e)
            return list (href_set)

        if new_height == last_height:
            break
        last_height = new_height

    try:
        soup = BeautifulSoup (driver.page_source, 'html.parser')
    except Exception as e:
        print (url, file=open ('url_cant_reach.txt', 'a'))
        print (f'3:   ==>>> URL NOT REACHABLE: {url}')
        try:
            driver.close ()
        except Exception as e:
            print (3300, e)
        try:
            driver.quit ()
        except Exception as e:
            print (4400, e)
        return list (href_set)

    href_tags = soup.find_all ('a', recursive=True)
    for ht in href_tags:
        tmp_lnk = ht.get ('href')

        if tmp_lnk is not None and any (x in tmp_lnk for x in include_pattern):
            if tmp_lnk.startswith (tuple (exclude_pattern)):
                continue
            elif tmp_lnk[0] == '/':
                href_set.add (base_url[:-1] + tmp_lnk)
            elif not tmp_lnk.startswith (("http", "www.")):
                href_set.add (base_url + tmp_lnk)
            else:
                href_set.add (tmp_lnk)
        else:
            continue

    try:
        driver.close ()
    except Exception as e:
        print (3, e)
    try:
        driver.quit ()
    except Exception as e:
        print (4, e)
    print (f'   ==>>> Data Collection  end: {url}')
    print (url, file=open ('texturl_reached.txt', 'a'))
    return list (href_set)


if __name__ == '__main__':
    base_url = "https://www.domaintoscrap.com/"
    include_patterns = ["domaintoscrap.com"]
    exclude_patterns = ["en."]  # exclude subdomain if need
    scrolling_button_text = 'Next'

    get_all_links_from_page_url (url=base_url, scrolling_button_text=scrolling_button_text, include_pattern=include_patterns, exclude_pattern=exclude_patterns, SCROLL_COUNT=5, SCROLL_PAUSE_TIME=1,
                                 implicit_delay_seconds=3, options=opts,
                                 base_url=base_url,
                                 selenium_chrome_driver_path=selenium_chrome_driver_path)
