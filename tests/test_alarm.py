#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_check_paloalto
----------------------------------

Tests for `check_paloalto` modules.
"""

import pytest
import responses
from nagiosplugin.state import ServiceState

import utils
from check_pa.modules import environmental


class TestAlarm(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = 'test'

    @responses.activate
    def test_alarm(self):
        f = 'environmentals_ok.xml'
        check = environmental.create_check(self)
        obj = check.resources[0]

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     obj.xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            with pytest.raises(SystemExit):
                check.main(verbose=3)

            assert check.exitcode == 0
            assert check.state == ServiceState(code=0, text='ok')
            assert check.summary_str == 'No alarms found.'

    @responses.activate
    def test_alarm_critical(self):
        f = 'environmentals_alarms.xml'
        check = environmental.create_check(self)
        obj = check.resources[0]

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     obj.xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            with pytest.raises(SystemExit):
                check.main(verbose=3)

            assert check.exitcode == 2
            assert check.state == ServiceState(code=2, text='critical')
            assert check.summary_str == 'Alarm(s) found: Temperature @ Test1, ' \
                                        'Temperature @ Test2'
