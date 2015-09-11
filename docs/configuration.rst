=============
Configuration
=============
*****
Token
*****
The REST API requires a token to get information. This token must be generated once::

	1. Create a "monitoring role" in the PA.
	2. Disable everything in the WEB UI tab within that role
	3. Enable "Operational requests" in the XML API tab and disable everything else
	4. Ensure that the tab "Command line" is "None"
	5. Create a new Admin user who uses that custom role and for best practices choose at least 20 length password without special characters other than '_-'
	6. Generating the token is easy. To do that login to your PA with the monitoring user

	and open:
	https://x.x.x.x/api/?type=keygen&user=YOUR-USERNAME&password=YOUR-PASSWORD
	(replace YOUR-USERNAME with the username created in step 5. and YOUR-PASSWORD accordingly)

******
Nagios
******
.. code-block:: console

 define command {
        command_name    check_paloalto
        command_line    /usr/local/bin/check_paloalto
        }