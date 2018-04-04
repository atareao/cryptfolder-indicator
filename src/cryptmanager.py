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

import gnomecryfsmod
from configurator import Configuration
from cfkeyringmanager import CFIPasswordManager


class CryptManager():
    def __init__(self):
        self.configuration = Configuration()
        self.passwordmanager = CFIPasswordManager()

    def edit_folder(self, base, new_base, new_mount, new_secret,
                    new_autodelete, new_automount):
        folders = self.get_folders()
        if base in folders.keys():
            mount = folders[base]['path_mount']
            if new_base in folders.keys():
                raise gnomecryfsmod.AlreadyExists()
            if gnomecryfsmod.is_folder_encrypted(base):
                if self.passwordmanager.exists_folder(base):
                    secret = self.passwordmanager.get_password(base)
                    ans = gnomecryfsmod.super_re_crypt_folder(base, new_base,
                                                              mount,
                                                              new_mount,
                                                              secret,
                                                              new_secret)
                    if ans is True:
                        if base != new_base:
                            del folders[base]
                        folders[new_base] = {
                            'path_base': new_base,
                            'path_mount': new_mount,
                            'autodelete': new_autodelete,
                            'automount': new_automount,
                            'mounted': gnomecryfsmod.is_folder_mounted(
                                new_base)}
                        self.configuration.set('folders', folders)
                        self.configuration.save()

        return False

    def add_folder(self, base, mount, secret,
                   autodelete=False, automount=False):
        folders = self.get_folders()
        if base in folders.keys():
            raise gnomecryfsmod.AlreadyExists()
        if gnomecryfsmod.is_folder_encrypted(base):
            if self.passwordmanager.exists_folder(base):
                saved_secret = self.passwordmanager.get_password(base)
                if saved_secret != secret:
                    raise gnomecryfsmod.BadPassword()
                    return
            else:
                if self.passwordmanager.createEncriptedFolder(base, secret)\
                        is False:
                    raise gnomecryfsmod.BadPassword()
                    return
            if gnomecryfsmod.is_folder_mounted(base):
                if gnomecryfsmod.unmount_folder(base):
                    gnomecryfsmod.mount_folder(base, mount, secret)
            else:
                if gnomecryfsmod.mount_folder(base, mount, secret):
                    gnomecryfsmod.unmount_folder(base)
            folders[base] = {'path_base': base,
                             'path_mount': mount,
                             'autodelete': autodelete,
                             'automount': automount,
                             'mounted': gnomecryfsmod.is_folder_mounted(base)
                             }
            self.configuration.set('folders', folders)
            self.configuration.save()
        else:
            if self.passwordmanager.exists_folder(base):
                saved_secret = self.passwordmanager.get_password(base)
                if saved_secret != secret:
                    raise gnomecryfsmod.BadPassword()
                    return
            else:
                if self.passwordmanager.createEncriptedFolder(base, secret)\
                        is False:
                    raise gnomecryfsmod.BadPassword()
                    return
                else:
                    if gnomecryfsmod.is_folder_encrypted(base):
                        if gnomecryfsmod.is_folder_mounted(base):
                            if gnomecryfsmod.unmount_folder(base):
                                gnomecryfsmod.mount_folder(base, mount, secret)
                        else:
                            if gnomecryfsmod.mount_folder(base, mount, secret):
                                gnomecryfsmod.unmount_folder(base)
                        folders[base] = {
                            'path_base': base,
                            'path_mount': mount,
                            'autodelete': autodelete,
                            'automount': automount,
                            'mounted': gnomecryfsmod.is_folder_mounted(base)}
                        self.configuration.set('folders', folders)
                        self.configuration.save()
                    elif gnomecryfsmod.crypt_folder(base, mount, secret):
                        folders[base] = {
                            'path_base': base,
                            'path_mount': mount,
                            'autodelete': autodelete,
                            'automount': automount,
                            'mounted': gnomecryfsmod.is_folder_mounted(base)}
                        self.configuration.set('folders', folders)
                        self.configuration.save()

    def remove_folder(self, base):
        folders = self.get_folders()
        if base in folders.keys():
            mount = folders[base]['path_mount']
            if gnomecryfsmod.remove_folder(base, mount) is True:
                self.passwordmanager.removeEncriptedFolder(base)
                del folders[base]
                self.configuration.set('folders', folders)
                self.configuration.save()

    def mount(self, base):
        folders = self.get_folders()
        if base in folders.keys():
            secret = self.passwordmanager.get_password(base)
            if secret is not None:
                gnomecryfsmod.mount_folder(base,
                                           folders[base]['path_mount'],
                                           secret)

    def unmount(self, base):
        folders = self.get_folders()
        if base in folders.keys():
            gnomecryfsmod.unmount_folder(base)

    def is_mounted(self, base):
        folders = self.get_folders()
        if base in folders.keys():
            return gnomecryfsmod.is_folder_mounted(base)
        return False

    def set_automount(self, base, automount):
        folders = self.get_folders()
        if base in folders.keys():
            folders[base]['automount'] = automount
            self.configuration.set('folders', folders)
            self.configuration.save()

    def get_folders(self):
        return self.configuration.get('folders')


if __name__ == '__main__':
    cm = CryptManager()
    cm.add_folder('/datos/temporal/sample7',
                  '/datos/temporal/montado7',
                  'euldlmdc2')
