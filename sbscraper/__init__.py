# -*- coding: utf-8 -*-
"""Scrapes websites for product information."""

__version__ = '0.0.1'


# Set NullHandler to avoid handler-related warnings.
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())