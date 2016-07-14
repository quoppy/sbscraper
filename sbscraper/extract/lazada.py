# -*- coding: utf-8 -*-

import copy
import urlparse

import bs4
import concurrent.futures
import requests_futures.sessions

from sbscraper.extract import base


class LazadaExtractor(base.Extractor):
    """Extracts data from Lazada.

    Lazada product data can be found in each product's page with some microdata.
    """

    def __init__(self, url, categories=None, start_page=1, page_size=50,
                 max_workers=2):
        """Constructor.

        Arguments:
            url (str): Base URL for the data source.
            categories: Iterable of categories to extract.
            start_page (int): Page to start from.
            page_size (int): Size of each page to extract.
            max_workers (int): Number of background workers.
        """
        super(LazadaExtractor, self).__init__(url=url, categories=categories,
                                              start_page=start_page,
                                              page_size=page_size)
        # Replace the session with an asynchronous one.
        self.session = requests_futures.sessions.FuturesSession(
            session=self.session, max_workers=max_workers)

    def get_data(self, response):
        # First find all products from the listing.
        products = response.data.find_all('div', class_='product-card')
        futures = []
        # For each product, request its full product page in the background.
        for product in products:
            product_url = product.get('data-original')
            if not product_url:
                continue
            product_url = urlparse.urljoin(self.url, product_url)
            futures.append(self.session.get(product_url,
                                            background_callback=_add_soup))
        # Yield over completed requests as they finish since order is not
        # important.
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            detail = result.data.find('div', itemscope=True,
                                      itemtype='http://schema.org/Product')
            datum = copy.copy(detail)
            yield datum

    def has_more(self, response):
        # Checks the page links to see if the last page is the one currently
        # selected. If so, there is no more data.
        pages = response.data.select('span.pages > a')
        if pages:
            last_page = pages[-1]
            return 'active_1' not in last_page.get('class', [])
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
    # Callback for BeautifulSoup to parse the response in the background thread.
    response.data = bs4.BeautifulSoup(response.text, 'lxml')