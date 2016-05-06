# -*- coding: utf-8 -*-

import logging
from nagiosplugin import CheckError

import nagiosplugin as np

from check_pa.xml_reader import XMLReader

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """

    :return:
    """
    return np.Check(
        UserAgent(args.host, args.token),
        np.ScalarContext('agent_last_heared', args.warn, args.crit),
        UserAgentContext('agent_connected'),
        UserAgentSummary())


class UserAgent(np.Resource):
    def __init__(self, host, token):
        self.host = host
        self.token = token
        self.cmd = '<show><user><user-id-agent><state>all</state>' \
                   '</user-id-agent></user></show>'
        self.xml_obj = XMLReader(self.host, self.token, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create user agent metrics.

        :return: a user agent metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        s = soup.result.string.strip()
        useragents = s.split('\n\n')

        for useragent in useragents:
            agent_details = useragent.split('\n')
            if (len(agent_details) != 31) or not (agent_details[0].startswith('Agent')):
                raise CheckError('Unexpected query result!')

            name = agent_details[0]
            status = agent_details[1].split(':')[1].strip()
            last_heared = int(agent_details[20].split(':')[1].strip())

            _log.info('Checking %s ', name)
            _log.info('Found status %s', status)
            _log.info('Last heared: %i seconds ago', last_heared)
            yield np.Metric(name, status, context='agent_connected')
            yield np.Metric(name, last_heared, context='agent_last_heared')


class UserAgentContext(np.Context):
    def __init__(self, name, fmt_metric='{name} is {valueunit}',
                 result_cls=np.Result):
        super(UserAgentContext, self).__init__(name, fmt_metric,
                                               result_cls)

    def evaluate(self, metric, resource):
        if metric.value == 'conn':
            return self.result_cls(np.Ok, None, metric)
        else:
            return self.result_cls(np.Critical, None, metric)


class UserAgentSummary(np.Summary):
    def ok(self, results):
        return 'All agents are connected and responding.'

    def problem(self, results):
        s = ''
        l = []
        for result in results.results:
            if result.state == np.Warn or result.state == np.Critical:
                if result.metric.context == 'agent_last_heared':
                    l.append("%s last heared: %i seconds ago" % (result.metric.name, result.metric.value))
                if result.metric.context == 'agent_connected':
                    l.append("%s connection status is %s"% (result.metric.name, result.metric.value))
        s += ', '.join(l)
        return s
