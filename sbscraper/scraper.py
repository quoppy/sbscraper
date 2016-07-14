# -*- coding: utf-8 -*-
"""Scrapers combine extractors, transformers and loaders."""

from sbscraper.extract.lazada import LazadaExtractor
from sbscraper.extract.redmart import RedMartExtractor
from sbscraper.load.sql import SQLiteLoader
from sbscraper.transform.lazada import LazadaProductTransformer
from sbscraper.transform.redmart import RedMartProductTransformer


class Scraper(object):
    """Default Scraper."""

    def __init__(self, extractor, transformer, loader):
        """Constructor.

        Arguments:
            extractor (:class:`Extractor`): Extractor used to get data.
            transformer (:class:`Transformer`): Converts data from an extractor
                for a loader.
            loader (:class:`Loader`): Puts data into a store.
        """
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self):
        """Runs the ETL process."""
        for item in self.extractor.extract():
            product = self.transformer.transform(item)
            self.loader.add(product)


class VersionedScraper(Scraper):
    """Scraper whose extractor and transformer work with a versioned API."""

    def __init__(self, extractor, transformer, loader):
        assert extractor.API_VERSION == transformer.API_VERSION
        super(VersionedScraper, self).__init__(extractor, transformer, loader)


LABELS = {
    'lazada-sqlite': (Scraper, LazadaExtractor, LazadaProductTransformer,
                      SQLiteLoader),
    'redmart-sqlite': (VersionedScraper, RedMartExtractor,
                       RedMartProductTransformer, SQLiteLoader)
}
