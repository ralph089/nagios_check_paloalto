# -*- coding: utf-8 -*-
import argparse
import sys
import nagiosplugin

sys.path.append('modules')

from check_pa.modules import certificate, throughput, diskspace, useragent, environmental, sessioninfo, thermal, load


@nagiosplugin.guarded
def main():  # pragma: no cover
    args = parse_args(sys.argv[1:])
    if args.reset:
        throughput.reset()
    else:
        check = args.func.create_check(args)
        check.main(verbose=args.verbose, timeout=args.timeout)


def parse_args(args):
    parser = argparse.ArgumentParser(description=__doc__)

    connection = parser.add_argument_group('Connection')
    connection.add_argument('-H', '--host',
                            help='PaloAlto Server Hostname',
                            required=True)
    connection.add_argument('-T', '--token',
                            help='Generated Token for REST-API access',
                            required=True)

    debug = parser.add_argument_group('Debug')
    debug.add_argument('-v', '--verbose', action='count', default=0,
                       help='increase output verbosity (use up to 3 times)')
    debug.add_argument('-t', '--timeout', default=10,
                       help='abort check execution after so many seconds (use 0 for no timeout)')
    debug.add_argument('--reset', action='store_true', help='Deletes the cookie file for the throughput check.')

    info = parser.add_argument_group('Info')
    info.add_argument('--version', action='version',
                      version='%(prog)s 0.3.1')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # Sub-Parser for command 'diskspace'.
    parser_diskspace = subparsers.add_parser('diskspace',
                                             help='check used diskspace.',
                                             )
    parser_diskspace.add_argument('-w', '--warn',
                                  metavar='WARN', type=int, default=85,
                                  help='Warning if diskspace is greater. '
                                       '(default: %(default)s)')
    parser_diskspace.add_argument('-c', '--crit',
                                  metavar='CRIT', type=int, default=95,
                                  help='Critical if disksace is greater. '
                                       '(default: %(default)s)')

    parser_diskspace.set_defaults(func=diskspace)

    # Sub-Parser for command 'certificates'.
    parser_certificates = subparsers.add_parser(
        'certificates',
        help='check the certificate store for '
             'expiring certificates: Outputs is a warning, '
             'if a certificate is in range.')
    parser_certificates.add_argument(
        '-ex', '--exclude', default='', help='exclude certificates from '
                                             'check by name.')
    parser_certificates.add_argument(
        '-r', '--range',
        metavar='RANGE',
        default='0:20',
        help='''
        Warning if days until certificate expiration is in range:
        Represents a threshold range.
        The general format is "[@][start:][end]
        (default: %(default)s)
        ''')
    parser_certificates.set_defaults(func=certificate)

    # Sub-Parser for command 'load'.
    parser_load = subparsers.add_parser(
        'load',
        help='check the CPU load.')
    parser_load.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=85,
        help='Warning if CPU load is greater. (default: %(default)s)')
    parser_load.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=95,
        help='Critical if CPU load is greater. (default: %(default)s)')
    parser_load.set_defaults(func=load)

    # Sub-Parser for command 'useragent'.
    parser_useragent = subparsers.add_parser(
        'useragent',
        help='check for running useragents.')
    parser_useragent.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=60,
        help='Warning if agent is not responding for a given amount of seconds. (default: %(default)s)')
    parser_useragent.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=240,
        help='Critical if agent is not responding for a given amount of seconds. (default: %(default)s)')
    parser_useragent.set_defaults(func=useragent)

    # Sub-Parser for command 'environmental'.
    parser_environmental = subparsers.add_parser(
        'environmental',
        help='check if an alarm is found.')
    parser_environmental.set_defaults(func=environmental)

    # Sub-Parser for command 'sessinfo'.
    parser_sessinfo = subparsers.add_parser(
        'sessinfo',
        help='check important session parameters.')
    parser_sessinfo.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=20000,
        help='Warning if number of sessions is greater. (default: %(default)s)')
    parser_sessinfo.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=50000,
        help='Critical if number of sessions is greater. (default: %(default)s)')
    parser_sessinfo.set_defaults(func=sessioninfo)

    # Sub-Parser for command 'thermal'.
    parser_thermal = subparsers.add_parser(
        'thermal',
        help='check the temperature.')
    parser_thermal.add_argument(
        '-w', '--warn',
        metavar='WARN', type=int, default=40,
        help='Warning if temperature is greater. (default: %(default)s)')
    parser_thermal.add_argument(
        '-c', '--crit',
        metavar='CRIT', type=int, default=45,
        help='Critical if temperature is greater. (default: %(default)s)')
    parser_thermal.set_defaults(func=thermal)

    # Sub-Parser for command 'throughput'.
    parser_throughput = subparsers.add_parser(
        'throughput',
        help='check the throughput.')

    parser_throughput.add_argument(
        '-i', '--interface',
        help='PA interface name, seperate by comma.',
        nargs='?',
        required=True,
    )
    parser_throughput.set_defaults(func=throughput)

    return parser.parse_args(args)


if __name__ == '__main__':  # pragma: no cover
    main()
