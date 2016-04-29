===
FAQ
===

If you have recently upgraded the PA firmware or reset the firewall and you are using the throughput command,
you receive the following error::

    Couldn't get a valid input value!

    If you recently upgraded the PA firmware or restarted the PA, please read the documentation.

The error occurs, because the plugins use a throughput counter from the REST-API. The value is stored on the computer,
to compare the new value with the stored one. If you reset or restart the PA, this will also reset the throughput
counter.

You can solve this error by executing the following command::

     $  check_paloalto reset_throughput
