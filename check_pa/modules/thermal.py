# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np

from check_pa.xml_reader import XMLReader

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """
    Creates and configures a check for the thermal command.

    :return: the thermal check.
    """
    return np.Check(
        Thermal(args.host, args.token),
        np.ScalarContext('temperature', args.warn, args.crit),
        ThermalSummary())


class Thermal(np.Resource):
    def __init__(self, host, token):
        self.host = host
        self.token = token
        self.cmd = '<show><system><environmentals><thermal>' \
                   '</thermal></environmentals></system></show>'
        self.xml_obj = XMLReader(self.host, self.token, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create thermal metrics.

        :return: a disk space metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        entrys = soup.find_all('entry')
        for entry in entrys:
            temp = entry.DegreesC.text
            _log.debug('Temperature: %s', temp)
            maxt = entry.max.text
            _log.debug('Max Temperature: %s', maxt)
            mint = entry.min.text
            _log.debug('Min Temperature: %s', mint)
            desc = entry.description.text
            _log.debug('Description: %s', desc)
            yield np.Metric(desc, float(temp),
                            min=float(mint),
                            max=float(maxt),
                            context='temperature')


class ThermalSummary(np.Summary):
    def ok(self, results):
        l = []
        s = ''
        for temp in results.results:
            l.append('%s is %d degrees Celsius' % (
                temp.metric.name, temp.metric.value))
        s += ', '.join(l)
        return s

    def problem(self, results):
        """
        Prints a more informative output

        :param results: Results container
        :return: status line
        """
        return 'Too high temperature: %s degrees Celsius' % (
            str(results.first_significant))
