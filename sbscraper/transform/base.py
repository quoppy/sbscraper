# -*- coding: utf-8 -*-
"""Transformers convert data from Extractors."""

import abc

from sbscraper import product


class ProductTransformer(object):
    """Base class for Transformers that convert data to a :class:`Product`."""

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

    def transform(self, datum):
        """Converts unit of data to a :class:`Product`.

        Arguments:
            datum: Unit of data to convert.

        Returns:
            :class:`Product`: Product instance.
        """
        return product.Product(
            title=self.get_title(datum),
            description=self.get_description(datum),
            currency=self.get_currency(datum),
            current_price=self.get_current_price(datum),
            original_price=self.get_original_price(datum)
        )