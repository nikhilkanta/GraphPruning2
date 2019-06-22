#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for GraphPruning2
You can install GraphPruning2 with
python setup.py install
"""
from glob import glob
import os
import sys
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

from setuptools import setup

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")

if sys.version_info[:2] < (3, 5):
    error = "GraphPruning2 requires Python 3.5 or later (%d.%d detected)."

# Write the version information.
sys.path.insert(0, 'graphpruning2')
#import release
#version = release.write_versionfile()
sys.path.pop(0)

packages = ["graphpruning2"]

install_requires = ['networkx>=2.2', 'numpy>=1.16.2', 'statsmodels>=0.9.0']


if __name__ == "__main__":

    setup(
        #name=release.name.lower(),
        name='graphpruning2',
        version="1.0",
        author="Nikhil Kanta",
        author_email="nikhilkantz25@gmail.com",
        license="MIT",
        url ="https://github.com/nikhilkanta/GraphPruning2",
        download_url = "https://github.com/nikhilkanta/GraphPruning2/archive/master.zip",
        keywords = ['networks', 'networkx', 'Pruning', 'graphs'],
        packages=packages,
        install_requires=install_requires,
        python_requires='>=3.5',
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.5'
            ] )
