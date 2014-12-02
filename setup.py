#!/usr/bin/env python

from setuptools import setup

setup(name='moves',
      version='0.1',
      description='Moves Client API',
      author='Derek Arnold',
      author_email='derek@derekarnold.net',
      url='https://github.com/lysol/moves',
      download_url='http://github.com/lysol/moves/archive/v0.1.tar.gz',
      packages=['moves'],
      install_requires=open('requirements.txt').read(),
      long_description=open('README.md').read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      license='MIT'
      )
