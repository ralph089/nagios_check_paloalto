=============================================
nagios_check_paloalto: a Nagios/Icinga Plugin
=============================================
nagios_check_paloalto is a **Nagios/Icinga plugin** for Palo Alto Next Generation Firewalls.
It is written in Python and based on the PA REST API.

Tested on:

- PA-500 v6.0.1 - v6.0.9
- PA-3050 v6.0.9 - 7.0.0

.. image:: https://travis-ci.org/ralph-hm/nagios_check_paloalto.svg?branch=master
    :target: https://travis-ci.org/ralph-hm/nagios_check_paloalto?branch=master

.. image:: https://coveralls.io/repos/ralph-hm/nagios_check_paloalto/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/ralph-hm/nagios_check_paloalto?branch=master

.. image:: https://badge.fury.io/py/check_paloalto.svg
    :target: https://badge.fury.io/py/check_paloalto

Documentation
-------------
http://nagios-check-paloalto.readthedocs.org/en/latest/

Quickstart
----------
Please make sure you have python-dev and libxslt1-dev installed on your machine.

To install nagios_check_paloalto::

	$ pip install check_paloalto

or use::

	$ pip3 install check_paloalto

The plugin requires a token to get information from the PA-REST-API. Please see the following link for more information:
http://nagios-check-paloalto.readthedocs.org/en/latest/configuration.html#token

Usage
-----
Command-line usage::

    usage: check_paloalto [-h] -H HOST -T TOKEN [-v] [-t TIMEOUT] [--version]
                      {diskspace,certificates,load,useragent,environmental,sessinfo,thermal,throughput}
                      ...

    positional arguments:
      {diskspace,certificates,load,useragent,environmental,sessinfo,thermal,throughput}
        diskspace           check used diskspace.
        certificates        check the certificate store for expiring certificates:
                            Outputs is a warning, if a certificate is in range.
        load                check the CPU load.
        useragent           check for running useragents.
        environmental       check if an alarm is found.
        sessinfo            check important session parameters.
        thermal             check the temperature.
        throughput          check the throughput.

    optional arguments:
      -h, --help            show this help message and exit

    Connection:
      -H HOST, --host HOST  PaloAlto Server Hostname
      -T TOKEN, --token TOKEN
                            Generated Token for REST-API access

    Debug:
      -v, --verbose         increase output verbosity (use up to 3 times)
      -t TIMEOUT, --timeout TIMEOUT
                            abort check execution after so many seconds (use 0 for
                            no timeout)

    Info:
      --version             show program's version number and exit


