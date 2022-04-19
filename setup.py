#!/usr/bin/env python3

from setuptools import setup, find_packages
import json
import os


try:
    rd_me_file_path = os.path.join( os.path.dirname(os.path.realpath(__file__)), "README.md")
    with open(rd_me_file_path, "r") as fh:
        long_description = fh.read()
    
    ver_file_path = os.path.join( os.path.dirname(os.path.realpath(__file__)), "jiosaavndownloader", "version.json")
    with open( ver_file_path, "r") as fh2:
        pkg_ver = json.load(fh2)['version']
except:
    raise



setup(
    name='jiosaavndownloader',
    version=pkg_ver,
    author="Vijaymahantesh Sattigeri",
    author_email="vijaymahantesh016@gmail.com",
    description="Downloads high quality songs from JioSaavn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vijaysattigeri/jiosaavndownloader",
    packages=find_packages(),
    # Copies these files to installation directory
    package_data = {
        "" : [ver_file_path]
    },
    install_requires = [
        'requests',
        'pyDes',
        'mutagen',
        'tqdm'
    ],
    entry_points = {
        'console_scripts': [
            'jiosaavndownloader = jiosaavndownloader.__main__:main'
            ]
    },
    license='Mozilla Public License Version 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers']
 )
