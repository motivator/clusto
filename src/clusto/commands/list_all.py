#!/usr/bin/env python
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8

import sys

import clusto
from clusto import script_helper


class ListAll(script_helper.Script):
    '''
    Lists all entities of a type
    '''

    def __init__(self):
        script_helper.Script.__init__(self)

    def _add_arguments(self, parser):
        parser.add_argument('--type', default=None, action='store',
            dest='clusto_type', help='Type of entities to show')

    def run(self, args):
        if args.clusto_type is None:
            clusto_types = []
        else:
            clusto_types = [args.clusto_type]
        for entity in clusto.get_entities(clusto_types=clusto_types):
            print entity.name


def main():
    lp, args = script_helper.init_arguments(ListAll)
    return(lp.run(args))

if __name__ == '__main__':
    sys.exit(main())

