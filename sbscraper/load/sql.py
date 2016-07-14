# -*- coding: utf-8 -*-
"""SQL-based Loaders."""

import sqlite3

from sbscraper import escape
from sbscraper.load import base


_CREATE_PRODUCTS_TABLE_SQLITE = """
CREATE TABLE products (
    details text
);
"""

_INSERT_PRODUCTS_TABLE_SQLITE = """
INSERT INTO products
VALUES (:details);
"""


class SQLiteLoader(base.Loader):
    """Loads product data into an SQLite database."""

    def __init__(self, uri):
        super(SQLiteLoader, self).__init__(uri)
        self.connection = sqlite3.connect(self.uri)
        self._create_schema()

    def add(self, product):
        """Adds a :class:`Product` to an SQLite database.

        Arguments:
            product (:class:`Product`): The :class:`Product` instance to add.
                Must be convertable to JSON.
        """
        as_text = escape.to_json(product)
        try:
            with self.connection:
                self.connection.execute(_INSERT_PRODUCTS_TABLE_SQLITE,
                                        {'details': as_text})
        except sqlite3.Error as error:
            self.logger.error("Error inserting row: %s", error)
            raise

    def _create_schema(self):
        """Creates the schema to store product data."""
        self.logger.debug("Creating table 'products'")
        try:
            self.connection.execute(_CREATE_PRODUCTS_TABLE_SQLITE)
        except sqlite3.OperationalError:
            self.logger.debug("Table 'products' already exists")
        else:
            self.logger.info("Created table 'products'")
