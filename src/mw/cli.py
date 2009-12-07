###
# mw - VCS-like nonsense for MediaWiki websites
# Copyright (C) 2009  Ian Weller <ian@ianweller.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
###

import inspect
import mw.clicommands
import os
import sys

class CLI(object):
    def __init__(self):
        self.me = os.path.basename(sys.argv[0])
        self.commands = {}
        self.shortcuts = {}
        for name in mw.clicommands.__dict__:
            if name == 'CommandBase':
                continue
            clazz = mw.clicommands.__dict__[name]
            if isinstance(clazz, type) and \
               issubclass(clazz, mw.clicommands.CommandBase):
                cmd = clazz()
                self.commands[cmd.name] = cmd
                self.shortcuts[cmd.name] = cmd.shortcuts

    def usage(self):
        print 'usage: %s [subcommand]' % self.me
        print
        for name in self.commands:
            cmd = self.commands[name]
            if len(cmd.shortcuts) > 0:
                full = name + ' (' + ' '.join(cmd.shortcuts) + ')'
            else:
                full = name
            print("\t%-14s %-25s" % (full, cmd.description))
        print
        sys.exit(1)

    def main(self):
        # determine what the subcommand is
        if len(sys.argv) > 1:
            if sys.argv[1] in self.commands.keys():
                the_command = sys.argv[1] # SWEET ACTION
            elif sys.argv[1] in ['--help', '-h']:
                self.usage()
            else:
                print '%s: invalid subcommand: %s' % (self.me, sys.argv[1])
                self.usage()
        if len(sys.argv) == 1:
            self.usage()
        # woo let's go
        self.commands[the_command].main()