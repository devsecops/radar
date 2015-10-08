#!/usr/bin/env python
from distutils.core import setup
#from setuptools import setup, find_packages
from glob import glob

setup(
    name="securitychecker",
    version="0.2",
    author="test",
    author_email='mikedix@amazon.com',
    license='TBD',
    description='allows you to validate AWS architecture for security and compliance rules',
    packages=['securitychecker'],
    include_package_data=True,
    package_data={'securitychecker': ['data/UnitTests/*','data/compliance/*']},
    install_requires=['pyyaml', 'boto' ],
    scripts=['securitychecker/securitychecker'],
)
