# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np

from check_pa.xml_reader import XMLReader

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """
    Creates and configures a check for the environmental command.

    :return: the environmental check.
    """
    return np.Check(
        Environmental(args.host, args.token),
        EnvironmentalContext('alarm'),
        EnvironmentalSummary())


class Environmental(np.Resource):
    """Reads the used disk space of the Palo Alto Firewall System."""

    def __init__(self, host, token):
        self.host = host
        self.token = token
        self.cmd = '<show><system><environmentals>' \
                   '</environmentals></system></show>'
        self.xml_obj = XMLReader(self.host, self.token, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create disk space metrics.

        :return: a disk space metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        entrys = soup.find_all('entry')
        for entry in entrys:
            if entry.alarm.text == 'True':
                _log.debug('Alarm found: %s' % entry.description)
                yield np.Metric(entry.description.text, True, context='alarm')
            yield np.Metric(entry.description.text, False, context='alarm')


class EnvironmentalContext(np.Context):
    def __init__(self, name, fmt_metric='{name} is {valueunit}',
                 result_cls=np.Result):
        super(EnvironmentalContext, self).__init__(name, fmt_metric,
                                                   result_cls)

    def evaluate(self, metric, resource):
        if not metric.value:
            return self.result_cls(np.Ok, None, metric)
        else:
            return self.result_cls(np.Critical, None, metric)


class EnvironmentalSummary(np.Summary):
    def ok(self, results):
        return 'No alarms found.'

    def problem(self, results):
        s = 'Alarm(s) found: '
        l = []
        for alarm in results.results:
            if alarm.metric.value:
                l.append(alarm.metric.name)
        s += ', '.join(l)
        return s
