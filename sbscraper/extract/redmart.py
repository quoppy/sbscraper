# -*- coding: utf-8 -*-

import urlparse

from sbscraper.extract import base


class RedMartExtractor(base.Extractor):
    """Extracts data from RedMart.

    RedMart has a versioned REST API that returns JSON similar to the form::

        {
            'products': [
                {
                    'description': 'Some product.',
                    'title': 'Product title.'
                }
            ],
            'page': 1,
            'total': 12
        }
    """

    # RedMart uses a versioned REST API.
    API_VERSION = 'v1.5.6'

    def __init__(self, url, categories=None, start_page=0, page_size=50):
        super(RedMartExtractor, self).__init__(url=url, categories=categories,
                                               start_page=start_page,
                                               page_size=page_size)

    def get_data(self, response):
        for datum in response.data.get('products', []):
            yield datum

    def has_more(self, response):
        data = response.data
        if 'page' in data and 'total' in data:
            page = data['page']
            total = data['total']
            return (page + 1) * self.page_size < total
        return False

    def request(self, category, page, page_size):
        url = urlparse.urljoin(self.url, "%s/catalog/search" % self.API_VERSION)
        parameters = {
            'category': category,
            'page': page,
            'pageSize': page_size
        }
        response = self.session.get(url, params=parameters)
        response.data = response.json()
        return response
