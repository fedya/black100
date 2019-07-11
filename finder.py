#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import json
import argparse
from bs4 import BeautifulSoup


def ll_request(book):
    try:
        search_headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.2171.95 Safari/537.36', 'Origin': 'https://www.livelib.ru',
                          'Upgrade-Insecure-Requests': '1', 'DNT': '1'}
        payload = {'btn_search': 'Искать', 'search[text]': '{}'.format(book)}
        print(payload)
        URL = 'https://www.livelib.ru/find'
        r = requests.post(url=URL,data=json.dumps(payload), headers=search_headers)
        page = r.content.decode('utf-8')
        print(page)
        soup = BeautifulSoup(page, 'html.parser')
        book_list = soup.find(
            'div', {'class': 'object-wrapper object-wrapper-outer object-edition'})
        template = '{prefix}{url}'.format
        PREFIX = 'https://www.livelib.ru'
        links = [template(prefix=PREFIX, url=e.get('href'), title=e.get('title'))
                 for e in book_list.find_all('a', href=True)]
        print(links[0])
    except: pass


ll_request('Стеклянные пчелы')
#ll_request('Рыцарь нищеты')
#ll_request('В стальных грозах')
#ll_request('Делалой М. Усы и юбки')
#ll_request('Витте С.Ю. Воспоминания, очерки, дневники, письма')
#ll_request('Жан-Пьер Руссо "Нездешняя гавань"')
#ll_request('Нестор Махно. Воспоминания')
