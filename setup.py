#!/usr/bin/env python3
import os
from setuptools import setup

long_description = open(
    os.path.join(
        os.path.dirname(__file__),
        'README.rst'
    )
).read()

setup(name='gcloudstoragecli',
      author='Lorian Coltof',
      author_email='loriancoltof@gmail.com',
      url='https://github.com/lorian1333/GoogleCloudStorageCLI',
      long_description=long_description,
      packages=['gcloudstoragecli'],
      version='0.0.1',
      install_requires=[
          'prompt_toolkit>=1.0.5',
          'pygments>=2.1',
          'click>=6.6',
          'gcloud>=0.18'
      ],
      entry_points={
          'console_scripts': [
              'gcscli = gcloudstoragecli:run'
          ]
      }
      )
