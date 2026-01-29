#!/usr/bin/env python

from setuptools import setup

setup(
    name='PyFileMaker',
    version="3.4",
    description='Python Object Wrapper for FileMaker Server XML Interface',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=['FileMaker'],
    author='Klokan Petr Pridal, Pieter Claerhout, Marcin Kawa',
    author_email='klokan@klokan.cz, pieter@yellowduck.be, kawa.macin@gmail.com',
    url='https://github.com/aeguana/PyFileMaker',
    download_url='https://github.com/aeguana/PyFileMaker/releases',
    license='http://www.opensource.org/licenses/bsd-license.php',
    platforms = ['any'],
    packages=['PyFileMaker'],
    install_requires=['requests'],
    python_requires='>=3.10',
)
