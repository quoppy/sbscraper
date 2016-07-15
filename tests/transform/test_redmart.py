# -*- coding: utf-8 -*-
"""Tests for RedMartProductTransformer."""

import json
import os

import pytest

from sbscraper.transform import redmart


@pytest.fixture
def json_path():
    return os.path.join(os.path.dirname(__file__), 'redmart.json')


@pytest.fixture
def transformer():
    return redmart.RedMartProductTransformer()


def test_transform(json_path, transformer):
    """Tests transforming RedMart data to a Product."""
    with open(json_path, 'rb') as source:
        datum = json.load(source)
    product = transformer.transform(datum)
    assert product['title'] == 'Hakushika Yamadanishiki'
    assert product['current_price'] == '14.7'
    assert product['original_price'] == '14.7'
    assert product['currency'] == 'SGD'