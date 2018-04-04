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
from com import _
from boxedswitch import BoxedSwitch
from cfkeyringmanager import CFIPasswordManager


class CreateCryptFolder(Gtk.Dialog):
    def __init__(self, parent, crypt_folder=None):

        Gtk.Dialog.__init__(
            self, _('CryptFolder'), parent,
            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_size_request(620, 190)
        self.connect('destroy', self.close_application)
        self.set_icon_from_file(com.ICON)

        self.button_ok = self.add_button(_('Aceptar'), Gtk.ResponseType.ACCEPT)
        self.button_ok.set_sensitive(False)
        self.button_cancel = self.add_button(_('Cancelar'),
                                             Gtk.ResponseType.CANCEL)
        self.button_cancel.connect('clicked', self._close)
        vbox = Gtk.VBox(spacing=5)
        vbox.set_border_width(5)
        self.get_content_area().add(vbox)

        grid = Gtk.Grid()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_left(10)
        grid.set_margin_right(10)
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)
        vbox.pack_start(grid, False, False, 0)

        label1 = Gtk.Label(label=_('Unencrypted folder') + ':')
        label1.set_width_chars(20)
        label1.set_alignment(0, 0.5)
        grid.attach(label1, 0, 0, 1, 1)

        self.entry1 = Gtk.Entry()
        self.entry1.connect('changed', self.on_unencripted_folder_changed)
        self.entry1.connect('changed', self.update_warning)
        self.entry1.set_editable(False)
        self.entry1.set_width_chars(50)
        grid.attach(self.entry1, 2, 0, 1, 1)

        button1 = Gtk.Button()
        image1 = Gtk.Image()
        image1.set_from_stock(Gtk.STOCK_DIRECTORY, Gtk.IconSize.MENU)
        button1.set_image(image1)
        button1.connect('clicked', self.on_button_1_clicked)
        grid.attach(button1, 3, 0, 1, 1)

        label2 = Gtk.Label(label=_('Encrypted folder') + ':')
        label2.set_width_chars(20)
        label2.set_alignment(0, 0.5)
        grid.attach(label2, 0, 1, 1, 2)

        self.entry2_rb1 = Gtk.RadioButton()
        self.entry2_rb1.connect('toggled', self.on_entry2_rb1_get_active)
        self.entry2_rb1.connect('toggled', self.update_warning)
        grid.attach(self.entry2_rb1, 1, 1, 1, 1)

        self.entry2_option1 = Gtk.Label()
        self.entry2_option1.set_alignment(0, 0.5)
        self.entry2_option1.set_width_chars(50)
        grid.attach(self.entry2_option1, 2, 1, 1, 1)

        self.entry2_rb2 = Gtk.RadioButton. new_with_label_from_widget(
            self.entry2_rb1, '')
        self.entry2_rb2.connect('toggled', self.on_entry2_rb2_get_active)
        self.entry2_rb2.connect('toggled', self.update_warning)
        grid.attach(self.entry2_rb2, 1, 2, 1, 1)

        self.entry2_option2 = Gtk.Entry()
        self.entry2_option2.set_editable(False)
        self.entry2_option2.connect('changed', self.update_warning)
        self.entry2_option2.set_width_chars(50)
        self.entry2_option2.set_sensitive(False)
        grid.attach(self.entry2_option2, 2, 2, 1, 1)

        button2 = Gtk.Button()
        image2 = Gtk.Image()
        image2.set_from_stock(Gtk.STOCK_DIRECTORY, Gtk.IconSize.MENU)
        button2.set_image(image2)
        button2.connect('clicked', self.on_button_2_clicked)
        grid.attach(button2, 3, 2, 1, 1)

        grid.attach(Gtk.Separator(), 0, 3, 4, 1)

        label3 = Gtk.Label(label=_('Password') + ':')
        label3.set_width_chars(20)
        label3.set_alignment(0, 0.5)
        grid.attach(label3, 0, 4, 1, 1)

        self.entry3 = Gtk.Entry()
        self.entry3.set_width_chars(50)
        self.entry3.set_visibility(False)
        self.entry3.connect('changed', self.update_warning)
        grid.attach(self.entry3, 2, 4, 1, 1)

        label4 = Gtk.Label(label=_('Repeat password') + ':')
        label4.set_width_chars(20)
        label4.set_alignment(0, 0.5)
        grid.attach(label4, 0, 5, 1, 1)

        self.entry4 = Gtk.Entry()
        self.entry4.set_width_chars(50)
        self.entry4.set_visibility(False)
        self.entry4.connect('changed', self.update_warning)
        grid.attach(self.entry4, 2, 5, 1, 1)

        self.checkbutton_entry3_visible = Gtk.CheckButton()
        self.checkbutton_entry3_visible.connect(
            'toggled', self.on_checkbutton_entry3_visible_toggled)
        self.checkbutton_entry3_visible.connect('toggled', self.update_warning)
        grid.attach(self.checkbutton_entry3_visible, 3, 4, 1, 2)

        grid.attach(Gtk.Separator(), 0, 6, 4, 1)

        label4 = Gtk.Label(label=_('Mount folder at start') + ':')
        label4.set_width_chars(20)
        label4.set_alignment(0, 0.5)
        grid.attach(label4, 0, 7, 1, 1)

        self.checkbutton1 = BoxedSwitch()
        grid.attach(self.checkbutton1, 2, 7, 1, 1)

        label5 = Gtk.Label(
            label=_('Delete unencrypted folder on unmount') + ':')
        label5.set_width_chars(20)
        label5.set_alignment(0, 0.5)
        grid.attach(label5, 0, 8, 1, 1)

        self.checkbutton2 = BoxedSwitch()
        grid.attach(self.checkbutton2, 2, 8, 1, 1)

        self.warning_box = Gtk.Box(Gtk.Orientation.HORIZONTAL, 5)
        self.image_warning = Gtk.Image()
        self.image_warning.set_from_icon_name('gtk-dialog-warning-panel',
                                              Gtk.IconSize.BUTTON)
        self.warning_box.pack_start(self.image_warning, False, True, 5)
        self.warning_message = Gtk.Label()
        self.warning_box.pack_start(self.warning_message, False, True, 5)
        grid.attach(self.warning_box, 2, 9, 4, 1)

        self.show_all()
        if crypt_folder is not None:
            passwordmanager = CFIPasswordManager()
            secret = passwordmanager.get_password(crypt_folder['path_base'])
            self.entry1.set_text(crypt_folder['path_base'])
            self.entry2_rb2.set_active(True)
            self.entry2_option2.set_text(crypt_folder['path_mount'])
            self.entry3.set_text(secret)
            self.entry4.set_text(secret)
            self.checkbutton1.set_active(crypt_folder['automount'])
            self.checkbutton2.set_active(crypt_folder['autodelete'])
        self.update_warning()

    def _close(self, widget):
        self.close()

    def update_warning(self, *args):
        warning = False
        msg = ''
        if len(self.entry1.get_text()) == 0:
            warning = True
            msg = _('Set unencrypted folder')
        elif self.entry2_rb2.get_active() and \
                len(self.entry2_option2.get_text()) == 0:
            warning = True
            msg = _('Set encrypted folder')
        elif len(self.entry3.get_text()) == 0:
            warning = True
            msg = _('Set the password')
        elif self.entry3.get_text() != self.entry4.get_text():
            warning = True
            msg = _('Passwords are different')
        self.warning_message.set_text(msg)
        self.button_ok.set_sensitive(not warning)
        self.warning_box.set_visible(warning)

    def on_entry2_rb1_get_active(self, widget):
        self.entry2_option2.set_sensitive(False)
        if widget.get_active():
            self.entry2_option1.set_text(
                os.path.join(com.LOCAL_DIR,
                             os.path.basename(self.entry1.get_text())))
        self.update_warning()

    def on_entry2_rb2_get_active(self, widget):
        self.entry2_option2.set_sensitive(True)

    def get_path_mount(self):
        return self.entry1.get_text()

    def get_path_base(self):
        if self.entry2_rb1.get_active():
            return self.entry2_option1.get_text()
        return self.entry2_option2.get_text()

    def get_secret(self):
        return self.entry3.get_text()

    def get_automount(self):
        return self.checkbutton1.get_active()

    def get_autodelete(self):
        return self.checkbutton2.get_active()

    def on_checkbutton_entry3_visible_toggled(self, widget):
        self.entry3.set_visibility(
            self.checkbutton_entry3_visible.get_active())
        self.entry4.set_visibility(
            self.checkbutton_entry3_visible.get_active())

    def on_unencripted_folder_changed(self, widget):
        if self.entry2_rb1.get_active():
            self.entry2_option1.set_text(
                os.path.join(com.LOCAL_DIR,
                             os.path.basename(self.entry1.get_text())))

    def on_button_1_clicked(self, widget):
        fcd = Gtk.FileChooserDialog(
            title=_('Unencrypted folder'),
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            buttons=(Gtk.STOCK_OK,
                     Gtk.ResponseType.ACCEPT,
                     Gtk.STOCK_CANCEL,
                     Gtk.ResponseType.CANCEL))
        res = fcd.run()
        if res == Gtk.ResponseType.ACCEPT:
            self.entry1.set_text(fcd.get_filename())
        fcd.destroy()

    def on_button_2_clicked(self, widget):
        fcd = Gtk.FileChooserDialog(
            title=_('Encrypted folder'),
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            buttons=(Gtk.STOCK_OK,
                     Gtk.ResponseType.ACCEPT,
                     Gtk.STOCK_CANCEL,
                     Gtk.ResponseType.CANCEL))
        res = fcd.run()
        if res == Gtk.ResponseType.ACCEPT:
            self.entry2_option2.set_text(fcd.get_filename())
            self.entry2_rb2.set_active(True)
        fcd.destroy()

    def close_application(self, widget):
        self.ok = False
        self.destroy()


if __name__ == "__main__":
    ce = CreateCryptFolder(None)
    if ce.run() == Gtk.ResponseType.ACCEPT:
        print(ce.get_path_base())
        print(ce.get_path_mount())
        print(ce.get_secret())
        print(ce.get_automount())
        print(ce.get_autodelete())
    ce.destroy()
    exit(0)
