# -*- coding: utf-8 -*-

from sbscraper.extract.lazada import LazadaExtractor
from sbscraper.extract.redmart import RedMartExtractor
from sbscraper.load.sql import SQLiteLoader
from sbscraper.transform.lazada import LazadaProductTransformer
from sbscraper.transform.redmart import RedMartProductTransformer


class Scraper(object):

    def __init__(self, extractor, transformer, loader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self):
        for item in self.extractor.extract():
            product = self.transformer.transform(item)
            self.loader.add(product)


class VersionedScraper(Scraper):

    def __init__(self, extractor, transformer, loader):
        assert extractor.API_VERSION == transformer.API_VERSION
        super(VersionedScraper, self).__init__(extractor, transformer, loader)


def classes_from_label(label):
    labels = {
        'lazada-sqlite': [Scraper, LazadaExtractor, LazadaProductTransformer,
                          SQLiteLoader],
        'redmart-sqlite': [VersionedScraper, RedMartExtractor,
                           RedMartProductTransformer, SQLiteLoader]
    }
    return labels[label]