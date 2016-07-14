# -*- coding: utf-8 -*-
"""Serialisation and escape-related functions."""

import json

from .product import Product


PRODUCT_TYPE = '__product__'


def product_default(item):
    if isinstance(item, Product):
        result = dict(item)
        result[PRODUCT_TYPE] = True
        return result
    raise TypeError("object %s cannot be converted to JSON" % item)


def product_object_hook(mapping):
    if PRODUCT_TYPE in mapping and mapping[PRODUCT_TYPE]:
        del mapping[PRODUCT_TYPE]
        return Product(**mapping)
    return mapping


def from_json(value, object_hook=product_object_hook, **kwargs):
    return json.loads(value, object_hook=object_hook, **kwargs)


def to_json(item, default=product_default, **kwargs):
    return json.dumps(item, default=default, **kwargs)