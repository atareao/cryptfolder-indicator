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
import shutil
#
import com
import gnomeencfsmod
from createenfs import CreateEncfs
#
import locale
import gettext
#
locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(com.APP, com.LANGDIR)
gettext.textdomain(com.APP)
_ = gettext.gettext
#


class CM(Gtk.Dialog): # needs GTK, Python, Webkit-GTK
	def __init__(self):
		self.location = None
		#***************************************************************
		Gtk.Dialog.__init__(self,'CryptFolder',None,Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,(Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
		self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		self.set_size_request(450, 450)
		self.connect('destroy', self.close_application)
		self.set_icon_from_file(com.ICON)
		#***************************************************************
		vbox = Gtk.VBox(spacing = 5)
		vbox.set_border_width(5)
		self.get_content_area().add(vbox)
		#***************************************************************
		frame = Gtk.Frame()
		vbox.add(frame)
		#***************************************************************
		vbox1 = Gtk.VBox(spacing = 5)
		vbox1.set_border_width(5)
		frame.add(vbox1)
		hbox1 = Gtk.HBox(spacing = 5)
		hbox1.set_border_width(5)
		vbox1.pack_start(hbox1,True,True,0)
		#***************************************************************
		scrolledwindow = Gtk.ScrolledWindow()
		scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
		scrolledwindow.set_shadow_type(Gtk.ShadowType.ETCHED_OUT)		
		scrolledwindow.set_size_request(450, 450)
		hbox1.pack_start(scrolledwindow,True,True,0)
		#
		self.model = Gtk.ListStore(GObject.TYPE_BOOLEAN, GObject.TYPE_BOOLEAN, GObject.TYPE_STRING)
		#
		self.treeview = Gtk.TreeView()
		self.treeview.set_model(self.model)
		scrolledwindow.add(self.treeview)
		#	
		self.column_mou = Gtk.TreeViewColumn('Mounted')
		self.column_aut = Gtk.TreeViewColumn('Automount')
		self.column_pth = Gtk.TreeViewColumn('Path')
		#
		self.cell_mou = Gtk.CellRendererToggle()
		self.cell_aut = Gtk.CellRendererToggle()
		self.cell_pth = Gtk.CellRendererText()
		self.cell_mou.set_property('activatable', True)
		self.cell_aut.set_property('activatable', True)
		self.cell_pth.set_property('editable', False)
		self.cell_mou.connect('toggled', self.toggled, (self.model,0))
		self.cell_aut.connect('toggled', self.toggled_automount, (self.model,1))
		self.column_mou.pack_start(self.cell_mou, True)
		self.column_aut.pack_start(self.cell_aut, True)
		self.column_pth.pack_start(self.cell_pth, True)
		self.column_mou.add_attribute(self.cell_mou, 'active',0)
		self.column_aut.add_attribute(self.cell_aut, 'active',1)
		self.column_pth.add_attribute(self.cell_pth, 'text',2)
		#
		self.treeview.append_column(self.column_mou)
		self.treeview.append_column(self.column_aut)
		self.treeview.append_column(self.column_pth)
		#
		#***************************************************************
		vbox2 = Gtk.VBox(spacing = 5)
		vbox2.set_border_width(5)
		hbox1.pack_start(vbox2,False,False,0)
		#
		button_add = Gtk.Button()
		image_add = Gtk.Image()
		image_add.set_from_stock(Gtk.STOCK_ADD,Gtk.IconSize.LARGE_TOOLBAR)
		button_add.set_image(image_add)
		button_add.connect('clicked',self.on_button_add_clicked)
		button_add.set_tooltip_text(_('Add new encrytped folder'))
		vbox2.pack_start(button_add,False,False,0)
		#
		button_remove = Gtk.Button()
		image_remove = Gtk.Image()
		image_remove.set_from_stock(Gtk.STOCK_REMOVE,Gtk.IconSize.LARGE_TOOLBAR)
		button_remove.set_image(image_remove)
		button_remove.connect('clicked',self.on_button_remove_clicked)
		button_remove.set_tooltip_text(_('Remove encrytped folder from indicator but not delete'))
		vbox2.pack_start(button_remove,False,False,0)
		#
		button_edit = Gtk.Button()
		image_edit = Gtk.Image()
		image_edit.set_from_stock(Gtk.STOCK_EDIT,Gtk.IconSize.LARGE_TOOLBAR)
		button_edit.set_image(image_edit)
		button_edit.connect('clicked',self.on_button_edit_clicked)
		button_edit.set_tooltip_text(_('Edit encrypted folder properties'))
		vbox2.pack_start(button_edit,False,False,0)
		#
		button_import = Gtk.Button()
		image_import = Gtk.Image()
		image_import.set_from_stock(Gtk.STOCK_CONVERT,Gtk.IconSize.LARGE_TOOLBAR)
		button_import.set_image(image_import)
		button_import.connect('clicked',self.on_button_import_clicked)
		button_import.set_tooltip_text(_('Import encrypted folder to indicator'))
		vbox2.pack_start(button_import,False,False,0)		
		#***************************************************************
		self.show_all()
		#
		self.load_preferences()
		#
		if self.run() == Gtk.ResponseType.ACCEPT:
			self.ok = True
		else:
			self.ok = False
		self.destroy()
	
	def on_button_import_clicked(self,widget):
		widget.set_sensitive(False)
		ce = CreateEncfs(self,import_folder = True)
		self.load_preferences()
		widget.set_sensitive(True)
	
	def on_button_add_clicked(self,widget):
		widget.set_sensitive(False)
		ce = CreateEncfs(self)
		self.load_preferences()
		widget.set_sensitive(True)
		
	def on_button_edit_clicked(self,widget):
		if len(self.treeview.get_selection().get_selected_rows()[1])>0:
			widget.set_sensitive(False)
			row = self.treeview.get_selection().get_selected_rows()[1][0]
			print(row)
			path = self.model[row][2]
			ee = CreateEncfs(self,epath = path)
			self.load_preferences()
			widget.set_sensitive(True)

	def on_button_remove_clicked(self,widget):
		if self.treeview.get_selection().count_selected_rows()>0:
			widget.set_sensitive(False)
			#
			row = self.treeview.get_selection().get_selected_rows()[1][0]
			path = self.model[row][2]
			print(path)
			msg =_('Are you sure to remove from CryptFolder-Indicator this encrypted\n folder? %s')%(path)
			md =Gtk.MessageDialog(parent = self, flags = Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, type = Gtk.MessageType.QUESTION, buttons = Gtk.ButtonsType.YES_NO, message_format = msg)
			if md.run() == Gtk.ResponseType.YES:
				gnomeencfsmod.remove_folder(path)
			md.destroy()
			#
			self.load_preferences()
			widget.set_sensitive(True)
			
	def toggled_automount(self,widget,row,liststore):
		before = liststore[0][row][1]
		after = not before
		liststore[0][row][1] = after
		path = liststore[0][row][2]
		gnomeencfsmod.edit_folder(path,new_automount = after)

	def toggled(self,widget,row,liststore):
		before = liststore[0][row][0]
		after = not before
		liststore[0][row][0] = after
		path = liststore[0][row][2]
		if after == True:
			gnomeencfsmod.mount_folder(path)			
		else:
			gnomeencfsmod.unmount_folder(path)

	def close_application(self, widget):
		self.ok = False
		self.destroy()
		
	def load_preferences(self):
		self.model.clear()
		folders = gnomeencfsmod.get_folders()
		for folder in folders:
			self.model.append([folder['mounted'],folder['auto-mount']=='yes',folder['encfs-path']])
		
	def save_preferences(self):
		pass
if __name__ == "__main__":	
	cm = CM()
	exit(0)
