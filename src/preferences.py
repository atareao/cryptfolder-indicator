#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
#
__author__="atareao"
__date__ ="$29-ene-2011$"
#
# <from numbers to letters.>
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
import os
from gi.repository import Gtk
import locale
import gettext
import com
import shutil
import time
from configurator import Configuration

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(com.APP, com.LANGDIR)
gettext.textdomain(com.APP)
_ = gettext.gettext

class Preferences(Gtk.Dialog):
	def __init__(self):
		#
		self.configurator = Configuration()
		Gtk.Dialog.__init__(self, 'CryptFolder Indicator | '+_('Preferences'),None,Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.set_size_request(500, 150)
		self.connect('close', self.close_application)
		self.set_icon_from_file(com.ICON)
		#
		self.vbox1 = Gtk.VBox(spacing = 5)
		self.vbox1.set_border_width(5)
		self.get_content_area().add(self.vbox1)
		#
		self.frame1 = Gtk.Frame()
		self.vbox1.add(self.frame1)
		#***************************************************************
		self.vbox2 = Gtk.VBox(spacing = 5)
		self.vbox2.set_border_width(5)
		self.frame1.add(self.vbox2)
		table1 = Gtk.Table(4,3,True)
		self.vbox2.add(table1)
		#
		self.checkbutton1 = Gtk.CheckButton(_('Autostart'))
		table1.attach(self.checkbutton1,0,3,0,1)
		self.checkbutton2 = Gtk.CheckButton(_('Mount selected folders at start'))
		table1.attach(self.checkbutton2,0,3,1,2)
		label1 = Gtk.Label(label=_('Select icon theme')+':')
		label1.set_alignment(0,0.5)
		table1.attach(label1,0,3,2,3)
		self.radiobutton0 = Gtk.RadioButton(group=None,label=_('Normal'))
		table1.attach(self.radiobutton0,0,1,3,4)
		self.radiobutton1 = Gtk.RadioButton(group=self.radiobutton0,label=_('Light'))
		table1.attach(self.radiobutton1,1,2,3,4)
		self.radiobutton2 = Gtk.RadioButton(group=self.radiobutton0,label=_('Dark'))
		table1.attach(self.radiobutton2,2,3,3,4)
		#***************************************************************		
		#
		self.load_preferences()
		#
		self.show_all()
		
	def close_application(self, widget, event):
		self.destroy()
		
	def close_ok(self):
		self.hide()
		
	def save(self):
		filestart = os.path.join(os.getenv("HOME"),".config/autostart/cryptfolder-indicator-autostart.desktop")
		if self.checkbutton1.get_active():
			if not os.path.exists(filestart):
				shutil.copyfile('/opt/extras.ubuntu.com/cryptfolder-indicator/share/cryptfolder-indicator/cryptfolder-indicator-autostart.desktop',filestart)
		else:		
			if os.path.exists(filestart):
				os.remove(filestart)
		if self.checkbutton2.get_active():
			self.configurator.set('mount_folders_on_start','yes')
		else:
			self.configurator.set('mount_folders_on_start','no')
		if self.radiobutton0.get_active() == True:
			option = 'normal'
		elif self.radiobutton1.get_active() == True:
			option = 'light'
		else:
			option = 'dark'
		self.configurator.set('theme',option)
		self.configurator.save()
		
			
	def load_preferences(self):
		if os.path.exists(os.path.join(os.getenv("HOME"),".config/autostart/cryptfolder-indicator-autostart.desktop")):
			self.checkbutton1.set_active(True)
		self.checkbutton2.set_active(self.configurator.get('mount_folders_on_start')=='yes')
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
