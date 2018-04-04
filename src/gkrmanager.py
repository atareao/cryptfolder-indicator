#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# CryptFolder-Indicator
# An indicator for crypt folders
#
# Copyright (C) 2010-2018 Lorenzo Carbonell
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
import ctypes
import com

libc = ctypes.CDLL("libc.so.6")


def mlock(var):
    if var:
        libc.mlock(var, len(var))


def munlock(var):
    if var:
        libc.munlock(var, len(var))


class NoPasswordFound(Exception):
    def __str__(self):
        return 'No password found'


class GnomeKeyringLocked(Exception):
    def __str__(self):
        return 'Gnome Keyring Locked'


class MyGnomeKeyring():
    def __init__(self):
        pass

    def _set_value_to_gnomekeyring(self, name, value):
        """Store a value in the keyring."""
        attributes = GnomeKeyring.Attribute.list_new()
        GnomeKeyring.Attribute.list_append_string(attributes, 'id', str(name))
        keyring = GnomeKeyring.get_default_keyring_sync()[1]
        value = GnomeKeyring.item_create_sync(
            keyring, GnomeKeyring.ItemType.GENERIC_SECRET,
            "%s preferences" % (com.APP), attributes, str(value), True)
        return value[1]

    def _get_value_from_gnomekeyring(self, name):
        """Get a locked secret for threaded/multiprocessing use."""
        value = ""
        attrlist = GnomeKeyring.Attribute.list_new()
        GnomeKeyring.Attribute.list_append_string(attrlist, 'id', str(name))
        result, found = GnomeKeyring.find_items_sync(
            GnomeKeyring.ItemType.GENERIC_SECRET, attrlist)
        if result == GnomeKeyring.Result.OK:
            value = found[0].secret
            mlock(value)
            return value
        elif result == GnomeKeyring.Result.NO_MATCH:
            raise(NoPasswordFound())
        raise(GnomeKeyringLocked())

    def get(self, key):
        return self._get_value_from_gnomekeyring('%s %s' % (com.APP, key))

    def set(self, key, value):
        return self._set_value_to_gnomekeyring('%s %s' % (com.APP, key), value)

    def get_password(self):
        return self.get('password')

    def set_password(self, password):
        return self.set('password', password)


if __name__ == '__main__':
    attributes = GnomeKeyring.Attribute.list_new()
    GnomeKeyring.Attribute.list_append_string(attributes, 'id', str('test'))
    keyring = GnomeKeyring.get_default_keyring_sync()[1]
    value = GnomeKeyring.item_create_sync(
        keyring, GnomeKeyring.ItemType.GENERIC_SECRET,
        "%s preferences" % (com.APP), attributes, str('test'), True)

    gk = MyGnomeKeyring()
    print(gk.set_password('prueba'))
    print(gk.set('ril_password', 'password'))
    print(gk.get('ril_password'))
