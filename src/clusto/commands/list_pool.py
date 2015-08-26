#!/usr/bin/env python
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8

from IPy import IP
import sys

import clusto
from clusto import script_helper


class ListPool(script_helper.Script):
    '''
    Lists servers that are part of two given pools.
    '''

    def __init__(self):
        script_helper.Script.__init__(self)

    def _add_arguments(self, parser):
        parser.add_argument('--names', default=False, action='store_true',
            help='Print names instead of ip addresses (defaults to False)')
        parser.add_argument('--recursive', default=False, action='store_true',
            help='Search resursively on both pools (defaults to False)')
        parser.add_argument('--type', default=None,
            help='Restrict results to the given type')
        parser.add_argument('pool', nargs='+', metavar='pool',
            help='Pool(s) to query')

    def run(self, args):
        serverset = None
        for pool in args.pool:
            pool = clusto.get_by_name(pool)
            contents = pool.contents(search_children=args.recursive)
            if args.type:
                contents = [x for x in contents if x.type == args.type]
            contents = set(contents)

            if serverset is None:
                serverset = contents
            else:
                serverset = serverset.intersection(pool)

        for server in serverset:
            if args.names:
                print server.name
            else:
                try:
                    ip = server.get_ips()
                    ip.sort(key=lambda x: IP(x))
                except Exception, e:
                    self.debug(e)
                    ip = None

                if ip:
                    print ' '.join(ip)
                else:
                    print server.name


def main():
    lp, args = script_helper.init_arguments(ListPool)
    return(lp.run(args))

if __name__ == '__main__':
    sys.exit(main())

