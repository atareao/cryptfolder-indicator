#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
#
#
# com.py
#
# Copyright (C) 2011 Lorenzo Carbonell
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
#
#
#

__author__ = 'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'
__date__ ='$13/09/2011'
__copyright__ = 'Copyright (c) 2011 Lorenzo Carbonell'
__license__ = 'GPLV3'
__url__ = 'http://www.atareao.es'
__version__ = '0.5.0-0extras13.04.7'

import os

######################################

def is_package():
    return __file__.find('src') < 0

######################################

VERSION = __version__
APP = 'cryptfolder-indicator'
APPCONF = APP + '.conf'
APPNAME = 'CryptFolder-Indicator'
SETTINGSPATH = 'apps.indicators.cryptfolder-indicator'
PARAMS = {
			'mount_folders_on_start':'no',
			'theme':'normal',
			'folders':{}
			}
# check if running from source
if is_package():
	ROOTDIR = '/opt/extras.ubuntu.com/cryptfolder-indicator/share/'
	SOCIALDIR = '/opt/extras.ubuntu.com/cryptfolder-indicator/share/cryptfolder-indicator/social'
	IMGDIR = '/opt/extras.ubuntu.com/cryptfolder-indicator/share/cryptfolder-indicator/icons'
	LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
	APPDIR = os.path.join(ROOTDIR, APP)	
	ICON = '/opt/extras.ubuntu.com/cryptfolder-indicator/share/pixmaps/cryptfolder-indicator.svg'
else:
	VERSION = VERSION + '-src'
	ROOTDIR = os.path.dirname(__file__)
	LANGDIR = os.path.normpath(os.path.join(ROOTDIR, '../po'))
	IMGDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/icons'))
	SOCIALDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/social'))
	APPDIR = ROOTDIR

ICON = os.path.normpath(os.path.join(IMGDIR,'cryptfolder-indicator.svg'))
ICON_L = os.path.normpath(os.path.join(IMGDIR,'cryptfolder-indicator-light.svg'))
ICON_D = os.path.normpath(os.path.join(IMGDIR,'cryptfolder-indicator-dark.svg'))
ICON_OPEN = os.path.normpath(os.path.join(IMGDIR,'cryptfolder-open.svg'))
ICON_OPEN_L = os.path.normpath(os.path.join(IMGDIR,'cryptfolder-open-light.svg'))
ICON_OPEN_D = os.path.normpath(os.path.join(IMGDIR,'cryptfolder-open-dark.svg'))
ICON_CLOSED = os.path.normpath(os.path.join(IMGDIR,'cryptfolder-closed.svg'))
ICON_CLOSED_L = os.path.normpath(os.path.join(IMGDIR,'cryptfolder-closed-light.svg'))
ICON_CLOSED_D = os.path.normpath(os.path.join(IMGDIR,'cryptfolder-closed-dark.svg'))

CONFIG_DIR = os.path.join(os.path.expanduser('~'),'.config')
CONFIG_APP_DIR = os.path.join(CONFIG_DIR, APP)
CONFIG_FILE = os.path.join(CONFIG_APP_DIR, APPCONF)

AUTOSTART_DIR = os.path.join(os.getenv('HOME'),'.config/autostart')
FILE_AUTO_START = os.path.join(AUTOSTART_DIR,'cryptfolder-indicator-autostart.desktop')












