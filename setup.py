from setuptools import setup

from sbscraper import __version__


setup(name='sbscraper',
      version=__version__,
      packages=['sbscraper'],
      entry_points = {
            'console_scripts': ['sbscraper=sbscraper.executable:main'],
      })