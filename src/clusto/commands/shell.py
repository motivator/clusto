#!/usr/bin/env python
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8
#
# Shell command
# Copyright 2009, Ron Gorodetzky <ron@fflick.com>

import sys

import IPython

from clusto import script_helper
from clusto import *


class Shell(script_helper.Script):
    '''
    This is a powerful, interactive clusto shell. The full clusto API
    is available in python idioms.

    Use at your own risk
    '''

    def __init__(self):
        script_helper.Script.__init__(self)

    def run(self, args):
        banner = None
        if IPython.__version__ >= '0.11':
            config=IPython.config.application.Config()
        if not sys.stdin.isatty() or args.files:
            opts = [
                '-noautoindent',
                '-nobanner',
                '-colors', 'NoColor',
                '-noconfirm_exit',
                '-nomessages',
                '-nosep',
                '-prompt_in1', '\x00',
                '-prompt_in2', '\x00',
                '-prompt_out', '\x00',
                '-xmode', 'Plain',
            ]
            if IPython.__version__ >= '0.11':
                config.TerminalInteractiveShell.autoindent = False
                config.TerminalIPythonApp.display_banner = False
                config.TerminalInteractiveShell.color_info = False
                config.TerminalInteractiveShell.confirm_exit = False
                config.TerminalInteractiveShell.quiet = True
                config.TerminalIPythonApp.ignore_old_config = True
                config.TerminalInteractiveShell.separate_in = ''
                config.PromptManager.in_template = '\x00'
                config.PromptManager.in_template1 = '\x00'
                config.PromptManager.in_template2 = '\x00'
                config.PromptManager.out_template = '\x00'
                config.TerminalInteractiveShell.xmode = 'Plain'
        else:
            opts = [
                '-prompt_in1', 'clusto [\#]> ',
                '-prompt_out', 'out [\#]> ',
            ]
            banner = '\nThis is the clusto shell. Respect it.'
            if IPython.__version__ >= '0.11':
                config.PromptManager.in_template = 'clusto [\#]> '
                config.PromptManager.out_template = 'out [\#]> '
        if args.loglevel == 'DEBUG':
            opts.append('-debug')
            config.debug = True

        plugins = script_helper.load_plugins(self.config)
        plugins.update(globals())
        if IPython.__version__ < '0.11':
            from IPython.Shell import IPShellEmbed
            ipshell = IPShellEmbed(opts, user_ns=plugins)
            if banner:
                ipshell.set_banner(banner)
        elif IPython.__version__ < '1.0':
            from IPython.frontend.terminal import embed
            ipshell = embed.InteractiveShellEmbed(banner1=banner,
                config=config, user_ns=plugins)
        else:
            from IPython.terminal import embed
            ipshell = embed.InteractiveShellEmbed(banner1=banner,
                config=config, user_ns=plugins)
        ipshell()

    def _add_arguments(self, parser):
        parser.add_argument('files', nargs='?',
            help='Files to load & run')

    def add_subparser(self, subparsers):
        parser = self._setup_subparser(subparsers)
        self._add_arguments(parser)

def main():
    shell, args = script_helper.init_arguments(Shell)
    return(shell.run(args))

if __name__ == '__main__':
    sys.exit(main())

