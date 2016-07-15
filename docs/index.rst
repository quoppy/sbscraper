.. sbscraper documentation master file, created by
   sphinx-quickstart on Thu Jul 14 06:27:27 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

sbscraper
=========
Scrapes e-commerce websites for product information.


Configuration
-------------
The following environment variables control the behaviour of sbscraper.

.. envvar:: SBSCRAPER_SCRAPER_LABEL

   Tells the scraper how to extract, transform and load the data.

   **lazada-sqlite**
      Extract data from Lazada and load it into an SQLite database.

   **redmart-sqlite**
      Extract data from RedMart and load it into an SQLite database.

.. envvar:: SBSCRAPER_EXTRACTOR_URL

   Base URL of the data source to extract from, eg. http://www.lazada.sg.

.. envvar:: SBSCRAPER_EXTRACTOR_CATEGORIES

   Comma-separated list of categories to get product data for.

.. envvar:: SBSCRAPER_LOADER_URI

   URI of the data store to load the scraped product information to.


Running with envdir
-------------------
`envdir <http://envdir.readthedocs.io/>`_ can be used to set up the environment
variables. Some example environments can be found in the envs directory, and
will output a .db file into the current directory.


Contents
--------

.. toctree::
   :maxdepth: 3

   specifications
   todo
   modules



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

