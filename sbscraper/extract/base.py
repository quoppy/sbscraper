# -*- coding: utf-8 -*-
"""Extractors get data from a web-based source."""

import abc
import logging

import requests


class Extractor(object):
    """Base class for Extractors."""

    def __init__(self, url, categories=None, start_page=None, page_size=None):
        """Constructor.

        Arguments:
            url (str): Base URL for the data source.
            categories: Iterable of categories to extract.
            start_page (int): Page to start from.
            page_size (int): Size of each page to extract.
        """
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.url = url
        self.categories = categories or []
        self.start_page = start_page
        self.page_size = page_size

    @abc.abstractmethod
    def get_data(self, response):
        """Gets data from a request response.

        Arguments:
            response (:class:`requests.Response`): Response from data source.

        Yields:
            Unit of data suitable for passing to a :class:`Transformer`.
        """
        pass

    @abc.abstractmethod
    def has_more(self, response):
        """Indicates if there is more data available after the current response.

        Arguments:
            response (:class:`requests.Response`): Response from data source.

        Returns:
            bool: True if there is more data available to request.
        """
        pass

    @abc.abstractmethod
    def request(self, category, page, page_size):
        """Sends a HTTP request for data.

        Arguments:
            category (str): Category to request data for.
            page (int): Page to request.
            page_size (int): Size of page.

        Returns:
            :class:`requests.Response`: Response from data source.
        """
        pass

    def extract(self, start_page=None, page_size=None):
        """Extracts data until no more is available.

        Arguments:
            start_page (int): Page to start from. Defaults to
                :attr:`start_page`.
            page_size (int): Size of each page. Defaults to :attr:`page_size`.

        Yields:
            Data for a product.
        """
        page_size = page_size or self.page_size
        self.logger.debug("Extractor page size: %s", page_size)
        for category in self.categories:
            page = start_page or self.start_page
            self.logger.debug("Extracting category '%s' from page '%s'",
                              category, page)
            while True:
                response = self.request(category, page, page_size)
                self.logger.debug("Extracting from '%s'", response.url)
                for datum in self.get_data(response):
                    yield datum
                if not self.has_more(response):
                    self.logger.debug('No more data available')
                    break
                page += 1