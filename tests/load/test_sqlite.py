# -*- coding: utf-8 -*-
"""Tests for SQLiteLoader."""

import decimal

import pytest

from sbscraper import escape
from sbscraper.product import Product
import sbscraper.load.sql


@pytest.fixture
def uri():
    """Returns a URI to an SQLite database."""
    return ':memory:'


@pytest.fixture
def loader(uri):
    """Returns a SQLiteLoader instance."""
    return sbscraper.load.sql.SQLiteLoader(uri)


def test_add(loader):
    """Tests adding a Product."""
    product = Product(title='Apple',
                      currency='SGD',
                      price='1.23')
    loader.add(product)

    with loader.connection:
        cursor = loader.connection.execute('SELECT details FROM products;')
    row = cursor.fetchone()
    assert escape.to_json(product) == row[0]