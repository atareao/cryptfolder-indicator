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
    gi.require_version('GnomeKeyring', '1.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import GnomeKeyring
import os
import com


class CFIPasswordManager():

    def __init__(self):
        self.keyring = GnomeKeyring.get_default_keyring_sync()[1]

    def unlock(self, password):
        result = GnomeKeyring.unlock_sync(self.keyring, password)
        print(result)
        if result == GnomeKeyring.Result.OK:
            return True
        return False

    def lock(self):
        result = GnomeKeyring.lock_sync(self.keyring)
        if result == GnomeKeyring.Result.OK:
            return True
        return False

    def isLocked(self):
        info = GnomeKeyring.get_info_sync(self.keyring)[1]
        return info.get_is_locked()

    def exists_folder(self, epath):
        epath = os.path.realpath(epath)
        return self.find_folder(epath) is not None

    def find_folder(self, epath):
        epath = os.path.realpath(epath)
        attributes = GnomeKeyring.Attribute.list_new()
        GnomeKeyring.Attribute.list_append_string(attributes, 'appid', com.APP)
        GnomeKeyring.Attribute.list_append_string(attributes,
                                                  'path_base',
                                                  epath)
        ff = GnomeKeyring.find_items_sync(GnomeKeyring.ItemType.GENERIC_SECRET,
                                          attributes)[1]
        if len(ff) > 0:
            return ff[0].item_id, ff[0].secret
        else:
            return None

    def get_password(self, epath):
        epath = os.path.realpath(epath)
        attributes = GnomeKeyring.Attribute.list_new()
        GnomeKeyring.Attribute.list_append_string(attributes, 'appid', com.APP)
        GnomeKeyring.Attribute.list_append_string(attributes,
                                                  'path_base',
                                                  epath)
        ff = GnomeKeyring.find_items_sync(GnomeKeyring.ItemType.GENERIC_SECRET,
                                          attributes)[1]
        if len(ff) > 0:
            return ff[0].secret
        return None

    def createEncriptedFolder(self, epath, password):
        epath = os.path.realpath(epath)
        attributes = GnomeKeyring.Attribute.list_new()
        GnomeKeyring.Attribute.list_append_string(attributes,
                                                  'appid',
                                                  com.APP)
        GnomeKeyring.Attribute.list_append_string(attributes,
                                                  'path_base',
                                                  str(epath))
        result = GnomeKeyring.item_create_sync(
            self.keyring, GnomeKeyring.ItemType.GENERIC_SECRET,
            'Encrypted folder %s' % (epath), attributes, password, True)[0]
        if result == GnomeKeyring.Result.OK:
            return True
        return False

    def removeEncriptedFolder(self, epath):
        epath = os.path.realpath(epath)
        id = self.find_folder(epath)
        if id is not None:
            GnomeKeyring.item_delete_sync(self.keyring, id[0])
            return True
        return False


if __name__ == '__main__':
    cfipm = CFIPasswordManager()
    '''
    print cfipm.unlock('1234')
    print cfipm.createEncriptedFolder('/home/atareao/',
                                      '/home/atareao/mount/',
                                      '1234567')
    print cfipm.find_folder('/home/atareao/')
    print cfipm.exists_folder('/home/atareao/')
    found = cfipm.find_folder('/home/atareao/')
    print cfipm.getattr('/home/atareao/')
    print found
    #print cfipm.changePasswordForEncriptedFolder('/home/atareao/','abcdefgh')
    found = cfipm.find_folder('/home/atareao/')
    '''
    print(cfipm.createEncriptedFolder('/home/atareao/', '1234'))
    print(cfipm.exists_folder('/home/atareao/'))
    # print cfipm.removeEncriptedFolder('/home/atareao/')
    # print cfipm.exists_folder('/home/atareao/')
    exit(0)
