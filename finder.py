#!/usr/bin/env python
import re
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium import webdriver
from bs4 import BeautifulSoup


def ll_request(book):
    driver = webdriver.Chrome('/usr/bin/chromedriver')
    el = WebDriverWait(driver, 15)

    payload = {'btn_search': 'Искать', 'search[text]': '{}'.format(book)}
    URL = 'https://www.livelib.ru/find'
    r = requests.post(url=URL,data=json.dumps(payload), headers=search_headers)
    page = r.content.decode('utf-8')
    soup = BeautifulSoup(page, 'html.parser')
    book_list = soup.find(
        'div', {'class': 'object-wrapper object-wrapper-outer object-edition'})
    template = '{prefix}{url}'.format
    PREFIX = 'https://www.livelib.ru'
    links = [template(prefix=PREFIX, url=e.get('href'), title=e.get('title'))
             for e in book_list.find_all('a', href=True)]
    print(links[0])


ll_request('Стеклянные пчелы')
