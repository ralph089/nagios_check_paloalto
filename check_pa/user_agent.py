# -*- coding: utf-8 -*-

import logging
import re
from lxml import etree

import nagiosplugin as np

from check_pa.xml_reader import XMLReader

_log = logging.getLogger('nagiosplugin')


def create_check(args):
    """

    :return:
    """
    return np.Check(
        UserAgent(args.host, args.token),
        np.ScalarContext('useragent'))


class UserAgent(np.Resource):
    def __init__(self, host, token):
        self.host = host
        self.token = token
        self.cmd = '<show><user><user-id-agent><state>all</state>' \
                   '</user-id-agent></user></show>'
        self.xml_obj = XMLReader(self.host, self.token, self.cmd)

    def probe(self):
        """
        Querys the REST-API and create user agent metrics..

        :return: a user agent metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()
        s = soup.result.string
        available_agents = re.findall('(Agent: ).+?(?=( Version :))', s)
        for agent in available_agents:
            _log.info('Agent: %s', agent)


