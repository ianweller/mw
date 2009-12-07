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

import ConfigParser
import json
import os
import sys
import time

class Metadir(object):
    def __init__(self):
        self.me = os.path.basename(sys.argv[0])
        root = os.getcwd()
        while True:
            if '.mw' in os.listdir(root):
                self.root = root
                break
            (head, tail) = os.path.split(root)
            if head == root:
                self.root = os.getcwd()
                break
            root = head
        self.location = os.path.join(self.root, '.mw')
        self.config_loc = os.path.join(self.location, 'config')
        if os.path.isdir(self.location) and \
           os.path.isfile(self.config_loc):
            self.config = ConfigParser.RawConfigParser()
            self.config.read(self.config_loc)
        else:
            self.config = None

    def create(self, api_url):
        # create the directory
        try:
            os.mkdir(self.location, 0755)
        except OSError, e:
            print '%s: you are already in a mw repo' % self.me
            sys.exit(1)
        # create config
        self.config = ConfigParser.RawConfigParser()
        self.config.add_section('remote')
        self.config.set('remote', 'api_url', api_url)
        with open(self.config_loc, 'wb') as config_file:
            self.config.write(config_file)
        # create cache
        os.mkdir(os.path.join(self.location, 'cache'))
        # create cache/page
        fd = file(os.path.join(self.location, 'cache', 'page'), 'w')
        fd.write(json.dumps({}))
        # create cache/rv
        fd = file(os.path.join(self.location, 'cache', 'rv'), 'w')
        fd.write(json.dumps({}))

    def add_page_info(self, pageid, pagename, rvids):
        lulz = file(os.path.join(self.location, 'cache', 'page'), 'r')
        conf = json.loads(lulz.read())
        conf[pageid] = {'name': pagename, 'rv': rvids}
        fd = file(os.path.join(self.location, 'cache', 'page'), 'w')
        fd.write(json.dumps(conf))

    def add_rv_info(self, rv):
        lulz = file(os.path.join(self.location, 'cache', 'rv'), 'r')
        conf = json.loads(lulz.read())
        rvid = int(rv['revid'])
        conf[rvid] = {
                'user': rv['user'], 'timestamp': rv['timestamp'],
                'content': rv['*']
        }
        conf[rvid]['minor'] = 'minor' in rv
        if 'comment' in rv:
            conf[rvid]['comment'] = rv['comment']
        else:
            conf[rvid]['comment'] = None
        fd = file(os.path.join(self.location, 'cache', 'rv'), 'w')
        fd.write(json.dumps(conf))