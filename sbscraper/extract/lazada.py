# -*- coding: utf-8 -*-

import copy
import urlparse

import bs4
import concurrent.futures
import requests_futures.sessions

from sbscraper.extract import base


class LazadaExtractor(base.Extractor):

    def __init__(self, url, categories=None, start_page=1, page_size=50,
                 max_workers=2):
        super(LazadaExtractor, self).__init__(url=url, categories=categories,
                                              start_page=start_page,
                                              page_size=page_size)
        self.session = requests_futures.sessions.FuturesSession(
            session=self.session, max_workers=max_workers)

    def get_data(self, response):
        products = response.data.find_all('div', class_='product-card')
        futures = []
        for product in products:
            product_url = product.get('data-original')
            if not product_url:
                continue
            product_url = urlparse.urljoin(self.url, product_url)
            futures.append(self.session.get(product_url,
                                            background_callback=_add_soup))
        for result in concurrent.futures.as_completed(futures):
            detail = result.data.find('div', itemscope=True,
                                      itemtype='http://schema.org/Product')
            datum = copy.copy(detail)
            yield datum

    def has_more(self, response):
        pages = response.data.select('span.pages > a')
        if pages:
            last_page = pages[-1]
            return 'active_1' in last_page['class']
        return False

    def request(self, category, page, page_size):
        url = urlparse.urljoin(self.url, category)
        parameters = {
            'page': page,
            'itemsperpage': page_size
        }
        future = self.session.get(url, params=parameters,
                                  background_callback=_add_soup)
        response = future.result()
        return response


def _add_soup(session, response):
    response.data = bs4.BeautifulSoup(response.text, 'lxml')