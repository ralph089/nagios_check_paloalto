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

import check_pa.modules.thermal
import utils


class TestThermal(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = 'test'

    @responses.activate
    def test_thermal(self):
        self.warn = 80
        self.crit = 90

        f = 'thermal.xml'
        check = check_pa.modules.thermal.create_check(self)
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
            assert check.summary_str == 'Temperature @ Test1 is 30 degrees' \
                                        ' Celsius, Temperature @ Test2 is 34' \
                                        ' degrees Celsius, Temperature @' \
                                        ' Test3 is 37 degrees Celsius,' \
                                        ' Temperature @ Test4' \
                                        ' is 25 degrees Celsius'

    @responses.activate
    def test_thermal_critical(self):
        self.warn = 20
        self.crit = 30

        f = 'thermal.xml'
        check = check_pa.modules.thermal.create_check(self)
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
            assert check.summary_str == 'Too high temperature: Temperature @ ' \
                                        'Test1 is 30.6 (outside range 0:30) ' \
                                        'degrees Celsius'
