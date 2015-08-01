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
from gi.repository import Gtk
from gi.repository import GObject
#
import com
import gnomeencfsmod
#
import locale
import gettext
#
locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(com.APP, com.LANGDIR)
gettext.textdomain(com.APP)
_ = gettext.gettext
#
class CreateEncfs(Gtk.Dialog): # needs GTK, Python, Webkit-GTK
	def __init__(self,parent,epath = None, import_folder = False):
		#***************************************************************
		Gtk.Dialog.__init__(self,'CryptFolder',parent,Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT,Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL))
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.set_size_request(620, 190)
		self.connect('destroy', self.close_application)
		self.set_icon_from_file(com.ICON)
		#***************************************************************
		vbox = Gtk.VBox(spacing = 5)
		vbox.set_border_width(5)
		self.get_content_area().add(vbox)
		#***************************************************************
		tabla = Gtk.Table(5,3)
		tabla.set_row_spacings(10)
		vbox.pack_start(tabla,False,False,0)
		#
		label1 = Gtk.Label(label=_('Encrypted folder')+':')
		label1.set_width_chars(20)
		label1.set_alignment(0,0.5)
		tabla.attach(label1, 0, 1, 0, 1, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		#
		self.entry1 = Gtk.Entry()
		self.entry1.set_width_chars(50)
		self.entry1.set_editable(False)
		tabla.attach(self.entry1, 1, 2, 0, 1, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		#
		button1 = Gtk.Button()
		image1 = Gtk.Image()
		image1.set_from_stock(Gtk.STOCK_DIRECTORY,Gtk.IconSize.MENU)
		button1.set_image(image1)
		button1.connect('clicked',self.on_button_1_clicked)
		tabla.attach(button1, 2, 3, 0, 1, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		#
		label2 = Gtk.Label(label=_('Mount folder')+':')
		label2.set_width_chars(20)
		label2.set_alignment(0,0.5)
		tabla.attach(label2, 0, 1, 1, 2, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		#
		self.entry2 = Gtk.Entry()
		self.entry2.set_width_chars(50)
		self.entry2.set_editable(False)
		tabla.attach(self.entry2, 1, 2, 1, 2, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		#
		button2 = Gtk.Button()
		image2 = Gtk.Image()
		image2.set_from_stock(Gtk.STOCK_DIRECTORY,Gtk.IconSize.MENU)
		button2.set_image(image2)
		button2.connect('clicked',self.on_button_2_clicked)		
		tabla.attach(button2, 2, 3, 1, 2, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		#
		label3 = Gtk.Label(label=_('Password')+':')
		label3.set_width_chars(20)
		label3.set_alignment(0,0.5)
		tabla.attach(label3, 0, 1, 2, 3, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		#
		self.entry3 = Gtk.Entry()
		self.entry3.set_width_chars(50)
		self.entry3.set_visibility(False)
		tabla.attach(self.entry3, 1, 2, 2, 3, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		#
		self.checkbutton_entry3_visible = Gtk.CheckButton()
		if epath:
			self.checkbutton_entry3_visible.set_active(False)
			self.entry3.set_visibility(False)
		else:
			self.checkbutton_entry3_visible.set_active(True)
			self.entry3.set_visibility(True)
		self.checkbutton_entry3_visible.connect('toggled',self.on_checkbutton_entry3_visible_toggled)
		tabla.attach(self.checkbutton_entry3_visible, 2, 3, 2, 3, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		#
		label4 = Gtk.Label(label=_('Mount folder at start')+':')
		label4.set_width_chars(20)
		label4.set_alignment(0,0.5)
		tabla.attach(label4, 0, 1, 3, 4, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)		
		#
		self.checkbutton1 = Gtk.CheckButton()
		tabla.attach(self.checkbutton1, 1, 2, 3, 4, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		#
		label5 = Gtk.Label(label=_('Delete decrypted folder on unmount')+':')
		label5.set_width_chars(20)
		label5.set_alignment(0,0.5)
		tabla.attach(label5, 0, 1, 4, 5, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)		
		#
		self.checkbutton2 = Gtk.CheckButton()
		tabla.attach(self.checkbutton2, 1, 2, 4, 5, xoptions=Gtk.AttachOptions.FILL, yoptions=Gtk.AttachOptions.FILL, xpadding=0, ypadding=0)
		#***************************************************************
		self.show_all()
		mpoint = None
		secret = None
		if epath != None:
			mpoint = gnomeencfsmod.get_mpoint(epath)
			secret = gnomeencfsmod.get_secret(epath)
			automount = gnomeencfsmod.get_automount(epath)
			autodelete = gnomeencfsmod.get_autodelete(epath)
			self.entry1.set_text(epath)
			self.entry2.set_text(mpoint)
			self.entry3.set_text(secret)
			self.checkbutton1.set_active(automount)
			self.checkbutton2.set_active(autodelete)
			self.entry1.set_editable(False)
		#
		if self.run() == Gtk.ResponseType.ACCEPT:
			self.ok = True
			if len(self.entry1.get_text())>0 and len(self.entry2.get_text())>0 and len(self.entry3.get_text())>0\
			and self.entry1.get_text() != self.entry2.get_text():
				path1 = self.entry1.get_text()
				path2 = self.entry2.get_text()
				print('Entrada 1: %s'%path1)
				print('Entrada 2: %s'% path2)
				automount = self.checkbutton1.get_active()
				autodelete = self.checkbutton2.get_active()
				password = self.entry3.get_text()
				if import_folder == True:
					if gnomeencfsmod.is_folder_encrypted(path1):
						gnomeencfsmod.import_folder(path1, path2, password, automount, autodelete)
						self.destroy()
					else:
						md = Gtk.MessageDialog(parent=None, flags=Gtk.DialogFlags.MODAL|Gtk.DialogFlags.DESTROY_WITH_PARENT,\
						type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, message_format=_('This folder is not encrypted, I can not import it'))
						md.run()
						md.destroy()
						self.destroy()
				else:
					if epath == None:
						try:
							gnomeencfsmod.add_folder(path1, path2, password, automount, autodelete)
						except gnomeencfsmod.AlreadyEncrypted:
							md = Gtk.MessageDialog(parent=None, flags=Gtk.DialogFlags.MODAL|Gtk.DialogFlags.DESTROY_WITH_PARENT,\
							type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, message_format=_('This folder is already encrypted'))
							md.run()
							md.destroy()
						self.destroy()
					else:
						if path2 == mpoint:
							new_mpoint = None
						else:
							new_mpoint = path2
						if password == secret:
							new_secret = None
						else:
							new_secret = password
						try:
							gnomeencfsmod.edit_folder(epath, new_mpoint = new_mpoint, new_secret = new_secret, new_automount = automount, new_autodelete = autodelete)
							self.destroy()
						except gnomeencfsmod.BadPassword:
							md = Gtk.MessageDialog(parent=None, flags=Gtk.DialogFlags.MODAL|Gtk.DialogFlags.DESTROY_WITH_PARENT,\
							type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, message_format=_('Bad Password'))
							md.run()
							md.destroy()
		else:
			self.ok = False
			self.destroy()
	def on_checkbutton_entry3_visible_toggled(self,widget):
		self.entry3.set_visibility(self.checkbutton_entry3_visible.get_active())
	def on_button_1_clicked(self,widget):
		fcd = Gtk.FileChooserDialog(title=_('Encrypted folder'), parent=self, action=Gtk.FileChooserAction.SELECT_FOLDER, buttons=(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT,Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL))
		res = fcd.run()
		if res == Gtk.ResponseType.ACCEPT:
			self.entry1.set_text(fcd.get_filename())			
		fcd.destroy()

	def on_button_2_clicked(self,widget):
		fcd = Gtk.FileChooserDialog(title=_('Mount point'), parent=self, action=Gtk.FileChooserAction.SELECT_FOLDER, buttons=(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT,Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL))
		res = fcd.run()
		if res == Gtk.ResponseType.ACCEPT:
			self.entry2.set_text(fcd.get_filename())			
		fcd.destroy()

	def close_application(self, widget):
		self.ok = False
		self.destroy()
	
if __name__ == "__main__":	
	ce = CreateEncfs(None)
	exit(0)
