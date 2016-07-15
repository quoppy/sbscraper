#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Console script."""

import logging
import os
import sys

import sbscraper
import sbscraper.scraper


# Environment variables.
PREFIX = 'SBSCRAPER'
EXTRACTOR_CATEGORIES = 'EXTRACTOR_CATEGORIES'
EXTRACTOR_URL = 'EXTRACTOR_URL'
LOADER_URI = 'LOADER_URI'
SCRAPER_LABEL = 'SCRAPER_LABEL'

LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'
LOG_DATE_FORMAT = '%y%m%d %H:%M:%S'


def get_setting(key, default=None):
    """Gets the value of a setting from the environment.

    Arguments:
        key (str): Name of setting.

    Returns:
        str: Value of setting.

    Raises:
        KeyError: Setting does not exist in the environment.
    """
    key = "%s_%s" % (PREFIX, key)
    return os.environ[key]


def configure_stream_logging(logger):
    """Configures logging to output to stderr.

    Arguments:
        logger (:class:`logging.Logger`): Logger to configure.
    """
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)



def main():
    """Runs the Scraper based on the environment.

    Returns:
        int: Exit status.
    """
    configure_stream_logging(logging.getLogger(sbscraper.__name__))

    logger = logging.getLogger(__name__)

    try:
        label = get_setting(SCRAPER_LABEL)
    except KeyError:
        logger.error('no scraper label set')
        return 1
    try:
        (scraper, extractor, transformer,
         loader) = sbscraper.scraper.LABELS[label]
    except KeyError:
        logger.error("invalid label: %s", label)
        return 1

    try:
        extractor_url = get_setting(EXTRACTOR_URL)
    except KeyError:
        logger.error('no extractor URL set')
        return 1

    try:
        extractor_categories = get_setting(EXTRACTOR_CATEGORIES)
    except KeyError:
        logger.error('no extractor categories set')
        return 1
    categories = [category.strip()
                  for category in extractor_categories.split(',')]
    if not categories:
        logger.error("no extractor categories found: %s", categories)
        return 1

    try:
        loader_uri = get_setting(LOADER_URI)
    except KeyError:
        logger.error('no loader URI set')
        return 1

    extractor = extractor(extractor_url, categories)
    transformer = transformer()
    loader = loader(loader_uri)
    scraper = scraper(extractor, transformer, loader)

    logger.info('Starting scraping process')
    scraper.run()
    logger.info('Done scraping')


if __name__ == '__main__':
    sys.exit(main())