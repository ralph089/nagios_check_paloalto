# -*- coding: utf-8 -*-

import logging
import os
import tempfile
import time

import nagiosplugin as np

from check_pa.utils import *
from check_pa.xml_reader import XMLReader, Finder

_log = logging.getLogger('nagiosplugin')
statefile = os.path.join(tempfile.gettempdir(), 'throughput')


def get_time():
    """
    Extract method for mocking time.

    :return: time.time() object
    """
    return time.time()  # pragma: no cover


def create_check(args):
    """
    Creates and configures a check for the throughput command.

    :return: the throughput check.
    """
    interfaces = str(args.interface).split(",")
    check = np.Check()
    for interface in interfaces:
        check.add(Throughput(args.host, args.token, interface))
    for interface in interfaces:
        check.add(np.ScalarContext('inBytes' + interface))
    for interface in interfaces:
        check.add(np.ScalarContext('outBytes' + interface))
    check.add(NetworkSummary())
    return check


def reset():  # pragma: no cover
    """
    Removes the throughput file.
    """
    if os.path.exists(statefile):
        os.remove(os.path.join(tempfile.gettempdir(), 'throughput'))


class Throughput(np.Resource):
    """
    A throughput resource.
    """

    def __init__(self, host, token, interface_name):
        self.host = host
        self.token = token
        self.interface_name = interface_name
        self.cmd = '<show><counter><interface>' + str(
            self.interface_name) + '</interface></counter></show>'
        self.xml_obj = XMLReader(self.host, self.token, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create throughput metrics.

        :return: a throughput metric.
        """

        global api_inbytes, api_outbytes
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())

        current_time = get_time()
        soup = self.xml_obj.read()
        ifnet = soup.find('ifnet')

        for item in ifnet.find_all('entry'):
            api_inbytes = Finder.find_item(item, 'ibytes')
            api_outbytes = Finder.find_item(item, 'obytes')

        _log.debug('Path to statefile: %r' % statefile)
        with np.Cookie(statefile) as cookie:
            old_inbytes = cookie.get(self.interface_name + 'i', api_inbytes)
            old_outbytes = cookie.get(self.interface_name + 'o', api_outbytes)
            old_time = cookie.get(self.interface_name + 't', current_time)

            cookie[self.interface_name + 'i'] = api_inbytes
            cookie[self.interface_name + 'o'] = api_outbytes
            cookie[self.interface_name + 't'] = current_time

        diff_time = int(current_time) - int(old_time)
        if diff_time > 0:
            diff_inbit = round(
                ((float(api_inbytes) - float(old_inbytes)) / diff_time) * 8, 2)
            diff_outbit = round(
                ((float(api_outbytes) - float(old_outbytes)) / diff_time) * 8,
                2)
        else:
            raise np.CheckError(
                'Difference between old timestamp and new timestamp is less '
                'or equal 0: If it is the first time you run the script, '
                'please execute it again!')

        return [
            np.Metric('inBytes' + str(self.interface_name), diff_inbit, 'c',
                      min=0),
            np.Metric('outBytes' + str(self.interface_name), diff_outbit, 'c',
                      min=0)]


class NetworkSummary(np.Summary):
    """
    Creates a throughput summary.
    """

    def __init__(self):
        pass

    def ok(self, results):
        bit_in, bit_out = 0, 0
        for result in results:
            if not str(result).find("inBytes"):
                bit_in += result.metric.value
            else:
                bit_out += result.metric.value
        return 'Input is %s Mb/s - Output is %s Mb/s' % (
            str(Utils.to_mega(bit_in)), str(Utils.to_mega(bit_out)))
