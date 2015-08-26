#!/usr/bin/env python
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8

import argparse
import sys

import clusto
from clusto import script_helper

class Reboot(script_helper.Script):
    '''
    This will reboot a given server or IP address
    '''

    def __init__(self):
        script_helper.Script.__init__(self)

    def _add_arguments(self, parser):
        parser.add_argument('--batch', action='store_true', default=False,
            help='Batch mode, don\'t prompt for confirmation')
        parser.add_argument('--method', default=None,
            help='Use the given method to reboot this server (eg. ipmi)')
        parser.add_argument('server', nargs='+',
            help='Server name or IP address')

    def add_subparser(self, subparsers):
        parser = self._setup_subparser(subparsers)
        self._add_arguments(parser)

    def confirm(self, server):
        print 'Parents: %s' % ' '.join([x.name for x in server.parents()])
        response = raw_input('Are you sure you want to reboot %s (yes/no)? ' % server.name)
        if response == 'yes':
            return True
        else:
            return False

    def run(self, args):
        for name in args.server:
            server = clusto.get(name)
            if not server:
                self.error('%s does not exist' % name)
                continue

            server = server[0]

            if not hasattr(server, 'reboot'):
                self.error('%s does not implement reboot()' % server.name)
                return -1

            if not args.batch:
                if not self.confirm(server):
                    return -1

            kwargs = {}
            if args.method is not None:
                kwargs['method'] = args.method
            server.reboot(**kwargs)


def main():
    reboot = Reboot()
    parent_parser = script_helper.setup_base_parser()
    this_parser = argparse.ArgumentParser(parents=[parent_parser],
        description=reboot._get_description())
    reboot._add_arguments(this_parser)
    args = this_parser.parse_args()
    reboot.init_script(args=args, logger=script_helper.get_logger(args.loglevel))
    return(reboot.run(args))


if __name__ == '__main__':
    sys.exit(main())

