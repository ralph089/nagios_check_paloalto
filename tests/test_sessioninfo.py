#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_check_paloalto
----------------------------------

Tests for `check_paloalto` modules.
"""

import mock
import pytest
import responses
from nagiosplugin.state import ServiceState

import check_pa.modules.sessioninfo
import utils


class TestSessionInfo(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = 'test'

    @responses.activate
    def test_sessinfo(self):
        f = 'mock_result.xml'
        self.warn = 20000
        self.crit = 50000

        check = check_pa.modules.sessioninfo.create_check(self)
        obj = check.resources[0]

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     obj.xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            nummax = 262142
            numactive = 4480
            kbps = 24266

            with mock.patch('check_pa.xml_reader.Finder.find_item',
                            side_effect=[nummax, numactive, kbps]):
                with pytest.raises(SystemExit):
                    check.main(verbose=3)

            assert check.exitcode == 0
            assert check.state == ServiceState(code=0, text='ok')
            assert check.summary_str == 'Active sessions: 4480 ' \
                                        '/ Throughput (kbps): 24266'

    @responses.activate
    def test_sessinfo_warning(self):
        f = 'mock_result.xml'
        self.warn = 4000
        self.crit = 50000

        check = check_pa.modules.sessioninfo.create_check(self)
        obj = check.resources[0]

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     obj.xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            nummax = 262142
            numactive = 4480
            kbps = 24266

            with mock.patch('check_pa.xml_reader.Finder.find_item',
                            side_effect=[nummax, numactive, kbps]):
                with pytest.raises(SystemExit):
                    check.main(verbose=3)

            assert check.exitcode == 1
            assert check.state == ServiceState(code=1, text='warning')
            assert check.summary_str == 'session is 4480 (outside range 0:4000)'

    @responses.activate
    def test_sessinfo_warning2(self):
        f = 'mock_result.xml'
        self.warn = 4000
        self.crit = 5000

        check = check_pa.modules.sessioninfo.create_check(self)
        obj = check.resources[0]

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     obj.xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            nummax = 262142
            numactive = 5002
            kbps = 24266

            with mock.patch('check_pa.xml_reader.Finder.find_item',
                            side_effect=[nummax, numactive, kbps]):
                with pytest.raises(SystemExit):
                    check.main(verbose=3)

            assert check.exitcode == 2
            assert check.state == ServiceState(code=2, text='critical')
            assert check.summary_str == 'session is 5002 (outside range 0:5000)'
