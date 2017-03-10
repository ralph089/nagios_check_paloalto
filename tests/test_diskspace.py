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

import check_pa.modules.diskspace
import utils


class TestDiskspace(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = 'test'

    @responses.activate
    def test_diskspace(self):
        self.warn = 80
        self.crit = 90

        f = 'diskspace.xml'
        check = check_pa.modules.diskspace.create_check(self)
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
            assert check.summary_str == 'sda2: 57%, ' \
                                        'sda5: 43%, ' \
                                        'sda6: 30%, ' \
                                        'sda8: 47%'

    @responses.activate
    def test_diskspace_warning(self):
        self.warn = 50
        self.crit = 90

        f = 'diskspace.xml'
        check = check_pa.modules.diskspace.create_check(self)
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
            assert check.summary_str == 'sda2 is 57% (outside range 0:50)'
