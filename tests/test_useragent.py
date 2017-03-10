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

import check_pa.modules.useragent
import utils


class TestUserAgent(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = 'test'

    @responses.activate
    def test_useragent(self):
        self.warn = 60
        self.crit = 240

        f = 'useragent_ok.xml'
        check = check_pa.modules.useragent.create_check(self)
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
            assert check.summary_str == 'All agents are connected and responding.'

    @responses.activate
    def test_useragent_warning(self):
        self.warn = 60
        self.crit = 240

        f = 'useragent_last_heared.xml'
        check = check_pa.modules.useragent.create_check(self)
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

            assert check.exitcode == 1
            assert check.state == ServiceState(code=1, text='warning')
            assert check.summary_str == 'Agent: Agent1 - Name1(vsys: vsys1) Host: 10.10.10.10(10.10.10.10):5007 ' \
                                        'last heared: 61 seconds ago'

    @responses.activate
    def test_useragent_critical_noconn(self):
        self.warn = 60
        self.crit = 240

        f = 'useragent_no_connection.xml'
        check = check_pa.modules.useragent.create_check(self)
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
            assert check.summary_str == 'Agent: Agent2 - Name2(vsys: vsys1) Host: 192.168.0.1(192.168.0.1):5007 ' \
                                        'connection status is error, ' \
                                        'Agent: Agent3 - Name3(vsys: vsys1) Host:11.11.11.11(11.11.11.11):5007 ' \
                                        'connection status is non-conn'

    @responses.activate
    def test_useragent_critical_last_heared(self):
        self.warn = 2
        self.crit = 30

        f = 'useragent_last_heared.xml'
        check = check_pa.modules.useragent.create_check(self)
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
            assert check.summary_str == 'Agent: Agent1 - Name1(vsys: vsys1) Host: 10.10.10.10(10.10.10.10):5007 last heared: 61 seconds ago'

    @responses.activate
    def test_useragent_changed_format(self):
        self.warn = 2
        self.crit = 30

        f = 'useragent_changed_format.xml'
        check = check_pa.modules.useragent.create_check(self)
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

            assert check.exitcode == 3
            assert check.state == ServiceState(code=3, text='unknown')
