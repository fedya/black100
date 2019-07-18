#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import json
import argparse
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.2171.95 Safari/537.36'}


def parse_book_id(url):
    print(url)
    resp = requests.get(url, headers=headers)
    if resp.status_code == 404:
        print('requested page [{}] not found'.format(url))
    if resp.status_code == 200:
        page = resp.content
        soup = BeautifulSoup(page, 'html.parser')
#        print(soup.prettify())
        # <div data-book="1002813399" id="lead-button" style="display:none;clear: both;">
        book_list = soup.find('div', {'class': 'book-right-data'})
#        <input id="sources-edition-id" type="hidden" value="1002813399"/>
        book_id = soup.find('input', {'id': 'sources-edition-id'}).get('value')
#        print(book_id)
#        print(book_list.prettify())
#            <span id="current-rating-1002813399">
#     <span title="Рейтинг 4.085 (73  читателя, рейтинг ожидания 0.000)">
        api_key = re.search('apikey=(\w+)', page.decode('ISO-8859-1'))
        print(api_key.group(1))
#        book_rating = soup.find('span')
        book_rating = soup.select_one('span.rating-book > span >  span')
#        print(book_rating['title'])
        print('book id: [{}] rating: [{}]'.format(
            book_id, book_rating['title']))
        return api_key.group(1), book_id, book_rating['title']


def parse_concrete_book(url):
    api_key, book_id, book_rating = parse_book_id(url)
    url = 'https://www.pricelib.ru/api/bookprice?callback=plcallback&api_key={}&edition_id={}'.format(
        api_key, book_id)
    resp = requests.get(url, headers=headers)
    if resp.status_code == 404:
        print('requested page [{}] not found'.format(url))
    if resp.status_code == 200:
        page = resp.content.decode('utf-8')
        # b'plcallback(\'
        # \')'
        # convert jsonm to json with simple split
        cleanup = page.replace("plcallback('", "").replace("')", "")
#        print(cleanup)
        book_prices = json.loads(cleanup)
        # book is available and it is paper
        a = list(filter(lambda x: x['is_available'] ==
                        "1" and x['type'] == 'paper', book_prices['data']))
#        print(json.dumps(a))
        for json_dict in a:
            print('{} {}'.format(
                json_dict['shop_title'], json_dict['price_discount']))
#            print("%s, цена %s " % (json_dict['shop_title'], json_dict['price_discount']))

#        print(book_prices)
#        print(json.dumps(book_prices, indent=4, sort_keys=True))
# def livelib_finder(book):


def ll_request(book):
    try:
        search_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
                          'Origin': 'https://www.livelib.ru',
                          'Upgrade-Insecure-Requests': '1', 'DNT': '1',
                          'Content-Type': 'application/x-www-form-urlencoded',
                          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'}

        payload = {'btn_search': 'Искать', 'search[text]': '{}'.format(book)}
        URL = 'https://www.livelib.ru/find'
        r = requests.post(url=URL, data=json.dumps(
            payload), headers=search_headers)
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
        return links[0]
    except:
        pass


# parse_book_id("https://www.livelib.ru/book/1002813399-geliopol-ernst-yunger")
#parse_concrete_book('e63c683a3cd6a4c41e82dc4b718e0ff8', '1002813399')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--book', help='book to check')
    parser.add_argument('--file', help='book list')
    args = parser.parse_args()
    if args.book is not None:
        #        parse_book_id(args.book)
        parse_concrete_book(args.book)
    if args.file is not None:
        with open(args.file) as file:
            for book in file:
                #print(book)
                ll_request(book)
