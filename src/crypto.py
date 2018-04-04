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
    gi.require_version('GLib', '2.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import GLib
from cryptmanager import CryptManager
from createcryptfolder import CreateCryptFolder
from com import _
import com
import gnomecryfsmod


class CM(Gtk.Dialog):
    def __init__(self):
        self.location = None
        Gtk.Dialog.__init__(self,
                            _('CryptFolder'),
                            None,
                            Gtk.DialogFlags.MODAL |
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.connect('destroy', self.close_application)
        self.set_icon_from_file(com.ICON)
        self.cryptmanager = CryptManager()

        vbox = Gtk.VBox(spacing=5)
        vbox.set_border_width(5)
        self.get_content_area().add(vbox)

        frame = Gtk.Frame()
        vbox.add(frame)

        vbox1 = Gtk.VBox(spacing=5)
        vbox1.set_border_width(5)
        frame.add(vbox1)
        hbox1 = Gtk.HBox(spacing=5)
        hbox1.set_border_width(5)
        vbox1.pack_start(hbox1, True, True, 0)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                                  Gtk.PolicyType.AUTOMATIC)
        scrolledwindow.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)
        scrolledwindow.set_size_request(750, 300)
        hbox1.pack_start(scrolledwindow, True, True, 0)

        self.model = Gtk.ListStore(str, str, bool, bool)

        self.treeview = Gtk.TreeView()
        self.treeview.set_model(self.model)
        scrolledwindow.add(self.treeview)

        self.column_ucrypt = Gtk.TreeViewColumn(_('Unencrypted folder'))
        self.column_crypt = Gtk.TreeViewColumn(_('Encrypted folder'))
        self.column_mou = Gtk.TreeViewColumn(_('Mounted'))
        self.column_aut = Gtk.TreeViewColumn(_('Automount'))

        self.cell_ucrypt = Gtk.CellRendererText()
        self.cell_crypt = Gtk.CellRendererText()
        self.cell_mou = Gtk.CellRendererToggle()
        self.cell_aut = Gtk.CellRendererToggle()

        self.cell_ucrypt.set_property('editable', False)
        self.cell_crypt.set_property('editable', False)
        self.cell_mou.set_property('activatable', True)
        self.cell_aut.set_property('activatable', True)
        self.cell_mou.connect('toggled',
                              self.toggled,
                              (self.model, 0))
        self.cell_aut.connect('toggled',
                              self.toggled_automount,
                              (self.model, 1))
        self.column_ucrypt.pack_start(self.cell_ucrypt, True)
        self.column_crypt.pack_start(self.cell_crypt, True)
        self.column_mou.pack_start(self.cell_mou, True)
        self.column_aut.pack_start(self.cell_aut, True)

        self.column_ucrypt.add_attribute(self.cell_ucrypt, 'text', 0)
        self.column_crypt.add_attribute(self.cell_crypt, 'text', 1)
        self.column_mou.add_attribute(self.cell_mou, 'active', 2)
        self.column_aut.add_attribute(self.cell_aut, 'active', 3)

        self.treeview.append_column(self.column_ucrypt)
        self.treeview.append_column(self.column_crypt)
        self.treeview.append_column(self.column_mou)
        self.treeview.append_column(self.column_aut)

        vbox2 = Gtk.VBox(spacing=5)
        vbox2.set_border_width(5)
        hbox1.pack_start(vbox2, False, False, 0)

        button_add = Gtk.Button()
        image_add = Gtk.Image()
        image_add.set_from_stock(Gtk.STOCK_ADD, Gtk.IconSize.LARGE_TOOLBAR)
        button_add.set_image(image_add)
        button_add.connect('clicked', self.on_button_add_clicked)
        button_add.set_tooltip_text(_('Add new encrytped folder'))
        vbox2.pack_start(button_add, False, False, 0)

        button_remove = Gtk.Button()
        image_remove = Gtk.Image()
        image_remove.set_from_stock(Gtk.STOCK_REMOVE,
                                    Gtk.IconSize.LARGE_TOOLBAR)
        button_remove.set_image(image_remove)
        button_remove.connect('clicked', self.on_button_remove_clicked)
        button_remove.set_tooltip_text(_('Remove encrytped folder from \
indicator but not delete'))
        vbox2.pack_start(button_remove, False, False, 0)

        button_edit = Gtk.Button()
        image_edit = Gtk.Image()
        image_edit.set_from_stock(Gtk.STOCK_EDIT, Gtk.IconSize.LARGE_TOOLBAR)
        button_edit.set_image(image_edit)
        button_edit.connect('clicked', self.on_button_edit_clicked)
        button_edit.set_tooltip_text(_('Edit encrypted folder properties'))
        vbox2.pack_start(button_edit, False, False, 0)

        self.show_all()

        self.load_preferences()

        if self.run() == Gtk.ResponseType.ACCEPT:
            self.ok = True
        else:
            self.ok = False
        self.destroy()

    def on_button_add_clicked(self, widget):
        widget.set_sensitive(False)
        ccf = CreateCryptFolder(self)
        if ccf.run() == Gtk.ResponseType.ACCEPT:
            GLib.idle_add(ccf.hide)
            path_base = ccf.get_path_base()
            path_mount = ccf.get_path_mount()
            secret = ccf.get_secret()
            automount = ccf.get_automount()
            autodelete = ccf.get_autodelete()
            try:
                self.cryptmanager.add_folder(path_base, path_mount, secret,
                                             autodelete, automount)
                self.load_preferences()
            except gnomecryfsmod.AlreadyExists as e:
                print(e)
                dialog = Gtk.MessageDialog(self, Gtk.DialogFlags.MODAL,
                                           Gtk.MessageType.INFO,
                                           buttons=Gtk.ButtonsType.OK)
                dialog.set_markup('<b>%s</b>' % _('CryptFolder-Indicator'))
                dialog.format_secondary_markup(_('This folder is already \
encrypted'))
                dialog.run()
                dialog.destroy()
            except gnomecryfsmod.BadPassword as e:
                print(e)
                dialog = Gtk.MessageDialog(self, Gtk.DialogFlags.MODAL,
                                           Gtk.MessageType.INFO,
                                           buttons=Gtk.ButtonsType.OK)
                dialog.set_markup('<b>%s</b>' % _('CryptFolder-Indicator'))
                dialog.format_secondary_markup(_('The password is wrong'))
                dialog.run()
                dialog.destroy()
        ccf.destroy()
        widget.set_sensitive(True)

    def on_button_edit_clicked(self, widget):
        if len(self.treeview.get_selection().get_selected_rows()[1]) > 0:
            widget.set_sensitive(False)
            row = self.treeview.get_selection().get_selected_rows()[1][0]
            print('row:', row)
            path = self.model[row][1]
            print('path:', path)
            folders = self.cryptmanager.get_folders()
            if path in folders:
                folder = folders[path]
                ccf = CreateCryptFolder(self, folder)
                if ccf.run() == Gtk.ResponseType.ACCEPT:
                    GLib.idle_add(ccf.hide)

                    path_base = folder['path_base']

                    new_path_base = ccf.get_path_base()
                    new_path_mount = ccf.get_path_mount()
                    new_secret = ccf.get_secret()
                    new_automount = ccf.get_automount()
                    new_autodelete = ccf.get_autodelete()

                    self.cryptmanager.edit_folder(path_base, new_path_base,
                                                  new_path_mount, new_secret,
                                                  new_autodelete,
                                                  new_automount)
                    self.load_preferences()
                ccf.destroy()
            widget.set_sensitive(True)

    def on_button_remove_clicked(self, widget):
        if self.treeview.get_selection().count_selected_rows() > 0:
            widget.set_sensitive(False)

            row = self.treeview.get_selection().get_selected_rows()[1][0]
            path = self.model[row][2]
            print(path)
            msg = _('Are you sure to remove from CryptFolder-Indicator \
this encrypted\n folder? %s') % (path)
            md = Gtk.MessageDialog(
                parent=self,
                flags=Gtk.DialogFlags.MODAL |
                Gtk.DialogFlags.DESTROY_WITH_PARENT,
                type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO,
                message_format=msg)
            if md.run() == Gtk.ResponseType.YES:
                self.cryptmanager.remove_folder(path)
            md.destroy()

            self.load_preferences()
            widget.set_sensitive(True)

    def toggled_automount(self, widget, row, liststore):
        before = liststore[0][row][3]
        after = not before
        liststore[0][row][3] = after
        path = liststore[0][row][1]
        self.cryptmanager.set_automount(path, after)

    def toggled(self, widget, row, liststore):
        before = liststore[0][row][2]
        after = not before
        liststore[0][row][2] = after
        path = liststore[0][row][1]
        if after is True:
            self.cryptmanager.mount(path)
        else:
            self.cryptmanager.unmount(path)

    def close_application(self, widget):
        self.ok = False
        self.destroy()

    def load_preferences(self):
        self.model.clear()
        folders = self.cryptmanager.get_folders()
        for index, base in enumerate(folders.keys()):
            print(index, folders[base])
            self.model.append([folders[base]['path_mount'],
                               base,
                               self.cryptmanager.is_mounted(base),
                               folders[base]['automount']])

    def save_preferences(self):
        pass


if __name__ == "__main__":
    cm = CM()
    exit(0)
