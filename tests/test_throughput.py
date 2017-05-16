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

import check_pa.modules.throughput
import utils


class TestThroughput(object):
    @classmethod
    def setup_class(cls):
        """setup host and token for test of Palo Alto Firewall"""
        cls.host = 'localhost'
        cls.token = 'test'

    @responses.activate
    def test_with_three_interfaces(self, statefile):
        self.interface = 'ethernet1/1, ethernet1/2, ethernet1/3'
        interfaces = []
        for interface in self.interface.split(','):
            interfaces.append(interface)

        file1 = 'throughput1.xml'
        file2 = 'throughput2.xml'
        file3 = 'throughput3.xml'

        check = check_pa.modules.throughput.create_check(self)
        objects = []
        for resource in check.resources:
            objects.append(resource)

        with responses.RequestsMock() as rsps:

            rsps.add(responses.GET,
                     objects[0].xml_obj.build_request_url(),
                     body=utils.read_xml(file1),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            rsps.add(responses.GET,
                     objects[1].xml_obj.build_request_url(),
                     body=utils.read_xml(file2),
                     status=200,
                     content_type='document',
                     match_querystring=True)
            rsps.add(responses.GET,
                     objects[2].xml_obj.build_request_url(),
                     body=utils.read_xml(file3),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            from nagiosplugin import Cookie

            # Resetting cookies
            with Cookie(statefile) as cookie:
                cookie[self.host + interfaces[0] + 'i'] = 0
                cookie[self.host + interfaces[0] + 'o'] = 0
                cookie[self.host + interfaces[0] + 't'] = 1441324800
                cookie[self.host + interfaces[1] + 'i'] = 0
                cookie[self.host + interfaces[1] + 'o'] = 0
                cookie[self.host + interfaces[1] + 't'] = 1441324800
                cookie[self.host + interfaces[2] + 'i'] = 0
                cookie[self.host + interfaces[2] + 'o'] = 0
                cookie[self.host + interfaces[2] + 't'] = 1441324800

            # Check will be executed exactly one second later
            now = 1441324801
            xml_ibytes = 1000000
            xml_obytes = 1000000

            with mock.patch('check_pa.modules.throughput.get_time',
                            return_value=now):
                with mock.patch('check_pa.xml_reader.Finder.find_item',
                                side_effect=[xml_ibytes, xml_obytes,
                                             xml_ibytes, xml_ibytes,
                                             xml_ibytes, xml_ibytes]):
                    with pytest.raises(SystemExit):
                        check.main(verbose=3)

            assert check.exitcode == 0
            assert check.state == ServiceState(code=0, text='ok')

            # 3000000 Byte = 3 MByte = 24 Mbit in 1 second = 24.0 Mb/s
            assert check.summary_str == 'Input is 24.0 Mb/s - Output is 24.0 ' \
                                        'Mb/s'

    @responses.activate
    def test_with_one_interface(self, statefile):
        file1 = 'throughput1.xml'

        self.interface = 'ethernet1/1'
        interfaces = []
        for interface in self.interface.split(','):
            interfaces.append(interface)

        check = check_pa.modules.throughput.create_check(self)
        objects = []
        for res in check.resources:
            objects.append(res)

        with responses.RequestsMock() as rsps:

            rsps.add(responses.GET,
                     objects[0].xml_obj.build_request_url(),
                     body=utils.read_xml(file1),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            from nagiosplugin import Cookie

            with Cookie(statefile) as cookie:
                cookie[self.host + interfaces[0] + 'i'] = 0
                cookie[self.host + interfaces[0] + 'o'] = 0
                cookie[self.host + interfaces[0] + 't'] = 1441324800

            # Check will be executed exactly ten seconds later
            now = 1441324810

            xml_ibytes = 1000000  # 1000000 Byte = 1 MByte
            xml_obytes = 1000000  # 1000000 Byte = 1 MByte
            with mock.patch('check_pa.modules.throughput.get_time',
                            return_value=now):
                with mock.patch('check_pa.xml_reader.Finder.find_item',
                                side_effect=[xml_ibytes, xml_obytes]):
                    with pytest.raises(SystemExit):
                        check.main(verbose=3)

            assert check.exitcode == 0
            assert check.state == ServiceState(code=0, text='ok')
            assert check.summary_str == 'Input is 0.8 Mb/s - Output is 0.8 ' \
                                        'Mb/s'

    def check_pa(self, time, ibytes, obytes, filename):
        objects = []
        file1 = filename

        check = check_pa.modules.throughput.create_check(self)

        for res in check.resources:
            objects.append(res)

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     objects[0].xml_obj.build_request_url(),
                     body=utils.read_xml(file1),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            with mock.patch('check_pa.modules.throughput.get_time',
                            return_value=time):
                with mock.patch('check_pa.xml_reader.Finder.find_item',
                                side_effect=[ibytes, obytes]):
                    with pytest.raises(SystemExit):
                        check.main(verbose=3)

        return check

    @responses.activate
    def test_with_different_ips(self, statefile):

        pa_1 = self.__class__()
        pa_1.host = "192.168.0.1"
        pa_1.interface = "ethernet1/1"

        pa_2 = self.__class__()
        pa_2.host = "192.168.0.2"
        pa_2.interface = "ethernet1/1"

        from nagiosplugin import Cookie

        with Cookie(statefile) as cookie:
            cookie[pa_1.host + pa_1.interface + 'i'] = 0
            cookie[pa_1.host + pa_1.interface + 'o'] = 0
            cookie[pa_1.host + pa_1.interface + 't'] = 1441324800

        check = pa_1.check_pa(1441324800, 10, 10, "throughput1.xml")

        assert check.exitcode == 3
        assert check.state == ServiceState(code=3, text='unknown')
        assert check.summary_str == 'Difference between old timestamp and new timestamp is less or equal 0: If it is the first time you run the script, please execute it again!'

        check = pa_2.check_pa(1441324810, 110, 110, "throughput1.xml")

        assert check.exitcode == 3
        assert check.state == ServiceState(code=3, text='unknown')
        assert check.summary_str == 'Difference between old timestamp and new timestamp is less or equal 0: If it is the first time you run the script, please execute it again!'

        check = pa_1.check_pa(1441324801, 1000000, 1000000, "throughput1.xml")
        assert check.exitcode == 0
        assert check.state == ServiceState(code=0, text='ok')
        # 1000000 Byte = 1 MByte = 8 Mbit in 1 second = 8.0 Mb/s
        assert check.summary_str == 'Input is 8.0 Mb/s - Output is 8.0 ' \
                                    'Mb/s'

        check = pa_2.check_pa(1441324811, 1000000, 1000000, "throughput1.xml")
        assert check.exitcode == 0
        assert check.state == ServiceState(code=0, text='ok')
        # 1000000 Byte = 1 MByte = 8 Mbit in 1 second = 8.0 Mb/s
        assert check.summary_str == 'Input is 8.0 Mb/s - Output is 8.0 ' \
                                    'Mb/s'

    @responses.activate
    def test_new_input_less_than_old(self, statefile):
        file1 = 'throughput1.xml'

        self.interface = 'ethernet1/1'
        interfaces = []
        for interface in self.interface.split(','):
            interfaces.append(interface)

        check = check_pa.modules.throughput.create_check(self)
        objects = []
        for res in check.resources:
            objects.append(res)

        with responses.RequestsMock() as rsps:

            rsps.add(responses.GET,
                     objects[0].xml_obj.build_request_url(),
                     body=utils.read_xml(file1),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            from nagiosplugin import Cookie

            with Cookie(statefile) as cookie:
                cookie[self.host + interfaces[0] + 'i'] = 10
                cookie[self.host + interfaces[0] + 'o'] = 10
                cookie[self.host + interfaces[0] + 't'] = 1441324800

            # Check will be executed exactly ten seconds later
            now = 1441324810

            xml_ibytes = 9
            xml_obytes = 11
            with mock.patch('check_pa.modules.throughput.get_time',
                            return_value=now):
                with mock.patch('check_pa.xml_reader.Finder.find_item',
                                side_effect=[xml_ibytes, xml_obytes]):
                    with pytest.raises(SystemExit):
                        check.main(verbose=3)

            assert check.exitcode == 3
            assert check.state == ServiceState(code=3, text='unknown')
            assert check.summary_str == 'Couldn\'t get a valid value: Found throughput less then old!'

    @responses.activate
    def test_new_output_less_than_old(self, statefile):
        file1 = 'throughput1.xml'

        self.interface = 'ethernet1/1'
        interfaces = []
        for interface in self.interface.split(','):
            interfaces.append(interface)

        check = check_pa.modules.throughput.create_check(self)
        objects = []
        for res in check.resources:
            objects.append(res)

        with responses.RequestsMock() as rsps:

            rsps.add(responses.GET,
                     objects[0].xml_obj.build_request_url(),
                     body=utils.read_xml(file1),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            from nagiosplugin import Cookie

            with Cookie(statefile) as cookie:
                cookie[self.host + interfaces[0] + 'i'] = 10
                cookie[self.host + interfaces[0] + 'o'] = 10
                cookie[self.host + interfaces[0] + 't'] = 1441324800

            # Check will be executed exactly ten seconds later
            now = 1441324810
            xml_ibytes = 11
            xml_obytes = 9

            with mock.patch('check_pa.modules.throughput.get_time',
                            return_value=now):
                with mock.patch('check_pa.xml_reader.Finder.find_item',
                                side_effect=[xml_ibytes, xml_obytes]):
                    with pytest.raises(SystemExit):
                        check.main(verbose=3)

            with Cookie(statefile) as cookie:
                input = cookie.get(self.host + interfaces[0] + 'i')
                output = cookie.get(self.host + interfaces[0] + 'o')
                time = cookie.get(self.host + interfaces[0] + 't')

                assert input == xml_ibytes
                assert output == xml_obytes
                assert time == now

        assert check.exitcode == 3
        assert check.state == ServiceState(code=3, text='unknown')
        assert check.summary_str == 'Couldn\'t get a valid value: Found throughput less then old!'

    @responses.activate
    def test_same_time(self, statefile):
        file1 = 'throughput1.xml'

        self.interface = 'ethernet1/1'
        interfaces = []
        for interface in self.interface.split(','):
            interfaces.append(interface)

        check = check_pa.modules.throughput.create_check(self)
        objects = []
        for resource in check.resources:
            objects.append(resource)

        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET,
                     objects[0].xml_obj.build_request_url(),
                     body=utils.read_xml(file1),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            from nagiosplugin import Cookie

            with Cookie(statefile) as cookie:
                cookie[self.host + interfaces[0] + 'i'] = 10
                cookie[self.host + interfaces[0] + 'o'] = 10
                cookie[self.host + interfaces[0] + 't'] = 1441324800

            # Check will be executed exactly at the same time
            now = 1441324800

            xml_ibytes = 11
            xml_obytes = 10

            with mock.patch('check_pa.modules.throughput.get_time',
                            return_value=now):
                with mock.patch('check_pa.xml_reader.Finder.find_item',
                                side_effect=[xml_ibytes, xml_obytes]):
                    with pytest.raises(SystemExit):
                        check.main(verbose=3)

            assert check.exitcode == 3
            assert check.state == ServiceState(code=3, text='unknown')
            assert check.summary_str == 'Difference between old timestamp ' \
                                        'and new timestamp is less or equal 0: ' \
                                        'If it is the first time you run the ' \
                                        'script, please execute it again!'

    @responses.activate
    def test_api_failed(self, statefile):
        file1 = 'throughput1.xml'

        self.interface = 'ethernet1/1'
        interfaces = []
        for interface in self.interface.split(','):
            interfaces.append(interface)

        check = check_pa.modules.throughput.create_check(self)
        objects = []
        for res in check.resources:
            objects.append(res)

        with responses.RequestsMock() as rsps:

            rsps.add(responses.GET,
                     objects[0].xml_obj.build_request_url(),
                     body=utils.read_xml(file1),
                     status=200,
                     content_type='document',
                     match_querystring=True)

            from nagiosplugin import Cookie

            with Cookie(statefile) as cookie:
                cookie[self.host + interfaces[0] + 'i'] = 10
                cookie[self.host + interfaces[0] + 'o'] = 10
                cookie[self.host + interfaces[0] + 't'] = 1441324800

            # Check will be executed exactly ten seconds later
            now = 1441324810

            xml_ibytes = ""
            xml_obytes = ""

            with mock.patch('check_pa.modules.throughput.get_time',
                            return_value=now):
                with mock.patch('check_pa.xml_reader.Finder.find_item',
                                side_effect=[xml_ibytes, xml_obytes]):
                    with pytest.raises(SystemExit):
                        check.main(verbose=3)

            assert check.exitcode == 3
            assert check.state == ServiceState(code=3, text='unknown')
            assert check.summary_str == 'Couldn\'t get a valid value!'
