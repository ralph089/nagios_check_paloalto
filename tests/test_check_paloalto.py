#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_check_paloalto
----------------------------------

Tests for `check_paloalto` modules.
"""

import responses

import utils
from check_pa.check_paloalto import parse_args
from check_pa.modules import diskspace, certificate, load, environmental, sessioninfo, thermal, throughput


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

    def test_arg_useragent(self):
        args = parse_args(['-H', self.host, '-T', self.token, 'useragent'])
        assert args.host == self.host
        assert args.token == self.token

    def test_arg_certificates(self):
        args = parse_args(
            ['-H', self.host, '-T', self.token, 'certificates', '-ex',
             self.exclude, '-r', self.range])
        assert args.host == self.host
        assert args.token == self.token

    def test_arg_throughput(self):
        args = parse_args(
            ['-H', self.host, '-T', self.token, 'throughput', '-i',
             self.interface])
        assert args.host == self.host
        assert args.token == self.token

    def test_certificates(self):
        f = 'certificates.xml'
        check = certificate.create_check(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'Certificate'

    def test_diskspace(self):
        f = 'diskspace.xml'
        check = diskspace.create_check(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'DiskSpace'

    def test_load(self):
        f = 'load.xml'
        check = load.create_check(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'Load'

    def test_sessinfo(self):
        f = 'mock_result.xml'
        check = sessioninfo.create_check(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'SessInfo'

    def test_environmental(self):
        f = 'environmentals_ok.xml'
        check = environmental.create_check(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'Environmental'

    def test_thermal(self):
        f = 'mock_result.xml'
        check = thermal.create_check(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'Thermal'

    def test_throughput(self):
        f = 'throughput1.xml'
        check = throughput.create_check(self)
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     check.resources[0].xml_obj.build_request_url(),
                     body=utils.read_xml(f),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            check.__call__()
        assert check.name == 'Throughput'
