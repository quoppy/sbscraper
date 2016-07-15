# -*- coding: utf-8 -*-
"""Loaders put data into some data store."""

import abc
import logging


class Loader(object):
    """Base class for Loaders."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, uri):
        """Constructor.

        Arguments:
            uri (str): URI to access for this Loader, eg. a connection string.
        """
        self.logger = logging.getLogger(__name__)
        self.uri = uri

    @abc.abstractmethod
    def add(self, product):
        """Adds a product to the store.

        Arguments:
            product (:class:`~sbscraper.product.Product`): Product to add.
        """
        pass