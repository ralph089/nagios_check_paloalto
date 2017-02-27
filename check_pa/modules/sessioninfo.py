# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np

from check_pa.xml_reader import XMLReader, Finder

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """
    Creates and configures a check for the sessioninfo command.

    :return: the sessioninfo check.
    """
    return np.Check(
        SessInfo(args.host, args.token),
        np.ScalarContext('session', args.warn, args.crit),
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
        Querys the REST-API and create session info metrics.

        :return: a sessioninfo metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        result = soup.result
        maxsess = int(Finder.find_item(result, 'num-max'))
        actsess = int(Finder.find_item(result, 'num-active'))
        throughput = int(Finder.find_item(result, 'kbps'))

        return [np.Metric('session', actsess, min=0, max=maxsess, context='session'),
                np.Metric('throughput_kbps', throughput, min=0, context='throughput')]


class SessSummary(np.Summary):
    def ok(self, results):
        return 'Active sessions: ' + str(
            results['session'].metric) + ' / Throughput (kbps): ' + str(
            results['throughput_kbps'].metric)
