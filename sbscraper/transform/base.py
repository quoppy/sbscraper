# -*- coding: utf-8 -*-
"""Transformers convert data from Extractors."""

import abc

from sbscraper import product


class Transformer(object):
    """Base class for Transformers."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_currency(self, datum):
        """Returns the currency for a product."""
        pass

    @abc.abstractmethod
    def get_current_price(self, datum):
        """Returns the current price for a product."""
        pass

    @abc.abstractmethod
    def get_description(self, datum):
        """Returns the description for a product."""
        pass

    @abc.abstractmethod
    def get_original_price(self, datum):
        """Returns the original price for a product."""
        pass

    @abc.abstractmethod
    def get_title(self, datum):
        """Returns the title for a product."""
        pass


class ProductTransformer(object):
    """Transformes data to a :class:`~sbscraper.product.Product`."""

    def transform(self, datum):
        """Converts unit of data to a :class:`~sbscraper.product.Product`.

        Arguments:
            datum: Unit of data to convert.

        Returns:
            :class:`~sbscraper.product.Product`: Product instance.
        """
        return product.Product(
            title=self.get_title(datum),
            description=self.get_description(datum),
            currency=self.get_currency(datum),
            current_price=self.get_current_price(datum),
            original_price=self.get_original_price(datum)
        )