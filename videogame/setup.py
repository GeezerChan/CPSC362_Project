# Andy Huynh
# CPSC 386-02
# 2023-02-20
# ahuynh86@csu.fullerton.edu
# @GeezerChan
#
# Lab 00-03
#
# M3: Scene
#

""" Simple setup.py """

from setuptools import setup

setup_info = {
    "name": "videogame",
    "version": "0.1",
    "description": "A package to support writing games with PyGame",
    # TODO: Optional, add more information to the setup.py script
    # "long_description": open("README.md").read(),
    # "author": "Tuffy Titan",
    # "author_email": "tuffy@csu.fullerton.edu",
    # "url": "https://some.url/somehwere/maybe/github",
}

setup(**setup_info)
