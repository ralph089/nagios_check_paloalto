#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup

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
      version='0.3.1',
      description="check_paloalto is a Nagios/Icinga plugin for Palo Alto Next Generation Firewalls. It is written in "
                  "Python and based on the PA REST API.",
      long_description=readme + '\n\n' + history,
      author="Ralph Offinger",
      author_email='ralph.offinger@gmail.com',
      url='https://github.com/ralph-hm/nagios_check_paloalto',
      install_requires=requirements,
      packages=['check_pa', 'check_pa.modules'],
      entry_points={
          'console_scripts': [
              'check_paloalto = check_pa.check_paloalto:main'
          ]
      },
      license="CC BY-ND 4.0",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Topic :: System :: Monitoring',
          'License :: OSI Approved :: Common Public License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='paloalto icinga nagios check',
      zip_safe=False,
      test_suite='tests',
      tests_require=test_requirements,
      )
