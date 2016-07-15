# -*- coding: utf-8 -*-

from sbscraper.transform import base


class LazadaProductTransformer(base.ProductTransformer):
    """Transforms Lazada data to :class:`~sbscraper.product.Product`."""

    def get_currency(self, datum):
        currency = datum.find(itemprop='priceCurrency')
        if currency:
            return unicode(currency.get('content', '')) or None

    def get_current_price(self, datum):
        price = datum.find(itemprop='price')
        if price:
            return unicode(price.get('content', '')) or None

    def get_description(self, datum):
        description = datum.find(itemprop='description')
        if description:
            return '\n'.join(description.stripped_strings)

    def get_original_price(self, datum):
        price = datum.select('div#special_price_area span#price_box')
        if price:
            price = price[0]
            return unicode(price.get_text(strip=True))

    def get_title(self, datum):
        title = datum.find(itemprop='name')
        if title:
            return unicode(title.get_text(strip=True))
