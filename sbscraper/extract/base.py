# -*- coding: utf-8 -*-
"""Extractors get data from a web-based source."""

import abc
import logging

import requests


class Extractor(object):

    def __init__(self, url, categories=None, start_page=None, page_size=None):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.url = url
        self.categories = categories or []
        self.start_page = start_page
        self.page_size = page_size

    @abc.abstractmethod
    def get_products(self, response):
        pass

    @abc.abstractmethod
    def has_more(self, response):
        pass

    @abc.abstractmethod
    def request(self, category, page, page_size):
        pass

    def extract(self, start_page=None, page_size=None):
        page_size = page_size or self.page_size
        for category in self.categories:
            page = start_page or self.start_page
            while True:
                response = self.request(category, page, page_size)
                for product in self.get_products(response):
                    yield product
                if not self.has_more(response):
                    break
                page += 1