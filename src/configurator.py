#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#
# Copyright (C) 2010 Lorenzo Carbonell
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
import codecs
import os
import json

import com

def check_autostart_dir():
	if not os.path.exists(com.AUTOSTART_DIR):
		os.makedirs(com.AUTOSTART_DIR)

def create_or_remove_autostart(create):
	check_autostart_dir()
	if create == True:
		if not os.path.exists(com.FILE_AUTO_START):
			shutil.copyfile('/usr/share/cryptfolder-indicator/cryptfolder-indicator-autostart.desktop',com.FILE_AUTO_START)
	else:
		if os.path.exists(com.FILE_AUTO_START):
			os.remove(com.FILE_AUTO_START)


class Configuration(object):
	def __init__(self):
		self.params = com.PARAMS
		self.read()
	
	def get(self,key):
		try:
			return self.params[key]
		except KeyError as e:
			print(e)
			self.params[key] = com.PARAMS[key]
			return self.params[key]
		
	def set(self,key,value):
		self.params[key] = value

	def reset(self):
		if os.path.exists(com.CONFIG_FILE):
			os.remove(com.CONFIG_FILE)		
		self.params = com.PARAMS
		self.save()

	def set_defaults(self):
		self.params = com.PARAMS
		self.save()
	
	def read(self):		
		try:
			f=codecs.open(com.CONFIG_FILE,'r','utf-8')
		except IOError as e:
			print(e)
			self.save()
			f=codecs.open(com.CONFIG_FILE,'r','utf-8')
		try:
			self.params = json.loads(f.read())
		except ValueError as e:
			print(e)
			self.save()
		f.close()

	def save(self):
		if not os.path.exists(com.CONFIG_APP_DIR):
			os.makedirs(com.CONFIG_APP_DIR)
		f=codecs.open(com.CONFIG_FILE,'w','utf-8')
		f.write(json.dumps(self.params))
		f.close()

	def exists_folder(self,name):
		return name in self.params['folders'].keys()
		
	def get_folder(self,name):
		if name in self.params['folders'].keys():
			folder = {}
			folder['encfs-path'] = self.params['folders'][name]['encfs-path']
			folder['mount-point'] = self.params['folders'][name]['mount-point']
			folder['auto-mount'] = self.params['folders'][name]['auto-mount']
			folder['auto-delete'] = self.params['folders'][name]['auto-delete']
			return folder
		return None

	def get_folders(self):
		folders=[]
		for key in self.params['folders'].keys():
			folder = {}
			folder['encfs-path'] = self.params['folders'][key]['encfs-path']
			folder['mount-point'] = self.params['folders'][key]['mount-point']
			folder['auto-mount'] = self.params['folders'][key]['auto-mount']
			folder['auto-delete'] = self.params['folders'][key]['auto-delete']
			folders.append(folder)
		return folders

	def create_folder(self,name,mount_point=None,auto_mount=False,auto_delete=False):
		if not self.exists_folder(name):
			folder = {}
			folder['encfs-path'] = name
			folder['mount-point'] = mount_point
			folder['auto-mount'] = auto_mount
			folder['auto-delete'] = auto_delete
			self.params['folders'][name] = folder
			self.save()

	def delete_folder(self,name):
		if name in self.params['folders'].keys():
			self.params['folders'].pop(name,None)
			self.save()
			return True
		return False

	def get_folder_mount_point(self,name):
		return self.params['folders'][name]['mount-point']

	def get_folder_auto_mount(self,name):
		return self.params['folders'][name]['auto-mount']

	def get_folder_auto_delete(self,name):
		return self.params['folders'][name]['auto-delete']
			
	def set_folder_mount_point(self,name,mount_point):
		self.params['folders'][name]['mount-point'] = mount_point
		self.save()

	def set_folder_auto_mount(self,name,auto_mount):
		self.params['folders'][name]['auto_mount'] = auto_mount
		self.save()

	def set_folder_auto_delete(self,name,auto_delete):
		self.params['folders'][name]['auto_delete'] = auto_delete
		self.save()
			
if __name__ == '__main__':
	conf = Configuration()
	print(conf.exists_folder('test'))
	conf.create_folder('test','/home/',False,True)
	conf.delete_folder('test')
	
