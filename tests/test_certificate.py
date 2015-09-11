#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_check_paloalto
----------------------------------

Tests for `check_paloalto` module.
"""

import responses
import mock
import pytest
from nagiosplugin.state import ServiceState

import check_pa.certificate
from tests.conftest import read_xml


class TestCertificates(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = 'test'
        cls.exclude = ''
        cls.range = '0:20'

    @responses.activate
    def test_certificate_warning(self):
        check = check_pa.certificate.create_check(self)
        obj = check.resources[0]

        from datetime import datetime
        now = datetime(2011, 10, 1)
        with mock.patch('check_pa.certificate.get_now',
                        return_value=now):
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET,
                         obj.xml_obj.build_request_url(),
                         body=read_xml('certificates.xml'),
                         status=200,
                         content_type='document',
                         match_querystring=True)

                with pytest.raises(SystemExit):
                    check.main(verbose=3)

        assert check.exitcode == 1
        assert check.state == ServiceState(code=1, text='warning')
        assert check.summary_str == 'test-certificate1 expires in 1 days, ' \
                                    'test-certificate2 expires in 2 days'

    @responses.activate
    def test_certificate_ok(self):
        check = check_pa.certificate.create_check(self)
        obj = check.resources[0]

        from datetime import datetime
        now = datetime(2011, 9, 1)
        with mock.patch('check_pa.certificate.get_now',
                        return_value=now):
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET,
                         obj.xml_obj.build_request_url(),
                         body=read_xml('certificates.xml'),
                         status=200,
                         content_type='document',
                         match_querystring=True)

                with pytest.raises(SystemExit):
                    check.main(verbose=3)

        assert check.exitcode == 0
        assert check.state == ServiceState(code=0, text='ok')
        assert check.summary_str == 'The next certificate will expire ' \
                                    'in 31 days.'
