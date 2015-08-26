#!/usr/bin/env python
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8

import sys

import clusto
from clusto import script_helper


class InitDB(script_helper.Script):
    '''
    Initialize the clusto database
    '''

    def __init__(self):
        script_helper.Script.__init__(self)

    def run(self, args):
        try:
            clusto.init_clusto()
        except Exception, e:
            print 'Error creating clusto database: %s' % str(e)
            return -1

def main():
    initdb, args = script_helper.init_arguments(InitDB)
    return(initdb.run(args))

if __name__ == '__main__':
    sys.exit(main())

