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

import check_pa.throughput
from tests.conftest import read_xml


class TestThroughput(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = 'test'

    @responses.activate
    def test_with_three_interfaces(self):
        self.interface = 'ethernet1/1, ethernet1/2, ethernet1/3'
        interfaces = []
        for interface in self.interface.split(','):
            interfaces.append(interface)

        file1 = 'throughput1.xml'
        file2 = 'throughput2.xml'
        file3 = 'throughput3.xml'

        check = check_pa.throughput.create_check(self)
        objects = []
        for ressource in check.resources:
            objects.append(ressource)

        with responses.RequestsMock() as rsps:

            rsps.add(responses.GET,
                     objects[0].xml_obj.build_request_url(),
                     body=read_xml(file1),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            rsps.add(responses.GET,
                     objects[1].xml_obj.build_request_url(),
                     body=read_xml(file2),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            rsps.add(responses.GET,
                     objects[2].xml_obj.build_request_url(),
                     body=read_xml(file3),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            from nagiosplugin import Cookie

            try:
                # Resetting cookies
                with Cookie(
                        check_pa.throughput.Throughput.statefile) as cookie:
                    cookie[interfaces[0] + 'i'] = 0
                    cookie[interfaces[0] + 'o'] = 0
                    cookie[interfaces[0] + 't'] = 1441324800
                    cookie[interfaces[1] + 'i'] = 0
                    cookie[interfaces[1] + 'o'] = 0
                    cookie[interfaces[1] + 't'] = 1441324800
                    cookie[interfaces[2] + 'i'] = 0
                    cookie[interfaces[2] + 'o'] = 0
                    cookie[interfaces[2] + 't'] = 1441324800

                # Check will be executed exactly one second later
                now = 1441324801
                xml_ibytes = 1000000
                xml_obytes = 1000000
                with mock.patch('check_pa.throughput.get_time',
                                return_value=now):
                    with mock.patch('check_pa.xml_reader.Finder.find_item',
                                    side_effect=[xml_ibytes, xml_obytes,
                                                 xml_ibytes, xml_ibytes,
                                                 xml_ibytes, xml_ibytes]):
                        with pytest.raises(SystemExit):
                            check.main(verbose=3)
            finally:
                import os
                os.remove(check_pa.throughput.Throughput.statefile)

            assert check.exitcode == 0
            assert check.state == ServiceState(code=0, text='ok')

            # 3000000 Byte = 3 MByte = 24 Mbit in 1 second = 24.0 Mb/s
            assert check.summary_str == 'Input is 24.0 Mb/s - Output is 24.0 ' \
                                        'Mb/s'

    @responses.activate
    def test_with_one_interface(self):
        file1 = 'throughput1.xml'

        self.interface = 'ethernet1/1'
        interfaces = []
        for interface in self.interface.split(','):
            interfaces.append(interface)

        check = check_pa.throughput.create_check(self)
        objects = []
        for ressource in check.resources:
            objects.append(ressource)

        with responses.RequestsMock() as rsps:

            rsps.add(responses.GET,
                     objects[0].xml_obj.build_request_url(),
                     body=read_xml(file1),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            from nagiosplugin import Cookie

            # Resetting cookies
            try:
                with Cookie(
                        check_pa.throughput.Throughput.statefile) as cookie:
                    cookie[interfaces[0] + 'i'] = 0
                    cookie[interfaces[0] + 'o'] = 0
                    cookie[interfaces[0] + 't'] = 1441324800

                # Check will be executed exactly ten seconds later
                now = 1441324810

                xml_ibytes = 1000000
                xml_obytes = 1000000
                with mock.patch('check_pa.throughput.get_time',
                                return_value=now):
                    with mock.patch('check_pa.xml_reader.Finder.find_item',
                                    side_effect=[xml_ibytes, xml_obytes]):
                        with pytest.raises(SystemExit):
                            check.main(verbose=3)
            finally:
                import os
                os.remove(check_pa.throughput.Throughput.statefile)

            assert check.exitcode == 0
            assert check.state == ServiceState(code=0, text='ok')

            # 1000000 Byte = 1 MByte = 8 Mbit in 10 seconds = 0.8 Mb/s
            assert check.summary_str == 'Input is 0.8 Mb/s - Output is 0.8 ' \
                                        'Mb/s'

    @responses.activate
    def test_new_input_less_than_old(self):
        file1 = 'throughput1.xml'

        self.interface = 'ethernet1/1'
        interfaces = []
        for interface in self.interface.split(','):
            interfaces.append(interface)

        check = check_pa.throughput.create_check(self)
        objects = []
        for ressource in check.resources:
            objects.append(ressource)

        with responses.RequestsMock() as rsps:

            rsps.add(responses.GET,
                     objects[0].xml_obj.build_request_url(),
                     body=read_xml(file1),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            from nagiosplugin import Cookie

            # Resetting cookies
            try:
                with Cookie(
                        check_pa.throughput.Throughput.statefile) as cookie:
                    cookie[interfaces[0] + 'i'] = 10
                    cookie[interfaces[0] + 'o'] = 10
                    cookie[interfaces[0] + 't'] = 1441324800

                # Check will be executed exactly ten seconds later
                now = 1441324810

                xml_ibytes = 9
                xml_obytes = 11
                with mock.patch('check_pa.throughput.get_time',
                                return_value=now):
                    with mock.patch('check_pa.xml_reader.Finder.find_item',
                                    side_effect=[xml_ibytes, xml_obytes]):
                        with pytest.raises(SystemExit):
                            check.main(verbose=3)
            finally:
                import os
                os.remove(check_pa.throughput.Throughput.statefile)

            assert check.exitcode == 3
            assert check.state == ServiceState(code=3, text='unknown')
            assert check.summary_str == 'Couldn\'t get a valid input value!\n\n' \
                                        'If you recently upgraded the PA firmware or restarted the PA, ' \
                                        'please read the documentation.'

    @responses.activate
    def test_new_output_less_than_old(self):
        file1 = 'throughput1.xml'

        self.interface = 'ethernet1/1'
        interfaces = []
        for interface in self.interface.split(','):
            interfaces.append(interface)

        check = check_pa.throughput.create_check(self)
        objects = []
        for ressource in check.resources:
            objects.append(ressource)

        with responses.RequestsMock() as rsps:

            rsps.add(responses.GET,
                     objects[0].xml_obj.build_request_url(),
                     body=read_xml(file1),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            from nagiosplugin import Cookie

            # Resetting cookies
            try:
                with Cookie(
                        check_pa.throughput.Throughput.statefile) as cookie:
                    cookie[interfaces[0] + 'i'] = 10
                    cookie[interfaces[0] + 'o'] = 10
                    cookie[interfaces[0] + 't'] = 1441324800

                # Check will be executed exactly ten seconds later
                now = 1441324810

                xml_ibytes = 11
                xml_obytes = 9
                with mock.patch('check_pa.throughput.get_time',
                                return_value=now):
                    with mock.patch('check_pa.xml_reader.Finder.find_item',
                                    side_effect=[xml_ibytes, xml_obytes]):
                        with pytest.raises(SystemExit):
                            check.main(verbose=3)
            finally:
                import os
                os.remove(check_pa.throughput.Throughput.statefile)

            assert check.exitcode == 3
            assert check.state == ServiceState(code=3, text='unknown')
            assert check.summary_str == 'Couldn\'t get a valid output value!\n\n' \
                                        'If you recently upgraded the PA firmware or restarted the PA, ' \
                                        'please read the documentation.'

    @responses.activate
    def test_same_time(self):
        file1 = 'throughput1.xml'

        self.interface = 'ethernet1/1'
        interfaces = []
        for interface in self.interface.split(','):
            interfaces.append(interface)

        check = check_pa.throughput.create_check(self)
        objects = []
        for ressource in check.resources:
            objects.append(ressource)

        with responses.RequestsMock() as rsps:

            rsps.add(responses.GET,
                     objects[0].xml_obj.build_request_url(),
                     body=read_xml(file1),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            from nagiosplugin import Cookie

            # Resetting cookies
            try:
                with Cookie(
                        check_pa.throughput.Throughput.statefile) as cookie:
                    cookie[interfaces[0] + 'i'] = 10
                    cookie[interfaces[0] + 'o'] = 10
                    cookie[interfaces[0] + 't'] = 1441324800

                # Check will be executed exactly at the same time
                now = 1441324800

                xml_ibytes = 11
                xml_obytes = 11
                with mock.patch('check_pa.throughput.get_time',
                                return_value=now):
                    with mock.patch('check_pa.xml_reader.Finder.find_item',
                                    side_effect=[xml_ibytes, xml_obytes]):
                        with pytest.raises(SystemExit):
                            check.main(verbose=3)
            finally:
                import os
                os.remove(check_pa.throughput.Throughput.statefile)

            assert check.exitcode == 3
            assert check.state == ServiceState(code=3, text='unknown')
            assert check.summary_str == 'Difference between old timestamp ' \
                                        'and new timestamp is less or equal 0: ' \
                                        'If it is the first time you run the ' \
                                        'script, please execute it again!'
