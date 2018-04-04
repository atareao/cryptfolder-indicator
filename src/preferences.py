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
from configurator import Configuration
from boxedswitch import BoxedSwitch
from com import _


def set_autostart(autostart):
    if os.path.exists(com.FILE_AUTO_START) and\
            not os.path.islink(com.FILE_AUTO_START):
        os.remove(com.FILE_AUTO_START)
    if autostart is True:
        if not os.path.islink(com.FILE_AUTO_START):
            os.symlink(com.FILE_AUTO_START_SRC, com.FILE_AUTO_START)
    else:
        if os.path.islink(com.FILE_AUTO_START):
            os.remove(com.FILE_AUTO_START)


class Preferences(Gtk.Dialog):
    def __init__(self):
        self.configurator = Configuration()
        Gtk.Dialog.__init__(self,
                            'CryptFolder Indicator | ' + _('Preferences'),
                            None,
                            Gtk.DialogFlags.MODAL |
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (Gtk.STOCK_CANCEL,
                             Gtk.ResponseType.REJECT,
                             Gtk.STOCK_OK,
                             Gtk.ResponseType.ACCEPT))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_size_request(500, 150)
        self.connect('close', self.close_application)
        self.set_icon_from_file(com.ICON)

        vbox1 = Gtk.VBox(spacing=5)
        vbox1.set_border_width(5)
        self.get_content_area().add(vbox1)

        frame1 = Gtk.Frame()
        vbox1.add(frame1)

        grid = Gtk.Grid()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_left(10)
        grid.set_margin_right(10)
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)
        frame1.add(grid)

        label = Gtk.Label(_('Autostart'))
        label.set_alignment(0, 0.5)
        grid.attach(label, 0, 0, 1, 1)

        self.checkbutton1 = BoxedSwitch()
        grid.attach(self.checkbutton1, 1, 0, 1, 1)

        label = Gtk.Label(_('Mount selected folders at start'))
        label.set_alignment(0, 0.5)
        grid.attach(label, 0, 1, 1, 1)

        self.checkbutton2 = BoxedSwitch()
        grid.attach(self.checkbutton2, 1, 1, 1, 1)

        label1 = Gtk.Label(label=_('Select icon theme') + ':')
        label1.set_alignment(0, 0.5)
        grid.attach(label1, 0, 2, 1, 1)
        self.radiobutton0 = Gtk.RadioButton(group=None,
                                            label=_('Normal'))
        grid.attach(self.radiobutton0, 1, 2, 1, 1)
        self.radiobutton1 = Gtk.RadioButton(group=self.radiobutton0,
                                            label=_('Light'))
        grid.attach(self.radiobutton1, 2, 2, 1, 1)
        self.radiobutton2 = Gtk.RadioButton(group=self.radiobutton0,
                                            label=_('Dark'))
        grid.attach(self.radiobutton2, 3, 2, 1, 1)

        self.load_preferences()
        self.show_all()

    def close_application(self, widget, event):
        self.destroy()

    def close_ok(self):
        self.hide()

    def save(self):
        set_autostart(self.checkbutton1.get_active())
        self.configurator.set('mount_folders_on_start',
                              self.checkbutton2.get_active())
        if self.radiobutton0.get_active() is True:
            option = 'normal'
        elif self.radiobutton1.get_active()is True:
            option = 'light'
        else:
            option = 'dark'
        self.configurator.set('theme', option)
        self.configurator.save()

    def load_preferences(self):
        if os.path.exists(com.FILE_AUTO_START) and\
                not os.path.islink(com.FILE_AUTO_START):
            os.remove(com.FILE_AUTO_START)
        self.checkbutton1.set_active(os.path.islink(com.FILE_AUTO_START))
        self.checkbutton2.set_active(
            self.configurator.get('mount_folders_on_start'))
        option = self.configurator.get('theme')
        if option == 'normal':
            self.radiobutton0.set_active(True)
        elif option == 'light':
            self.radiobutton1.set_active(True)
        else:
            self.radiobutton2.set_active(True)


if __name__ == "__main__":
    cm = Preferences()
    if cm.run() == Gtk.ResponseType.ACCEPT:
        cm.hide()
        cm.save()
    cm.destroy()
    exit(0)
