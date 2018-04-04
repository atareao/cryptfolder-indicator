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

import gi
try:
    gi.require_version('Gtk', '3.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk


class BoxedSwitch(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.set_spacing(5)
        self.switch = Gtk.Switch()
        self.pack_start(self.switch, False, False, 0)

    def set_active(self, active):
        self.switch.set_active(active)

    def get_active(self):
        return self.switch.get_active()
