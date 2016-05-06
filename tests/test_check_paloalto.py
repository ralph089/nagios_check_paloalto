#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_check_paloalto
----------------------------------

Tests for `check_paloalto` module.
"""
import responses

from check_pa.check_paloalto import parse_args, _diskspace, _certificates, \
    _environmental, _load, _sessinfo, _thermal, _throughput, _useragent
from tests.conftest import read_xml


class TestCheckPaloAlto(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = '123456ABC'
        cls.warn = 80
        cls.crit = 90
        cls.verbose = 1
        cls.exclude = ''
        cls.range = '0:20'
        cls.interface = 'test'
        cls.reset = False

    def test_arg_diskspace(self):
        args = parse_args(['-H', self.host, '-T', self.token, 'diskspace'])
        assert args.host == self.host
        assert args.token == self.token
        assert args.func.__name__ == _diskspace.__name__

    def test_arg_useragent(self):
        args = parse_args(['-H', self.host, '-T', self.token, 'useragent'])
        assert args.host == self.host
        assert args.token == self.token
        assert args.func.__name__ == _useragent.__name__

    def test_arg_certificates(self):
        args = parse_args(
            ['-H', self.host, '-T', self.token, 'certificates', '-ex',
             self.exclude, '-r', self.range])
        assert args.host == self.host
        assert args.token == self.token
        assert args.func.__name__ == _certificates.__name__

    def test_arg_throughput(self):
        args = parse_args(
            ['-H', self.host, '-T', self.token, 'throughput', '-i',
             self.interface])
        assert args.host == self.host
        assert args.token == self.token
        assert args.func.__name__ == _throughput.__name__

    def test_certificates(self):
        f = 'certificates.xml'
        check = _certificates(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'Certificate'

    def test_diskspace(self):
        f = 'diskspace.xml'
        check = _diskspace(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'DiskSpace'

    def test_load(self):
        f = 'load.xml'
        check = _load(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'Load'

    def test_sessinfo(self):
        f = 'mock_result.xml'
        check = _sessinfo(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'SessInfo'

    def test_environmental(self):
        f = 'environmentals_ok.xml'
        check = _environmental(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'Environmental'

    def test_thermal(self):
        f = 'mock_result.xml'
        check = _thermal(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'Thermal'

    def test_throughput(self):
        f = 'throughput1.xml'
        check = _throughput(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'Throughput'
