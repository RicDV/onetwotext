#!/usr/bin/env python

import os
import sys
import setuptools

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://onetwotext.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='onetwotext',
    version='0.1.0',
    description='A python library that expose web-app to count text words',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Riccardo De Vecchis',
    author_email='devecchisriccardo@live.it',
    url='https://github.com/RicDV/onetwotext',
    packages=setuptools.find_packages(),
    package_dir={'onetwotext': 'onetwotext'},
    include_package_data=True,
    package_data={
        "": ["*.ttf","*.toml","*.key","*.js","*.html", "*.css","*.jpg","*.png"],
    },
    python_requires=">=3.7.5",
        install_requires=[
            "cryptography==2.8",
            "flask",
            "flask-session",
            "waitress",
            "toml",
            "fake_useragent",
            "pydantic",
            "curl_cffi"
            
        ],
        entry_points={
        "console_scripts": [
            "ott=onetwotext.main:main",
        ]
    },
    license='MIT',
    zip_safe=False,
    keywords='onetwotext',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
