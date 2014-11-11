#!/usr/bin/env python

from setuptools import setup
from PyFileMaker import __version__, __doc__

setup(name='PyFileMaker',
      version=__version__,
      description='Python Object Wrapper for FileMaker Server XML Interface',
      long_description=__doc__,
      author='Klokan Petr Pridal, Pieter Claerhout',
      author_email='klokan@klokan.cz, pieter@yellowduck.be',
      license='http://www.opensource.org/licenses/bsd-license.php',
      url='http://code.google.com/p/pyfilemaker/',
      platforms = ["any"],
      packages=['PyFileMaker']
     )
