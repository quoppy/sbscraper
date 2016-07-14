# -*- coding: utf-8 -*-

from sbscraper import product
from sbscraper.transform import base


class RedMartProductTransformer(base.ProductTransformer):
    """Transforms RedMart data to :class:`Product` instances."""

    API_VERSION = 'v1.5.6'

    def get_currency(self, datum):
        # RedMart only deals in SGD.
        return 'SGD'

    def get_current_price(self, datum):
        pricing = datum.get('pricing', {})
        on_sale = bool(pricing.get('on_sale'))
        if on_sale:
            return pricing.get('promo_price')
        else:
            return pricing.get('price')

    def get_description(self, datum):
        return datum.get('desc')

    def get_original_price(self, datum):
        return datum.get('pricing', {}).get('price')

    def get_title(self, datum):
        return datum.get('title')