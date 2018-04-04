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
    gi.require_version('AppIndicator3', '0.1')
    gi.require_version('GdkPixbuf', '2.0')
    gi.require_version('Notify', '0.7')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GdkPixbuf
from gi.repository import Notify
import os
import webbrowser
import dbus
import com
import machine_information
import crypto
from preferences import Preferences
from cryptmanager import CryptManager
from configurator import Configuration
from folderitem import FolderItem
from com import _


def add2menu(menu,
             text=None,
             icon=None,
             conector_event=None,
             conector_action=None):
    if text is not None:
        menu_item = Gtk.ImageMenuItem.new_with_label(text)
        if icon:
            image = Gtk.Image.new_from_file(icon)
            menu_item.set_image(image)
            menu_item.set_always_show_image(True)
    else:
        if icon is None:
            menu_item = Gtk.SeparatorMenuItem()
        else:
            menu_item = Gtk.ImageMenuItem.new_from_file(icon)
            menu_item.set_always_show_image(True)
    if conector_event is not None and conector_action is not None:
        menu_item.connect(conector_event, conector_action)
    menu_item.show()
    menu.append(menu_item)
    return menu_item


class CryptFolderIndicator():
    def __init__(self):
        if dbus.SessionBus().request_name(
            'es.atareao.cryptfolder_indicator') !=\
                dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER:
            print("application already running")
            exit(0)
        self.indicator = appindicator.Indicator.new(
            'CryptFolder-Indicator',
            'indicator-messages',
            appindicator.IndicatorCategory.APPLICATION_STATUS)

        self.editing_folders = False
        self.cryptmanager = CryptManager()
        self.menu_mount_all_folders()
        self.load_preferences()
        self.set_menu()

    def get_help_menu(self):
        help_menu = Gtk.Menu()
        github = add2menu(help_menu,
                          text=_('Project page'),
                          conector_event='activate',
                          conector_action=lambda x: webbrowser.open('\
https://github.com/atareao/cryptfolder-Indicator'))
        help = add2menu(help_menu,
                        text=_('Get help online...'),
                        conector_event='activate',
                        conector_action=lambda x: webbrowser.open('\
https://www.atareao.es/aplicacion/cryptfolder-indicator-o-cifrado-seguro-de-\
tus-archivos-en-ubuntu/'))
        translate = add2menu(help_menu,
                             text=_('Translate this application...'),
                             conector_event='activate',
                             conector_action=lambda x: webbrowser.open('\
https://translations.launchpad.net/cryptfolder-indicator'))
        bug = add2menu(help_menu,
                       text=_('Report a bug...'),
                       conector_event='activate',
                       conector_action=lambda x: webbrowser.open('\
https://github.com/atareao/cryptfolder-Indicator/issues'))
        add2menu(help_menu)
        add2menu(help_menu,
                 text=_('About'),
                 conector_event='activate',
                 conector_action=self.menu_about_response)
        web = add2menu(help_menu,
                       text=_('El atareao'),
                       conector_event='activate',
                       conector_action=lambda x: webbrowser.open('\
https://www.atareao.es'))
        twitter = add2menu(help_menu,
                           text=_('Follow me in Twitter'),
                           conector_event='activate',
                           conector_action=lambda x: webbrowser.open('\
https://twitter.com/atareao'))
        googleplus = add2menu(help_menu,
                              text=_('Follow me in Google+'),
                              conector_event='activate',
                              conector_action=lambda x: webbrowser.open('\
https://plus.google.com/118214486317320563625/posts'))
        facebook = add2menu(help_menu,
                            text=_('Follow me in Facebook'),
                            conector_event='activate',
                            conector_action=lambda x: webbrowser.open('\
http://www.facebook.com/elatareao'))
        add2menu(help_menu)
        #
        github.set_image(Gtk.Image.new_from_file(
            os.path.join(com.ICONDIR, 'github.svg')))
        github.set_always_show_image(True)
        help.set_image(Gtk.Image.new_from_file(
            os.path.join(com.ICONDIR, 'help.svg')))
        help.set_always_show_image(True)
        translate.set_image(Gtk.Image.new_from_file(
            os.path.join(com.ICONDIR, 'translate.svg')))
        translate.set_always_show_image(True)
        bug.set_image(Gtk.Image.new_from_file(
            os.path.join(com.ICONDIR, 'bug.svg')))
        bug.set_always_show_image(True)
        web.set_image(Gtk.Image.new_from_file(
            os.path.join(com.ICONDIR, 'web.svg')))
        web.set_always_show_image(True)
        twitter.set_image(Gtk.Image.new_from_file(os.path.join(
            com.ICONDIR, 'twitter.svg')))
        twitter.set_always_show_image(True)
        googleplus.set_image(Gtk.Image.new_from_file(os.path.join(
            com.ICONDIR, 'google.svg')))
        googleplus.set_always_show_image(True)
        facebook.set_image(Gtk.Image.new_from_file(os.path.join(
            com.ICONDIR, 'facebook.svg')))
        facebook.set_always_show_image(True)

        help_menu.show()
        return help_menu

    def on_folderitem_clicked(self, widget):
        print('ofc', widget.folder)
        folder = widget.folder
        if self.editing_folders is True:
            return
        if self.cryptmanager.is_mounted(folder['path_base']) is True:
            self.cryptmanager.unmount(folder['path_base'])
        else:
            self.cryptmanager.mount(folder['path_base'])
        if self.cryptmanager.is_mounted(folder['path_base']):
            widget.set_mounted(True)
            msg = '{0}: {1}'.format(_('Mounted'), folder['path_mount'])
            icon = self.ICON_OPEN
        else:
            widget.set_mounted(False)
            msg = '{0}: {1}'.format(_('Unmounted'), folder['path_mount'])
            icon = self.ICON_CLOSED
        try:
            notification = Notify.Notification.new('CryptFolder-Indicator',
                                                   msg,
                                                   icon)
            notification.show()
        except Exception as e:
            print(e)

    def on_edit_folders_clicked(self, widget):
        self.editing_folders = True
        widget.set_sensitive(False)
        crypto.CM()
        self.set_menu()
        widget.set_sensitive(True)
        self.editing_folders = False

    def set_menu(self):
        configurator = Configuration()
        theme = configurator.get('theme')

        self.menu = Gtk.Menu()
        folders = self.cryptmanager.get_folders()
        for key in folders.keys():
            print(folders[key], theme)
            folderItem = FolderItem(folders[key], theme)
            folderItem.set_mounted(self.cryptmanager.is_mounted(key))
            folderItem.connect('activate', self.on_folderitem_clicked)
            folderItem.show()
            self.menu.append(folderItem)

        add2menu(self.menu)
        add2menu(self.menu,
                 text=_('Edit crypt folders'),
                 conector_event='activate',
                 conector_action=self.on_edit_folders_clicked)
        add2menu(self.menu,
                 text=_('Preferences'),
                 conector_event='activate',
                 conector_action=self.menu_preferences_response)
        add2menu(self.menu)
        self.menu_help = add2menu(self.menu,
                                  text=_('Help'))
        self.menu_help.set_submenu(self.get_help_menu())
        add2menu(self.menu)
        self.menu_separator2 = Gtk.MenuItem()
        add2menu(self.menu,
                 text=_('Exit'),
                 conector_event='activate',
                 conector_action=self.menu_exit_response)

        self.menu.show()
        self.indicator.set_icon(self.ICON)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.menu)

    def load_preferences(self):
        configurator = Configuration()
        option = configurator.get('theme')
        if option == 'normal':
            self.ICON = com.ICON
            self.ICON_OPEN = com.ICON_OPEN
            self.ICON_CLOSED = com.ICON_CLOSED
        elif option == 'light':
            self.ICON = com.ICON_L
            self.ICON_OPEN = com.ICON_OPEN_L
            self.ICON_CLOSED = com.ICON_CLOSED_L
        else:
            self.ICON = com.ICON_D
            self.ICON_OPEN = com.ICON_OPEN_D
            self.ICON_CLOSED = com.ICON_CLOSED_D

    def menu_preferences_response(self, widget):
        widget.set_sensitive(False)
        preferences = Preferences()
        if preferences.run() == Gtk.ResponseType.ACCEPT:
            preferences.hide()
            preferences.save()
            self.load_preferences()
            self.set_menu()
        preferences.destroy()
        widget.set_sensitive(True)

    def menu_mount_all_folders(self):
        configurator = Configuration()
        automount = configurator.get('mount_folders_on_start')
        print('Mount folders on start? %s' % automount)
        if automount is True:
            folders = self.cryptmanager.get_folders()
            for key in folders.keys():
                if folders[key]['automount'] is True and\
                        self.cryptmanager.is_mounted(key) is False:
                    self.cryptmanager.mount(key)

    def menu_exit_response(self, widget):
        print('Exit')
        folders = self.cryptmanager.get_folders()
        for index, key in enumerate(folders.keys()):
            mounted = self.cryptmanager.is_mounted(key)
            print(index, 'key:', key, 'mounted:', mounted)
            folders[key]['mounted'] = mounted
            if mounted:
                self.cryptmanager.unmount(key)
        configurator = Configuration()
        configurator.set('folders', folders)
        configurator.save()
        exit(0)

    def on_menu_project_clicked(self, widget):
        webbrowser.open('https://launchpad.net/cryptfolder-indicator')

    def on_menu_help_online_clicked(self, widget):
        webbrowser.open('https://answers.launchpad.net/cryptfolder-indicator')

    def on_menu_translations_clicked(self, widget):
        webbrowser.open('\
https://translations.launchpad.net/cryptfolder-indicator')

    def on_menu_bugs_clicked(self, widget):
        webbrowser.open('https://bugs.launchpad.net/cryptfolder-indicator')

    def menu_about_response(self, widget):
        widget.set_sensitive(False)
        ad = Gtk.AboutDialog()
        ad.set_name(com.APPNAME)
        ad.set_version(com.VERSION)
        ad.set_copyright('Copyrignt (c) 2010-2018\nLorenzo Carbonell')
        ad.set_comments(_('An indicator for crypt folders with encfs'))
        ad.set_license('''
This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.''')
        ad.set_website('http://www.atareao.es')
        ad.set_website_label('http://www.atareao.es')
        ad.set_authors(['\
Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
        ad.set_documenters(['\
Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
        ad.set_artists(['\
padlock.svg By AJ Ashton <http://www.openclipart.org/detail/17931>'])
        ad.set_translator_credits('''
Gianfranco Frisani<https://launchpad.net/~gfrisani>
Sascha Biermanns<https://launchpad.net/~skkd-h4k1n9>
Eugene Marshal<https://launchpad.net/~lowrider>
Xuacu Saturio<https://launchpad.net/~xuacusk8>
Xose M Lamas<https://launchpad.net/~xmgz>
Lorenzo Carbonell<https://launchpad.net/~lorenzo-carbonell>
LEROY Jean-Christophe<https://launchpad.net/~celtic2-deactivatedaccount>
Daniel Winzen<https://launchpad.net/~q-d>
xemard.nicolas<https://launchpad.net/~xemard.nicolas>
Albert Casanovas<https://launchpad.net/~lnkxdesings>
irbinix<https://launchpad.net/~irbinix>
Adolfo Jayme Barrientos<https://launchpad.net/~fitoschido>
Łukasz Komorowski<https://launchpad.net/~komorowskiukasz>''')
        ad.set_icon_from_file(com.ICON)
        ad.set_logo(GdkPixbuf.Pixbuf.new_from_file(com.ICON))
        ad.set_program_name(com.APPNAME)
        ad.run()
        ad.destroy()
        widget.set_sensitive(True)


def main():
    print(machine_information.get_information())
    print('CryptFolder-Indicator version: %s' % com.VERSION)
    print('#####################################################')
    Notify.init('cryptfolder-indicator')
    CryptFolderIndicator()
    Gtk.main()
    exit(0)


if __name__ == "__main__":
    main()
