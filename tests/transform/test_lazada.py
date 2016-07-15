# -*- coding: utf-8 -*-
"""Tests for LazadaProductTransformer."""

import os

import pytest

import bs4

from sbscraper.transform import lazada


@pytest.fixture
def html_path():
    return os.path.join(os.path.dirname(__file__), 'lazada.html')


@pytest.fixture
def transformer():
    return lazada.LazadaProductTransformer()


def test_transform(html_path, transformer):
    """Tests transforming Lazada data to a Product."""
    with open(html_path, 'rb') as html:
        datum = bs4.BeautifulSoup(html, 'lxml')
    product = transformer.transform(datum)
    assert product['title'] == 'Monkey 47 Gin 500ml'
    assert product['current_price'] == '90.00'
    assert product['currency'] == 'SGD'
