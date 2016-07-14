from setuptools import setup

from sbscraper import __version__


setup(
    name='sbscraper',
    version=__version__,
    packages=['sbscraper'],
    install_requires=[
        'beautifulsoup4',
        'futures',
        'lxml',
        'requests',
        'requests-futures'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
    entry_points={
        'console_scripts': [
            'sbscraper=sbscraper.executable:main'
        ]
    }
)