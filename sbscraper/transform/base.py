# -*- coding: utf-8 -*-
"""Transformers convert data from Extractors."""

import abc

from sbscraper import product


class Transformer(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_currency(self, datum):
        pass

    @abc.abstractmethod
    def get_current_price(self, datum):
        pass

    @abc.abstractmethod
    def get_description(self, datum):
        pass

    @abc.abstractmethod
    def get_original_price(self, datum):
        pass

    @abc.abstractmethod
    def get_title(self, datum):
        pass

    def transform(self, datum):
        return product.Product(
            title=self.get_title(datum),
            description=self.get_description(datum),
            currency=self.get_currency(datum),
            current_price=self.get_current_price(datum),
            original_price=self.get_original_price(datum)
        )