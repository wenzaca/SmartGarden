# -*- coding: utf-8 -*-

import os

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name="smartgarden_webserver",
    version="1.0",
    description="Smart Garden Webserver used to control an Raspberry PI, developed in Python with JS, Jquery and Ajax.",
    long_description=readme,
    author='Wendler Zacariotto',
    author_email='wenzaca@gmail.com',
    url='https://github.com/wenzaca/SmartGarden',
    license=license,

    # declare your packages
    packages=["src", "src.flaskapp"],

    # include data files
    data_files=['conf'],

    # requirements
    install_requires=['Flask', 'boto3', 'AWSIoTPythonSDK', 'numpy', 'flask_wtf'],
    python_requires='>=3.6.0',

    # tests
    test_suite="test"


)
