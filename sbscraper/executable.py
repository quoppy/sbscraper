#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import logging
import os
import sys

import sbscraper.scraper


PREFIX = 'SBSCRAPER'

EXTRACTOR_CATEGORIES = 'EXTRACTOR_CATEGORIES'
EXTRACTOR_URL = 'EXTRACTOR_URL'
LOADER_URI = 'LOADER_URI'
SCRAPER_LABEL = 'SCRAPER_LABEL'


def _getenv(key, default=None):
    key = "%s_%s" % (PREFIX, key)
    return os.getenv(key, default=default)


def main():
    logger = logging.getLogger(__name__)

    label = _getenv(SCRAPER_LABEL)
    (scraper, extractor, transformer,
     loader) = sbscraper.scraper.classes_from_label(label)

    extractor_url = _getenv(EXTRACTOR_URL)
    if not extractor_url:
        logger.error('no extractor URL set')
        return 1

    extractor_categories = _getenv(EXTRACTOR_CATEGORIES, '')
    categories = [category.strip()
                  for category in extractor_categories.split(',')]
    if not categories:
        logger.error('no extractor categories set')
        return 1

    loader_uri = _getenv(LOADER_URI)
    if not loader_uri:
        logger.error('no loader URI set')
        return 1

    extractor = extractor(extractor_url, categories)
    transformer = transformer()
    loader = loader(loader_uri)
    scraper = scraper(extractor, transformer, loader)
    scraper.run()


if __name__ == '__main__':
    sys.exit(main())