#!/usr/bin/env python
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8
#
# Shell command
# Copyright 2010, Jeremy Grosser <synack@digg.com>

import os
import sys

import clusto
from clusto import script_helper


class Console(script_helper.Script):
    '''
    Use clusto's hardware port mappings to console to a remote server
    using the serial console.
    '''

    def __init__(self):
        script_helper.Script.__init__(self)

    def _add_arguments(self, parser):
        parser.add_argument('--user', '-u',
            help='SSH User (you can also set this in clusto.conf '
                 'in console.user: --user > clusto.conf:console.user')
        parser.add_argument('--force', '-f', action='store_true',
            default=False, help='Force taking over the console session')
        parser.add_argument('server', nargs=1,
            help='Object to console to (IP or name)')

    def run(self, args):
        try:
            server = clusto.get(args.server[0])
            if not server:
                raise LookupError('Object "%s" does not exist' % args.server)
        except Exception as e:
            self.debug(e)
            self.error('No object like "%s" was found' % args.server)
            return 1
        server = server[0]

        if not hasattr(server, 'console'):
            self.error('The object %s lacks a console method' % server.name)
            return 2

        user = os.environ.get('USER')
        if args.user:
            self.debug('Grabbing user from parameter')
            user = args.user
        else:
            self.debug('Grabbing user from config file or default')
            user = self.get_conf('console.user', user)
        self.debug('User is "%s"' % user)
        return(server.console(ssh_user=user))


def main():
    console, args = script_helper.init_arguments(Console)
    return(console.run(args))

if __name__ == '__main__':
    sys.exit(main())

