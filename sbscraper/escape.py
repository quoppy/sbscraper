# -*- coding: utf-8 -*-
"""Serialisation and escape-related functions."""

import decimal
import json

from sbscraper import product


PRODUCT_TYPE = '__product__'


def product_default(item):
    """Hook for converting Python object to JSON."""
    if isinstance(item, product.Product):
        result = dict(item)
        result[PRODUCT_TYPE] = True
        return result
    raise TypeError("object %s cannot be converted to JSON" % item)


def product_object_hook(mapping):
    """Hook for converting JSON to Python object."""
    if PRODUCT_TYPE in mapping and mapping[PRODUCT_TYPE]:
        del mapping[PRODUCT_TYPE]
        return product.Product(**mapping)
    return mapping


def from_json(value, object_hook=product_object_hook,
              parse_float=decimal.Decimal, **kwargs):
    """Converts JSON to Python.

    All arguments are passed to :func:`json.loads`.

    Returns:
        object: Python object converted from JSON.
    """
    return json.loads(value, object_hook=object_hook, parse_float=parse_float,
                      **kwargs)


def to_json(item, default=product_default, **kwargs):
    """Convert Python to JSON.

    All arguments are passed to :func:`json.dumps`.

    Returns:
        str: JSON value.
    """
    return json.dumps(item, default=default, **kwargs)