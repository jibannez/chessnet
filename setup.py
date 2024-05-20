# -*- coding: utf-8 -*-
# from distutils.core import setup
from setuptools import setup

setup(
    name='chessnet',
    version='0.3.0',
    author='Jorge Ibáñez Gijón, Gonzalo S. Nido, & Alberto Pascual',
    author_email='jorge.ibannez@uam.es',
    packages=['chessnet'],
    zip_safe=False,
    scripts=['scripts/pgn2epd.py'],
    url='https://git.kabe.es/chessnet',
    license='LICENSE.txt',
    description='chessnet library',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy >= 1.8.1",
        "numba >= 0.35.0",
        "python-chess >= 0.22.1"
    ],
)
