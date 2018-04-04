#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# This file is part of CryptFolder-Indicator
#
# Copyright (C) 2011 - 2018 Lorenzo Carbonell Cerezo
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import codecs
import os
import json

import com


class Configuration(object):
    def __init__(self):
        self.params = com.PARAMS
        self.read()

    def get(self, key):
        try:
            return self.params[key]
        except KeyError as e:
            print(e)
            self.params[key] = com.PARAMS[key]
            return self.params[key]

    def set(self, key, value):
        self.params[key] = value

    def reset(self):
        if os.path.exists(com.CONFIG_FILE):
            os.remove(com.CONFIG_FILE)
        self.params = com.PARAMS
        self.save()

    def set_defaults(self):
        self.params = com.PARAMS
        self.save()

    def read(self):
        try:
            f = codecs.open(com.CONFIG_FILE, 'r', 'utf-8')
        except IOError as e:
            print(e)
            self.save()
            f = codecs.open(com.CONFIG_FILE, 'r', 'utf-8')
        try:
            self.params = json.loads(f.read())
        except ValueError as e:
            print(e)
            self.save()
        f.close()

    def save(self):
        if not os.path.exists(com.CONFIG_APP_DIR):
            os.makedirs(com.CONFIG_APP_DIR)
        f = codecs.open(com.CONFIG_FILE, 'w', 'utf-8')
        f.write(json.dumps(self.params, indent=4, sort_keys=True))
        f.close()

    def __str__(self):
        ans = ''
        for key in sorted(self.params.keys()):
            ans += '{0}: {1}\n'.format(key, self.params[key])
        return ans
