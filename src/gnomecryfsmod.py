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
import shutil
import subprocess
from com import _
import re
import tempfile
from distutils.dir_util import copy_tree

MOUNT = '/bin/mount'
FUSERMOUNT = '/bin/fusermount'
CRYFS = '/usr/bin/cryfs'
ECHO = '/bin/echo'

# -----------------------------------------------------------------------

# =============================================================================
# Exceptions
# =============================================================================


class AlreadyEncrypted(Exception):
    def __str__(self):
        return _('This is already a crypted folder')


class BadPassword(Exception):
    def __str__(self):
        return _('The password is wrong')


class MountPointInUse(Exception):
    def __str__(self):
        return _('Mount point already in use')


class NullPassword(Exception):
    def __str__(self):
        return _('Password can not be null')


class AlreadyExists(Exception):
    def __str__(self):
        return _('This folder already exists')


class AlreadyOpened(Exception):
    def __str__(self):
            return _('This folder is already opened')


class NoEncrypted(Exception):
    def __str__(self):
            return "This folder is not crypted"


class NotOpened(Exception):
    def __str__(self):
            return _('This folder is not opened')


class NotUnmount(Exception):
    def __str__(self):
            return _('Not unmount')


class NotMounted(Exception):
    def __str__(self):
            return _('Not mounted')


class LoError(Exception):
    def __str__(self):
            return _('No loopback device available')


class NotDir(Exception):
    def __str__(self):
            return _('This is not a folder')

# =============================================================================
# actions
# =============================================================================


def is_folder_mounted(epath):
    '''Test if a folder is mounted'''
    epath = os.path.realpath(epath)
    p = subprocess.Popen([MOUNT], stdout=subprocess.PIPE)
    mount = p.communicate()[0].decode('utf-8')
    pattern = r'cryfs@(.*)\b\son\s(.*)\b\stype\sfuse.cryfs.*'
    matches = re.findall(pattern, mount)
    for match in matches:
        folder_o, folder_m = match
        if epath == folder_o:
            return True
    return False


def get_folder_where_mounted(epath):
    '''Get where a folder is mounted'''
    epath = os.path.realpath(epath)
    p = subprocess.Popen([MOUNT], stdout=subprocess.PIPE)
    mount = p.communicate()[0].decode('utf-8')
    pattern = r'cryfs@(.*)\b\son\s(.*)\b\stype\sfuse.cryfs.*'
    matches = re.findall(pattern, mount)
    for match in matches:
        folder_o, folder_m = match
        if epath == folder_o:
            return folder_m
    raise NotMounted()
    return None


def is_folder_encrypted(epath):
    """Check if 'epath' points to an EncFS directory."""
    # epath = trai(epath)
    epath = os.path.realpath(epath)
    if is_folder_mounted(epath):
        return True
    return os.path.exists(os.path.join(epath, 'cryfs.config')) and\
        os.path.isfile(os.path.join(epath, 'cryfs.config'))


def remove_folder(epath, mpoint):
    epath = os.path.realpath(epath)
    mpoint = os.path.realpath(mpoint)
    if not is_folder_encrypted(epath):
        raise NoEncrypted()
        return False
    if is_folder_mounted(epath):
        if not unmount_folder(epath):
            raise NotUnmount()
            return False
    if os.path.exists(mpoint):
        shutil.rmtree(mpoint)
    if os.path.exists(epath):
        shutil.rmtree(epath)
    return True


def crypt_folder(epath, mpoint, secret):
    epath = os.path.realpath(epath)
    mpoint = os.path.realpath(mpoint)
    if is_folder_encrypted(epath):
        raise AlreadyEncrypted()
        return False
    tempfolder = None
    os.environ['CRYFS_FRONTEND'] = 'noninteractive'
    os.environ['CRYFS_NO_UPDATE_CHECK'] = 'true'
    if os.path.exists(mpoint):
        tempfolder = tempfile.NamedTemporaryFile().name
        copy_tree(mpoint, tempfolder, update=1)
        shutil.rmtree(mpoint)
    os.makedirs(mpoint)
    if os.path.exists(epath):
        shutil.rmtree(epath)
    os.makedirs(epath)
    p1 = subprocess.Popen([ECHO, secret], stdout=subprocess.PIPE)
    p2 = subprocess.Popen([CRYFS, epath, mpoint],
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    ans = p2.communicate()[0].decode()
    if ans.find('Creating config file (this can take some time)...done') > -1:
        if tempfolder is not None and os.path.exists(tempfolder):
            copy_tree(tempfolder, mpoint, update=1)
            shutil.rmtree(tempfolder)
        return True
    if os.path.exists(tempfolder):
        shutil.rmtree(tempfolder)
    return False


def super_re_crypt_folder(epath, new_epath, mpoint, new_mpoint, secret,
                          new_secret):
    epath = os.path.realpath(epath)
    mpoint = os.path.realpath(mpoint)
    new_epath = os.path.realpath(new_epath)
    new_mpoint = os.path.realpath(new_mpoint)
    if epath != new_epath:
        if mount_folder(epath, mpoint, secret):
            if os.path.exists(new_epath):
                shutil.rmtree(new_epath)
            if os.path.exists(new_mpoint):
                shutil.rmtree(new_mpoint)
            os.environ['CRYFS_FRONTEND'] = 'noninteractive'
            os.environ['CRYFS_NO_UPDATE_CHECK'] = 'true'
            os.makedirs(mpoint)
            os.makedirs(epath)
            p1 = subprocess.Popen([ECHO, secret], stdout=subprocess.PIPE)
            p2 = subprocess.Popen([CRYFS, epath, mpoint],
                                  stdin=p1.stdout, stdout=subprocess.PIPE)
            ans = p2.communicate()[0].decode()
            if ans.find('Creating config file (this can take some time)...\
done') > -1:
                copy_tree(mpoint, new_mpoint, update=1)
                if unmount_folder(epath):
                    if os.path.exists(epath):
                        shutil.rmtree(epath)
                    if os.path.exists(mpoint):
                        shutil.rmtree(mpoint)
                return True
    else:
        if secret == new_secret:
            if mpoint == new_mpoint:
                return True
            else:
                if is_folder_mounted(epath):
                    if unmount_folder(epath):
                        if os.path.exists(mpoint):
                            shutil.rmtree(mpoint)
                return mount_folder(epath, new_mpoint, secret)
        else:
            if not is_folder_mounted(epath):
                if not mount_folder(epath):
                    return False
            tempfolder = tempfile.NamedTemporaryFile().name
            copy_tree(mpoint, tempfolder, update=1)
            if not unmount_folder(epath):
                return False
            if os.path.exists(epath):
                shutil.rmtree(epath)
            if os.path.exists(mpoint):
                shutil.rmtree(mpoint)
            if os.path.exists(new_epath):
                shutil.rmtree(new_epath)
            if os.path.exists(new_mpoint):
                shutil.rmtree(new_mpoint)
            os.environ['CRYFS_FRONTEND'] = 'noninteractive'
            os.environ['CRYFS_NO_UPDATE_CHECK'] = 'true'
            os.makedirs(new_epath)
            os.makedirs(new_mpoint)
            p1 = subprocess.Popen([ECHO, new_secret], stdout=subprocess.PIPE)
            p2 = subprocess.Popen([CRYFS, new_epath, new_mpoint],
                                  stdin=p1.stdout, stdout=subprocess.PIPE)
            ans = p2.communicate()[0].decode()
            if ans.find('Creating config file (this can take some time)...\
done') > -1:
                if tempfolder is not None and os.path.exists(tempfolder):
                    copy_tree(tempfolder, new_mpoint, update=1)
                    shutil.rmtree(tempfolder)
                return True
            if os.path.exists(tempfolder):
                shutil.rmtree(tempfolder)
    return False


def re_crypt_folder(epath, mpoint, secret, new_secret):
    epath = os.path.realpath(epath)
    mpoint = os.path.realpath(mpoint)
    if not is_folder_mounted(epath):
        mount_folder(epath, mpoint, secret)
    tempfolder = tempfile.NamedTemporaryFile().name
    copy_tree(mpoint, tempfolder, update=1)
    if not unmount_folder(epath):
        return False
    os.environ['CRYFS_FRONTEND'] = 'noninteractive'
    os.environ['CRYFS_NO_UPDATE_CHECK'] = 'true'
    if os.path.exists(epath):
        shutil.rmtree(epath)
    os.makedirs(epath)
    if os.path.exists(mpoint):
        shutil.rmtree(mpoint)
    os.makedirs(mpoint)
    p1 = subprocess.Popen([ECHO, new_secret], stdout=subprocess.PIPE)
    p2 = subprocess.Popen([CRYFS, epath, mpoint],
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    ans = p2.communicate()[0].decode()
    if ans.find('Creating config file (this can take some time)...done') > -1:
        if tempfolder is not None and os.path.exists(tempfolder):
            copy_tree(tempfolder, mpoint, update=1)
            shutil.rmtree(tempfolder)
        return True
    if os.path.exists(tempfolder):
        shutil.rmtree(tempfolder)
    return False


def unmount_folder(epath):
    epath = os.path.realpath(epath)
    mpoint = get_folder_where_mounted(epath)
    if mpoint is not None:
        cmd = [FUSERMOUNT, "-u", mpoint]
        msg = "Unmounting %s from %s: " % (epath, mpoint)
        p = subprocess.Popen(cmd,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        p.communicate()[0].decode()
        msg += p.returncode and "FAILED" or "OK"
        print(msg)
        return True
    return False


def mount_folder(epath, mpoint, secret):
    epath = os.path.realpath(epath)
    mpoint = os.path.realpath(mpoint)
    print('Folder to mount %s' % epath)
    os.environ['CRYFS_FRONTEND'] = 'noninteractive'
    os.environ['CRYFS_NO_UPDATE_CHECK'] = 'true'
    p1 = subprocess.Popen([ECHO, secret], stdout=subprocess.PIPE)
    p2 = subprocess.Popen([CRYFS, epath, mpoint],
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    ans = p2.communicate()[0].decode()
    if ans.find('Mounting filesystem. To unmount, call:') > -1:
        return True
    raise BadPassword()
    return False


if __name__ == '__main__':
    # print(is_folder_mounted('/datos/temporal/sample2'))
    # print(unmount_folder('/datos/temporal/sample2'))
    # print(is_folder_encrypted('/datos/temporal/sample2'))
    '''
    print(is_folder_mounted('/datos/temporal/sample2'))
    print(get_folder_where_mounted('/datos/temporal/sample2'))
    unmount_folder('/datos/temporal/sample6')
    print(create_crypted_folder('/datos/temporal/sample6',
                                '/datos/temporal/montado6',
                                'euldlmdc'))
    print('Desmontando:' + str(unmount_folder('/datos/temporal/sample6')))
    print(mount_folder('/datos/temporal/sample6',
                       '/datos/temporal/montado6',
                       'euldlmdc7'))
    '''
    print(re_crypt_folder('/datos/temporal/sample7',
                          '/datos/temporal/montado7',
                          'euldlmdc1',
                          'euldlmdc2'))
    print(unmount_folder('/datos/temporal/sample7'))
    exit(0)

