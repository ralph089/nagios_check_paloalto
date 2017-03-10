#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_check_paloalto
----------------------------------

Tests for `check_paloalto` modules.
"""

import pytest
import responses
from nagiosplugin import CheckError

import utils
from check_pa.xml_reader import XMLReader, Finder


class TestCheckPaloAltoXML(object):
    @responses.activate
    def test_xml_read_response(self):
        f = 'diskspace.xml'
        xml_reader = XMLReader('test.de', 'test', 'test')

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, xml_reader.build_request_url(),
                     body=utils.read_xml(f), status=200,
                     content_type='document',
                     match_querystring=True)
            xml_response = xml_reader.read()
            text = xml_response.response['status']
            assert text == "success"

    @responses.activate
    def test_xml_exception_404(self):
        f = 'diskspace.xml'
        xml_reader = XMLReader('test.de', 'test', 'test')

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, xml_reader.build_request_url(),
                     body=utils.read_xml(f), status=404,
                     content_type='document',
                     match_querystring=True)
            with pytest.raises(CheckError):
                xml_reader.read()

    @responses.activate
    def test_not_authorized(self):
        f = 'not_authorized.xml'
        xml_reader = XMLReader('test.de', 'test', 'test')

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, xml_reader.build_request_url(),
                     body=utils.read_xml(f), status=200,
                     content_type='document',
                     match_querystring=True)
            with pytest.raises(CheckError):
                xml_reader.read()

    @responses.activate
    def test_finder(self):
        f = 'load.xml'
        xml_reader = XMLReader('test.de', 'test', 'test')

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, xml_reader.build_request_url(),
                     body=utils.read_xml(f), status=200,
                     content_type='document',
                     match_querystring=True)
            xml_response = xml_reader.read()
            found = Finder.find_item(xml_response, 'coreid')
            assert '0' == found

    @responses.activate
    def test_finder2(self):
        f = 'load.xml'
        xml_reader = XMLReader('test.de', 'test', 'test')

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, xml_reader.build_request_url(),
                     body=utils.read_xml(f), status=200,
                     content_type='document',
                     match_querystring=True)
            xml_response = xml_reader.read()
            with pytest.raises(CheckError):
                Finder.find_item(xml_response, 'test')
