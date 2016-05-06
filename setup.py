#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'nagiosplugin',
    'beautifulsoup4',
    'lxml',
    'requests'
]

test_requirements = [
    'responses',
    'flake8'
]

setup(name='check_paloalto',
      version='0.1.6',
      description="check_paloalto is a Nagios/Icinga plugin for Palo Alto Next Generation Firewalls. It is written in Python and based on the PA REST API.",
      long_description=readme + '\n\n' + history,
      author="Ralph Offinger",
      author_email='ralph.offinger@gmail.com',
      url='https://github.com/ralph-hm/nagios_check_paloalto',
      install_requires=requirements,
      packages=['check_pa'],
      entry_points={
          'console_scripts': [
              'check_paloalto = check_pa.check_paloalto:main'
          ]
      },
      license="CC BY-ND 4.0",
      classifiers=[
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 4 - Beta',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',

          'Topic :: System :: Monitoring',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: Common Public License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
      ],

      # What does your project relate to?
      keywords='paloalto icinga nagios check',
      test_suite='tests',
      tests_require=test_requirements,
      )
