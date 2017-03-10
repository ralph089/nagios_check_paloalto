# -*- coding: utf-8 -*-

import logging

import nagiosplugin as np
from datetime import datetime

from check_pa.xml_reader import XMLReader, Finder

_log = logging.getLogger('nagiosplugin')


def get_now():
    """
    Extract method for mocking datetime.now.

    :return: datetime.today() object
    """
    return datetime.today()  # pragma: no cover


def create_check(args):
    """
    Creates and configures a check for the certificate command.

    :return: the throughput check.
    """
    return np.Check(
        Certificate(args.host, args.token, args.exclude),
        CertificateContext('certificates', args.range),
        CertificateSummary(args.range))


class Certificate(np.Resource):
    """
    Will fetch the certificates from the REST API and returns a warning if
    the remaining days of the certificate is between the value of warning
    (e. g. 20) and critical (e. g. 0).

    If a certificate has been revoked or excluded, no warning will appear.
    """

    def __init__(self, host, token, exclude):
        self.host = host
        self.token = token
        self.cmd = '<show><config><running>' \
                   '<xpath>shared/certificate</xpath>' \
                   '</running></config></show>'
        self.xml_obj = XMLReader(self.host, self.token, self.cmd)
        self.exclude = str(exclude).split(",")

    def probe(self):
        """
        Querys the REST-API and create certificate metrics.

        :return: a certificate metric.
        """
        _log.info('Reading XML from: %s', self.xml_obj.build_request_url())
        soup = self.xml_obj.read()

        certificates = soup.find_all('entry')

        for certificate in certificates:
            not_valid_after = Finder.find_item(certificate,
                                             'not-valid-after').replace(
                "GMT", "").strip()
            date_object = datetime.strptime(not_valid_after, '%b %d %H:%M:%S %Y')
            difference = date_object - get_now()
            _log.debug('Certificate %s difference: %s days' % (
                certificate.get('name'), difference.days))
            try:
                status = Finder.find_item(certificate, 'status')
            except np.CheckError:
                status = ""
            if certificate.get('name') not in self.exclude:
                if status != "revoked":
                    yield np.Metric(certificate.get('name'), difference.days,
                                    context='certificates')


class CertificateContext(np.Context):
    def __init__(self, name, r,
                 fmt_metric='{name} expires in {valueunit}',
                 result_cls=np.Result):
        super(CertificateContext, self).__init__(name, fmt_metric, result_cls)
        self.r = np.Range(r)

    def evaluate(self, metric, resource):
        """Output depending on given start and end range.

        Returns a warning, if a certificate is between given start and end
        range.
        Returns ok, if a certificate is out of range.

        :param metric:
        :param resource:
        :return:
        """
        if self.r.match(metric.value):
            return self.result_cls(np.Warn, None, metric)
        else:
            return self.result_cls(np.Ok, None, metric)


class CertificateSummary(np.Summary):
    def __init__(self, r):
        self.r = np.Range(r)

    def ok(self, results):
        l = []
        for result in results:
            l.append(result.metric.value)
        output = 'The next certificate will expire in %s days.' % min(l)
        return str(output)

    def problem(self, results):
        l = []
        for result in results:
            if self.r.match(result.metric.value):
                l.append(str(result) + ' days')
        output = ", ".join(l)
        return str(output)
