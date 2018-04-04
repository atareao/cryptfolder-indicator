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
import os
import com


class FolderItem(Gtk.ImageMenuItem):
    def __init__(self, folder, theme):
        Gtk.ImageMenuItem.__init__(self)
        self.folder = folder
        self.set_tooltip_text(folder['path_mount'])
        self.set_label(os.path.basename(folder['path_mount']))
        self.set_theme(theme)

    def set_theme(self, theme):
        self.theme = theme
        if theme == 'normal':
            self.ICON_OPEN = com.ICON_OPEN
            self.ICON_CLOSED = com.ICON_CLOSED
        elif theme == 'light':
            self.ICON_OPEN = com.ICON_OPEN_L
            self.ICON_CLOSED = com.ICON_CLOSED_L
        else:
            self.ICON_OPEN = com.ICON_OPEN_D
            self.ICON_CLOSED = com.ICON_CLOSED_D
        self.set_mounted()

    def set_mounted(self, mounted=None):
        if mounted is None:
            mounted = self.folder['mounted']
        else:
            self.folder['mounted'] = mounted
        if mounted:
            image = Gtk.Image.new_from_file(self.ICON_OPEN)
        else:
            image = Gtk.Image.new_from_file(self.ICON_CLOSED)
        self.set_image(image)
        self.set_always_show_image(True)



