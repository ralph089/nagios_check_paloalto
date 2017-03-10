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

import check_pa.modules.load
import utils


class TestLoad(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = 'test'

    @responses.activate
    def test_load_ok(self):
        self.warn = 80
        self.crit = 90

        f = 'load.xml'
        check = check_pa.modules.load.create_check(self)
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
        assert check.summary_str == 'CPU0: 0.0%, CPU1: 2.0%, CPU2: 4.0%, ' \
                                    'CPU3: 4.0%, CPU4: 5.0%, CPU5: 6.0%'

    @responses.activate
    def test_load_critical(self):
        self.warn = 90
        self.crit = 5

        f = 'load.xml'
        check = check_pa.modules.load.create_check(self)
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
        assert check.summary_str == 'CPU5 is 6% (outside range 0:5)'
