# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np

from check_pa.xml_reader import XMLReader, Finder

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """
    Creates and configures a check for the load command.

    :return: the load check.
    """
    return np.Check(
        Load(args.host, args.token),
        np.ScalarContext('load', args.warn, args.crit),
        LoadSummary())


class Load(np.Resource):
    def __init__(self, host, token):
        self.host = host
        self.token = token
        self.cmd = '<show><running><resource-monitor><minute><last>1<%2Flast' \
                   '>' \
                   '<%2Fminute><%2Fresource-monitor><%2Frunning><%2Fshow>'
        self.xml_obj = XMLReader(self.host, self.token, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create load metrics.

        :return: a load metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        cpuavg = soup.find('cpu-load-average')

        for entry in cpuavg.find_all('entry'):
            coreid = int(Finder.find_item(entry, 'coreid'))
            cpu_load = float(Finder.find_item(entry, 'value'))
            yield np.Metric('CPU%d' % coreid, cpu_load, '%', min=0, max=100,
                            context='load')


class LoadSummary(np.Summary):
    def ok(self, results):
        l = []
        for cpu in results.results:
            s = '%s: %s%%' % (cpu.metric.name, cpu.metric.value)
            _log.debug('Add result %r', s)
            l.append(s)
        _log.debug('CPU count: %d' % len(l))
        output = ", ".join(l)
        return str(output)
