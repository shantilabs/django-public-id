#!/usr/bin/env python
import os
import sys

from setuptools import setup, find_packages

version = __import__('public_id').__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()


setup(
    name='django-public-id',
    description='Long non-incremental IDs for public links. Essentially a compact form of UUID (22 bytes for 128-bit value)',
    version=version,
    author='Maxim Oransky',
    author_email='maxim.oransky@gmail.com',
    maintainer='Dmitrii Gerasimenko',
    maintainer_email='kiddima@gmail.com',
    url='https://github.com/shantilabs/django-public-id',
    packages=['public_id'],
    zip_safe=True,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
    ],
)
