# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

# Declare your non-python data files:
# Files underneath configuration/ will be copied into the build preserving the
# subdirectory structure if they exist.
data_files = []
for root, dirs, files in os.walk('conf'):
    data_files.append((os.path.relpath(root, 'conf'),
                       [os.path.join(root, f) for f in files]))

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
    packages=find_packages(where="src", exclude=("test",)),
    package_dir={"": "src"},

    # include data files
    data_files=data_files,

    # requirements
    install_requires=['Flask', 'boto3', 'AWSIoTPythonSDK', 'numpy', 'flask_wtf'],
    python_requires='>=3.6.0',
)
