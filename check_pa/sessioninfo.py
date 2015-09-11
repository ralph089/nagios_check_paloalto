# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np

from check_pa.xml_reader import XMLReader, Finder

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """

    :return:
    """
    return np.Check(
        SessInfo(args.host, args.token),
        np.ScalarContext('maxsess'),
        np.ScalarContext('actsess'),
        np.ScalarContext('throughput'),
        SessSummary())


class SessInfo(np.Resource):
    def __init__(self, host, token):
        self.host = host
        self.token = token
        self.cmd = '<show><session><info></info></session></show>'
        self.xml_obj = XMLReader(self.host, self.token, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create thermal metrics.

        :return: a disk space metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        result = soup.result
        maxsess = int(Finder.find_item(result, 'num-max'))
        actsess = int(Finder.find_item(result, 'num-active'))
        throughput = int(Finder.find_item(result, 'kbps'))

        return [np.Metric('maxsess', maxsess, min=0),
                np.Metric('actsess', actsess, min=0),
                np.Metric('throughput', throughput, 'kbps', min=0)]


class SessSummary(np.Summary):
    def ok(self, results):
        return 'Max possible sessions: ' + str(
            results['maxsess'].metric) + ' / Active sessions: ' + str(
            results['actsess'].metric) + ' / Throughput: ' + str(
            results['throughput'].metric)
