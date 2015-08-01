#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# Describe classes, methods and functions in a module.
# Works with user-defined modules, all Python library
# modules, including built-in modules.

from gi.repository import GnomeKeyring,GLib
import com
APPID = com.APP

class CFIPasswordManager():
	
	def __init__(self):
		self.keyring = GnomeKeyring.get_default_keyring_sync()[1]
	
	def unlock(self,password):
		result = GnomeKeyring.unlock_sync(self.keyring,password)
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
		info =  GnomeKeyring.get_info_sync(self.keyring)[1]
		return info.get_is_locked()
	
	def exists_folder(self,epath):
		return self.find_folder(epath) != None
	
	def find_folder(self,epath):
		attributes = GnomeKeyring.Attribute.list_new()
		GnomeKeyring.Attribute.list_append_string(attributes, 'appid', APPID)		
		GnomeKeyring.Attribute.list_append_string(attributes, 'encfs-path', epath)
		ff = GnomeKeyring.find_items_sync(GnomeKeyring.ItemType.GENERIC_SECRET, attributes)[1]
		if len(ff)>0:
			return ff[0].item_id, ff[0].secret
		else:
			return None

	def createEncriptedFolder(self,epath,password):
		attributes = GnomeKeyring.Attribute.list_new()
		GnomeKeyring.Attribute.list_append_string(attributes, 'appid', APPID)
		GnomeKeyring.Attribute.list_append_string(attributes, 'encfs-path', str(epath))
		result = GnomeKeyring.item_create_sync (self.keyring, \
		GnomeKeyring.ItemType.GENERIC_SECRET, \
		'Encrypted folder %s'%(epath),attributes, password,True)[0]
		if result == GnomeKeyring.Result.OK:
			return True
		return False

	def removeEncriptedFolder(self,epath):
		id = self.find_folder(epath)
		if id != None:
			GnomeKeyring.item_delete_sync(self.keyring,id[0])
			return True
		return False

if __name__ == '__main__':
	cfipm = CFIPasswordManager()
	'''
	print cfipm.unlock('1234')
	print cfipm.createEncriptedFolder('/home/atareao/','/home/atareao/mount/','1234567')
	print cfipm.find_folder('/home/atareao/')
	print cfipm.exists_folder('/home/atareao/')
	found = cfipm.find_folder('/home/atareao/')
	print cfipm.getattr('/home/atareao/')
	print found
	#print cfipm.changePasswordForEncriptedFolder('/home/atareao/','abcdefgh')
	found = cfipm.find_folder('/home/atareao/')
	print found	
	'''
	print(cfipm.createEncriptedFolder('/home/atareao/','1234'))
	print(cfipm.exists_folder('/home/atareao/'))
	#print cfipm.removeEncriptedFolder('/home/atareao/')
	#print cfipm.exists_folder('/home/atareao/')
	exit(0)
