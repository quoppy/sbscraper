# -*- coding: utf-8 -*-

import urlparse

from sbscraper.extract import base


class RedMartExtractor(base.Extractor):

    API_VERSION = 'v1.5.6'

    def __init__(self, url, categories=None, start_page=0, page_size=50):
        super(RedMartExtractor, self).__init__(url=url, categories=categories,
                                               start_page=start_page,
                                               page_size=page_size)

    def get_data(self, response):
        return response.data.get('products', [])

    def has_more(self, response):
        data = response.data
        if ('page' in data and
                'page_size' in data and
                'total' in data):
            page = data['page']
            page_size = data['page_size']
            total = data['total']
            return (page + 1) * page_size < total
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
