from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='python-fortniteapi-wrapper',
    version='1.0.0',
    description='A python Fortnite API wrapper that doesn\'t suck',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/LeagueRank/Fortnite-API',
    author='David Horn',
    author_email='david@leaguerank.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2'
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests'])
)