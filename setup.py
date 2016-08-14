#!/usr/bin/env python3

from setuptools import setup
import gcloudstoragecli

setup(name='gcloudstoragecli',
      author='Lorian Coltof',
      author_email='loriancoltof@gmail.com',
      url='https://github.com/lorian1333/GoogleCloudStorageCLI',
      long_description=gcloudstoragecli.__doc__,
      packages=['gcloudstoragecli'],
      version='0.0.1',
      install_requires=[
          'prompt_toolkit>=1.0.5',
          'pygments>=2.1',
          'click>=6.6'
      ],
      entry_points={
          'console_scripts': [
              'gcscli = gcloudstoragecli:run'
          ]
      }
      )
