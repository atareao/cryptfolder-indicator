#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
__author__='atareao'
__date__ ='$14/06/2011'
#
# CryptFolder-Indicator
# An indicator for crypt folders
#
# Copyright (C) 2010-2011 Lorenzo Carbonell
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
from gi.repository import GObject
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from gi.repository import Notify
from gi.repository import GLib
import os
import locale
import gettext
import webbrowser
import dbus
import com
import gnomeencfsmod
import crypto
import machine_information
from preferences import Preferences
from configurator import Configuration

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(com.APP, com.LANGDIR)
gettext.textdomain(com.APP)
_ = gettext.gettext

def add2menu(menu, text = None, icon = None, conector_event = None, conector_action = None):
	if text != None:
		menu_item = Gtk.ImageMenuItem.new_with_label(text)
		if icon:
			image = Gtk.Image.new_from_file(icon)
			menu_item.set_image(image)
			menu_item.set_always_show_image(True)
	else:
		if icon == None:
			menu_item = Gtk.SeparatorMenuItem()
		else:
			menu_item = Gtk.ImageMenuItem.new_from_file(icon)
			menu_item.set_always_show_image(True)
	if conector_event != None and conector_action != None:				
		menu_item.connect(conector_event,conector_action)
	menu_item.show()
	menu.append(menu_item)
	return menu_item

class CryptFolderIndicator():
	def __init__(self):
		if dbus.SessionBus().request_name('es.atareao.cryptfolder_indicator') != dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER:
			print("application already running")
			exit(0)
		self.indicator = appindicator.Indicator.new ('CryptFolder-Indicator', 'indicator-messages', appindicator.IndicatorCategory.APPLICATION_STATUS)
		#
		self.editing_folders = False
		self.menu_mount_all_folders()
		self.load_preferences()
		self.set_menu()


	def get_help_menu(self):
		help_menu =Gtk.Menu()
		#		
		add2menu(help_menu,text = _('Web...'),conector_event = 'activate',conector_action = self.on_menu_project_clicked)
		add2menu(help_menu,text = _('Get help online...'),conector_event = 'activate',conector_action = self.on_menu_help_online_clicked)
		add2menu(help_menu,text = _('Translate this application...'),conector_event = 'activate',conector_action = self.on_menu_translations_clicked)
		add2menu(help_menu,text = _('Report a bug...'),conector_event = 'activate',conector_action = self.on_menu_bugs_clicked)
		add2menu(help_menu)
		add2menu(help_menu,text = _('About'),conector_event = 'activate',conector_action = self.menu_about_response)
		web = add2menu(help_menu,text = _('Homepage'),conector_event = 'activate',conector_action = lambda x: webbrowser.open('http://www.atareao.es/tag/cryptfolder-indicator'))
		twitter = add2menu(help_menu,text = _('Follow us in Twitter'),conector_event = 'activate',conector_action = lambda x: webbrowser.open('https://twitter.com/atareao'))
		googleplus = add2menu(help_menu,text = _('Follow us in Google+'),conector_event = 'activate',conector_action = lambda x: webbrowser.open('https://plus.google.com/118214486317320563625/posts'))
		facebook = add2menu(help_menu,text = _('Follow us in Facebook'),conector_event = 'activate',conector_action = lambda x: webbrowser.open('http://www.facebook.com/elatareao'))
		add2menu(help_menu)
		add2menu(help_menu,text = _('About'),conector_event = 'activate',conector_action = self.menu_about_response)
		#		
		web.set_image(Gtk.Image.new_from_file(os.path.join(com.SOCIALDIR,'web.svg')))
		web.set_always_show_image(True)
		twitter.set_image(Gtk.Image.new_from_file(os.path.join(com.SOCIALDIR,'twitter.svg')))
		twitter.set_always_show_image(True)
		googleplus.set_image(Gtk.Image.new_from_file(os.path.join(com.SOCIALDIR,'googleplus.svg')))
		googleplus.set_always_show_image(True)
		facebook.set_image(Gtk.Image.new_from_file(os.path.join(com.SOCIALDIR,'facebook.svg')))
		facebook.set_always_show_image(True)
		#
		help_menu.show()
		return help_menu
	def on_path_clicked(self,widget):
		if self.editing_folders ==True:
			return
		print ('%s is mounted -> %s'%(widget.get_label(),gnomeencfsmod.is_folder_mounted(widget.get_label())))
		if gnomeencfsmod.is_folder_mounted(widget.get_label()) == True:
			if gnomeencfsmod.unmount_folder(widget.get_label()) == True:
				widget.set_image(Gtk.Image.new_from_file(self.ICON_CLOSED))
				msg = '%s %s\nfrom\n%s'%(_('Unmounted'),widget.get_label(),gnomeencfsmod.get_mpoint(widget.get_label()))
				icon = self.ICON_CLOSED
			else:
				msg = '%s %s\nfrom\n%s'%(_('Not unmounted'),widget.get_label(),gnomeencfsmod.get_mpoint(widget.get_label()))
				icon = self.ICON_OPEN
		else:
			try:
				if gnomeencfsmod.mount_folder(widget.get_label()) == True:
					widget.set_image(Gtk.Image.new_from_file(self.ICON_OPEN))
					msg = '%s %s\non\n%s'%(_('Mounted'),widget.get_label(),gnomeencfsmod.get_mpoint(widget.get_label()))
					icon = self.ICON_OPEN
				else:
					msg = '%s %s\non\n%s'%(_('Not mounted'),widget.get_label(),gnomeencfsmod.get_mpoint(widget.get_label()))
					icon = self.ICON_CLOSED
				notification = Notify.Notification.new('CryptFolder-Indicator',msg,icon)
				notification.show()
			except gnomeencfsmod.BadPassword as e:
				notification = Notify.Notification.new('CryptFolder-Indicator',_('The password is wrong'))
				notification.show()

		
	def on_edit_folders_clicked(self,widget):
		self.editing_folders = True
		widget.set_sensitive(False)
		cm = crypto.CM()
		self.set_menu()
		widget.set_sensitive(True)
		self.editing_folders = False
		
	def set_menu(self):
		self.menu = Gtk.Menu()
		#
		for folder in gnomeencfsmod.get_folders():
			if folder['mounted'] == True:
				image = self.ICON_OPEN
			else:
				image = self.ICON_CLOSED
			print('-----------------')
			print(folder['encfs-path'], image)
			add2menu(self.menu, text = folder['encfs-path'], icon = image, conector_event = 'activate', conector_action = self.on_path_clicked)
		add2menu(self.menu)
		add2menu(self.menu, text = _('Edit crypt folders'),conector_event = 'activate', conector_action = self.on_edit_folders_clicked)
		add2menu(self.menu, text = _('Preferences'),conector_event = 'activate', conector_action = self.menu_preferences_response)
		add2menu(self.menu)
		self.menu_help = add2menu(self.menu,text = _('Help'))
		self.menu_help.set_submenu(self.get_help_menu())
		add2menu(self.menu)
		self.menu_separator2=Gtk.MenuItem()
		add2menu(self.menu,text = _('Exit'),conector_event = 'activate',conector_action = self.menu_exit_response)
		#
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
		
	def menu_preferences_response(self,widget):
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
		option = configurator.get('theme')		
		automount = configurator.get('mount_folders_on_start')
		print('Mount folders on start? %s'%automount)
		if automount == 'yes':
			for folder in gnomeencfsmod.get_folders():
				print('#################################################')
				print('automount folder %s?%s'%(folder['encfs-path'],folder['auto-mount']))
				print('is folder %s mounted?%s'%(folder['encfs-path'],folder['mounted']))
				if folder['auto-mount'] == 'yes' and folder['mounted'] == False:
					try:
						gnomeencfsmod.mount_folder(folder['encfs-path'])
						print('folder %s mounted'%(folder['encfs-path']))
					except gnomeencfsmod.BadPassword:
						pass
				
	def menu_exit_response(self,widget):
		for folder in gnomeencfsmod.get_folders():
			print('#################################################')
			print('is folder %s mounted?%s'%(folder['encfs-path'],folder['mounted']))
			if folder['mounted'] == True:
				gnomeencfsmod.unmount_folder(folder['encfs-path'])
		exit(0)
		
	def on_menu_project_clicked(self,widget):
		webbrowser.open('https://launchpad.net/cryptfolder-indicator')
		
	def on_menu_help_online_clicked(self,widget):
		webbrowser.open('https://answers.launchpad.net/cryptfolder-indicator')
	
	def on_menu_translations_clicked(self,widget):
		webbrowser.open('https://translations.launchpad.net/cryptfolder-indicator')
	
	def on_menu_bugs_clicked(self,widget):
		webbrowser.open('https://bugs.launchpad.net/cryptfolder-indicator')		
			
	def menu_about_response(self,widget):
		widget.set_sensitive(False)
		ad=Gtk.AboutDialog()
		ad.set_name(com.APPNAME)
		ad.set_version(com.VERSION)
		ad.set_copyright('Copyrignt (c) 2010-2013\nLorenzo Carbonell')
		ad.set_comments(_('An indicator for crypt folders with encfs'))
		ad.set_license(''+
		'This program is free software: you can redistribute it and/or modify it\n'+
		'under the terms of the GNU General Public License as published by the\n'+
		'Free Software Foundation, either version 3 of the License, or (at your option)\n'+
		'any later version.\n\n'+
		'This program is distributed in the hope that it will be useful, but\n'+
		'WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY\n'+
		'or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for\n'+
		'more details.\n\n'+
		'You should have received a copy of the GNU General Public License along with\n'+
		'this program.  If not, see <http://www.gnu.org/licenses/>.')
		ad.set_website('http://www.atareao.es')
		ad.set_website_label('http://www.atareao.es')
		ad.set_authors(['Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
		ad.set_documenters(['Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'])
		ad.set_artists(['padlock.svg By AJ Ashton <http://www.openclipart.org/detail/17931>'])
		ad.set_translator_credits(''+
		'Gianfranco Frisani<https://launchpad.net/~gfrisani>\n'+
		'Sascha Biermanns<https://launchpad.net/~skkd-h4k1n9>\n'+
		'Eugene Marshal<https://launchpad.net/~lowrider>\n'+
		'Xuacu Saturio<https://launchpad.net/~xuacusk8>\n'+
		'Xose M Lamas<https://launchpad.net/~xmgz>\n'+
		'Lorenzo Carbonell<https://launchpad.net/~lorenzo-carbonell>\n'+
		'LEROY Jean-Christophe<https://launchpad.net/~celtic2-deactivatedaccount>\n'+
		'Daniel Winzen<https://launchpad.net/~q-d>\n'+
		'xemard.nicolas<https://launchpad.net/~xemard.nicolas>\n'+
		'Albert Casanovas<https://launchpad.net/~lnkxdesings>\n'+
		'irbinix<https://launchpad.net/~irbinix>\n'+
		'Adolfo Jayme Barrientos<https://launchpad.net/~fitoschido>\n'+
		'Łukasz Komorowski<https://launchpad.net/~komorowskiukasz>')
		ad.set_icon_from_file(com.ICON)
		ad.set_logo(GdkPixbuf.Pixbuf.new_from_file(com.ICON))
		ad.set_program_name(com.APPNAME)
		ad.run()
		ad.destroy()
		widget.set_sensitive(True)

if __name__ == "__main__":
	print(machine_information.get_information())
	print('CryptFolder-Indicator version: %s'%com.VERSION)
	print('#####################################################')
	Notify.init('cryptfolder-indicator')
	cfi=CryptFolderIndicator()
	Gtk.main()
	exit(0)
