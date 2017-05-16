.. :changelog:

History
-------
0.3.2 (2017-16-05)
------------------
* Fixed issue #8: Measuring throughput on multiple identically configured PA's fails

0.3.1 (2017-10-03)
------------------

* Improvement: It is no longer necessary to reset the internal cookie when upgrading PA.
* Renamed performance data label for throughput command.
* Removed the the unit of measurement (UOM) for throughput command

0.3 (2017-27-02)
----------------

* Support for Python 3.5 added
* Minor code improvements
* Changed the the unit of measurement (UOM) according to official Nagios-Documentation (thanks to Ios77)

0.1.6 (2016-06-05)
------------------

* Added script version switch
* Improved error handling
* Updated documentation
* Upgraded dependencies

0.1.5 (2016-29-04)
------------------

* Fixed a argparse bug


0.1.4 (2016-29-04)
------------------

* Added functionality to monitor state of the user-agents
* Added script timeout switch
* Improved error handling
* Improved functionality of sessinfo command


0.1.3 (2015-14-09)
------------------

* Disabled warnings for insecure requests to support older installations:
  https://urllib3.readthedocs.org/en/latest/security.html


0.1.2 (2015-14-09)
------------------

* Fixed a bug for parsing args in python3.
* Enabled warnings for insecure requests:
  https://urllib3.readthedocs.org/en/latest/security.html
* Changed format for setup.cfg.
* Updated docs.


0.1.1 (2015-10-09)
------------------

* Support Python 2.7, 3.3, 3.4.
* Support PyPi.
* Included tests.
* Improved performance.
* Improved output and debugging.
