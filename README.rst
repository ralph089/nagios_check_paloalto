=============================================
nagios_check_paloalto: a Nagios/Icinga Plugin
=============================================
nagios_check_paloalto is a **Nagios/Icinga plugin** for Palo Alto Next Generation Firewalls.
It is written in Python and based on the PA REST API.

Tested on:

- PA-500 v6.0.1 - v6.0.9
- PA-3050 v6.0.9

.. image:: https://travis-ci.org/ralph-hm/nagios_check_paloalto.svg?branch=master
    :target: https://travis-ci.org/ralph-hm/nagios_check_paloalto?branch=master

.. image:: https://coveralls.io/repos/ralph-hm/nagios_check_paloalto/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/ralph-hm/nagios_check_paloalto?branch=master

Documentation
-------------
http://nagios-check-paloalto.readthedocs.org/en/latest/

Quickstart
----------
Please make sure you have the following packages installed on your machine::

    $ apt-get install python-dev, libxslt1-dev

To install nagios_check_paloalto::

	$ pip install check_paloalto

Usage
-----
Command-line usage::

    usage: check_paloalto [-h] [-H HOST] [-T TOKEN] [-v]
                          {diskspace,certificates,load,environmental,sessinfo,thermal,throughput}
                          ...

    positional arguments:
      {diskspace,certificates,load,environmental,sessinfo,thermal,throughput}
        diskspace           Checks used diskspace.
        certificates        Checks the certificate store for expiring
                            certificates: Outputs is a warning, if a certificate
                            is in range.
        load                Checks the CPU load.
        environmental       Checks if an alarm is found.
        sessinfo            Checks important session parameters.
        thermal             Checks the temperature.
        throughput          Checks the throughput.

    optional arguments:
      -h, --help            show this help message and exit

    Connection:
      -H HOST, --host HOST  PaloAlto Server Hostname
      -T TOKEN, --token TOKEN
                            Generated Token for REST-API access

    Debug:
      -v, --verbose         increase output verbosity (use up to 3 times)

Features
--------

* TODO
