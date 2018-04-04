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

import os
import locale
import gettext

__author__ = 'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'
__copyright__ = 'Copyright (c) 2011 - 2018 Lorenzo Carbonell'
__license__ = 'GPLV3'
__url__ = 'http://www.atareao.es'
USRDIR = '/usr'


def is_package():
    return (__file__.startswith(USRDIR) or os.getcwd().startswith(USRDIR))


PARAMS = {'mount_folders_on_start': False,
          'theme': 'normal',
          'folders': {}
          }


APP = 'cryptfolder-indicator'
APPCONF = APP + '.conf'
APPNAME = 'CryptFolder-Indicator'
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config')
CONFIG_APP_DIR = os.path.join(CONFIG_DIR, APP)
CONFIG_FILE = os.path.join(CONFIG_APP_DIR, APPCONF)
AUTOSTART_DIR = os.path.join(CONFIG_DIR, 'autostart')
LOCAL_DIR = os.path.join(os.path.expanduser('~'), '.local', 'share', APP)
FILE_AUTO_START = os.path.join(AUTOSTART_DIR,
                               'cryptfolder-indicator-autostart.desktop')
if not os.path.exists(CONFIG_APP_DIR):
    os.makedirs(CONFIG_APP_DIR)
if not os.path.exists(LOCAL_DIR):
    os.makedirs(LOCAL_DIR)

# check if running from source
if is_package():
    ROOTDIR = '/usr/share/'
    LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
    APPDIR = os.path.join(ROOTDIR, APP)
    ICONDIR = os.path.join(APPDIR, 'icons')
    CHANGELOG = os.path.join(APPDIR, 'changelog')
    AUTOSTART_SOURCE_DIR = APPDIR
else:
    ROOTDIR = os.path.dirname(__file__)
    LANGDIR = os.path.join(ROOTDIR, 'template1')
    APPDIR = os.path.join(ROOTDIR, APP)

    ICONDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/icons'))
    DEBIANDIR = os.path.normpath(os.path.join(ROOTDIR, '../debian'))
    CHANGELOG = os.path.join(DEBIANDIR, 'changelog')
    AUTOSTART_SOURCE_DIR = os.path.normpath(os.path.join(APPDIR, '../data'))

AUTOSTART_DIR = os.path.join(CONFIG_DIR, 'autostart')
FILE_AUTO_START_NAME = 'cryptfolder-indicator-autostart.desktop'
FILE_AUTO_START_SRC = os.path.join(AUTOSTART_SOURCE_DIR, FILE_AUTO_START_NAME)
FILE_AUTO_START = os.path.join(AUTOSTART_DIR, FILE_AUTO_START_NAME)

ICON = os.path.join(ICONDIR, 'cryptfolder-indicator.svg')
ICON_L = os.path.join(ICONDIR, 'cryptfolder-indicator-light.svg')
ICON_D = os.path.join(ICONDIR, 'cryptfolder-indicator-dark.svg')
ICON_OPEN = os.path.join(ICONDIR, 'cryptfolder-open.svg')
ICON_OPEN_L = os.path.join(ICONDIR, 'cryptfolder-open-light.svg')
ICON_OPEN_D = os.path.join(ICONDIR, 'cryptfolder-open-dark.svg')
ICON_CLOSED = os.path.join(ICONDIR, 'cryptfolder-closed.svg')
ICON_CLOSED_L = os.path.join(ICONDIR, 'cryptfolder-closed-light.svg')
ICON_CLOSED_D = os.path.join(ICONDIR, 'cryptfolder-closed-dark.svg')

f = open(CHANGELOG, 'r')
line = f.readline()
f.close()
pos = line.find('(')
posf = line.find(')', pos)
VERSION = line[pos + 1:posf].strip()
if not is_package():
    VERSION = VERSION + '-src'

try:
    current_locale, encoding = locale.getdefaultlocale()
    language = gettext.translation(APP, LANGDIR, [current_locale])
    language.install()
    _ = language.gettext
except Exception as e:
    _ = str
