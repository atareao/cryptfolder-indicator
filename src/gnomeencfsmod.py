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
import sys
import shutil
import subprocess
import pexpect
from cfkeyringmanager import CFIPasswordManager
from configurator import Configuration
from com import _

MTAB = "/etc/mtab"
FUSERMOUNT = "fusermount"
ENCFS = "encfs"
ENCFSCTL = "encfsctl"
ECHO = "echo"
MOUNT = "mount"
# n for normal mode, p for paranoia mode
MODE = "n"

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
        return "This folder already exists"


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


class LoError(Exception):
    def __str__(self):
            return _('No loopback device available')


class NotDir(Exception):
    def __str__(self):
            return _('This is not a folder')

# =============================================================================
# actions
# =============================================================================


def trai(text):
    if text and text.find(' ') > -1 and text.find('\\') == -1:
        text = text.replace(' ', '\ ')
    return text


def is_folder_mounted(epath):
    """Test if a folder is mounted"""
    folder = _get_items(epath=epath)
    if not folder:
        return False
    mpoint = folder["mount-point"]
    p = subprocess.Popen([MOUNT], stdout=subprocess.PIPE)
    mount = p.communicate()[0].decode('utf-8')
    lines = mount.strip('\n').split('\n')
    points = []
    for line in lines:
        points.append(os.path.abspath(
            line.split('type ')[0].split(' on ')[1].strip()))
    return os.path.abspath(mpoint) in points


def unmount_folder(epath):
    folder = _get_items(epath=epath)
    if not folder:
        return False
    mpoint = folder["mount-point"]
    autodelete = folder['auto-delete']
    secret = get_secret(epath)
    msg = "Unmounting %s from %s: " % (epath, mpoint)
    if os.path.exists(mpoint) is False:
        return True
    if not os.path.isdir(mpoint):
        raise NotDir()
    else:
        cmd = [FUSERMOUNT, "-u", mpoint]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        p.communicate(input=("%s\n" % secret).encode('utf-8'))
        msg += p.returncode and "FAILED" or "OK"
        print('autodelete %s' % autodelete)
        if autodelete == 'yes':
            delete_it(mpoint)
    print(msg)
    return True


def edit_folder(epath,
                new_mpoint=None,
                new_secret=None,
                new_automount=False,
                new_autodelete=False):
    print('Edit folders')
    folder = _get_items(epath=epath)
    if folder is not None:
        mpoint = folder["mount-point"]
        automount = (folder["auto-mount"] == 'yes')
        autodelete = (folder['auto-delete'] == 'yes')
        secret = get_secret(epath)
        if new_mpoint is None and new_secret is None and\
                new_automount == automount and new_autodelete == autodelete:
            return True
        if new_secret is not None and secret != new_secret:
            p1 = subprocess.Popen(
                [ECHO, "-e", secret + "\n" + new_secret + "\n"],
                stdout=subprocess.PIPE)
            p2 = subprocess.Popen(
                [ENCFSCTL, "autopasswd", epath],
                stdin=p1.stdout, stdout=subprocess.PIPE)
            p2.communicate()[0]
            if p2.poll() is not 0:
                raise BadPassword()
            cfipm = CFIPasswordManager()
            cfipm.createEncriptedFolder(epath, new_secret)
        if new_mpoint is not None and new_mpoint != mpoint:
            if is_folder_mounted(epath) is True:
                if unmount_folder(epath) is False:
                    raise NotUnmount()
            try:
                delete_it(mpoint)
            except Exception as e:
                print(e)
            delete_it(new_mpoint)
            if not os.path.exists(new_mpoint):
                os.mkdir(new_mpoint)
            mpoint = new_mpoint
        # update item data
        configuration = Configuration()
        configuration.set_folder_mount_point(epath, mpoint)
        if new_automount is True:
            configuration.set_folder_auto_mount(epath, 'yes')
        else:
            configuration.set_folder_auto_mount(epath, 'no')
        if new_autodelete is True:
            configuration.set_folder_auto_delete(epath, 'yes')
        else:
            configuration.set_folder_auto_delete(epath, 'no')
        configuration.save()
    return True


def is_folder_stored(epath):
    if _get_items(epath=epath):
        return True
    return False


def is_folder_encrypted(epath):
    """Check if 'epath' points to an EncFS directory."""
    # epath = trai(epath)
    p = subprocess.Popen(["encfsctl", "info", epath],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    p.communicate()
    return p.returncode == 0


def import_folder(epath, mpoint, secret, automount, autodelete):
    if _get_items(epath=epath):
        return True
    configuration = Configuration()
    configuration.create_folder(epath, mpoint, automount, autodelete)
    configuration.save()
    cfipm = CFIPasswordManager()
    cfipm.createEncriptedFolder(epath, secret)
    return True


def add_folder(epath, mpoint, secret, automount, autodelete):
    print(is_folder_encrypted(epath))
    if is_folder_encrypted(epath):
        raise AlreadyEncrypted()
        return False
    """Add new EncFS item to keyring."""
    print(_get_items(epath=epath))
    if _get_items(epath=epath):
        return True
    configuration = Configuration()
    configuration.create_folder(epath, mpoint, automount, autodelete)
    configuration.save()
    cfipm = CFIPasswordManager()
    cfipm.createEncriptedFolder(epath, secret)

    return create_crypted_folder(epath, mpoint, secret)


def create_crypted_folder(epath, mpoint, secret):
    print("Encrypting...")
    if os.path.exists(epath):
        shutil.rmtree(epath)
    os.makedirs(epath)
    if os.path.exists(mpoint):
        shutil.rmtree(mpoint)
    os.makedirs(mpoint)
    command = 'encfs "%s" "%s"' % (epath, mpoint)
    print(command)
    child = pexpect.spawn(command)
    child.logfile = sys.stdout
    child.expect('\n')
    child.sendline('x')
    child.expect('\n')
    child.sendline('1')
    # Selected key size
    child.expect('\n')
    child.sendline('256')
    # filesystem block size
    child.expect('\n')
    child.sendline('1024')
    # The following filename encoding algorithms are available
    child.expect('\n')
    child.sendline('3')
    # Enable filename initialization vector chaining
    child.expect('\n')
    child.sendline('n')
    # Enable per-file initialization vectors
    child.expect('\n')
    child.sendline('n')
    # Enable block authentication code headers
    child.expect('\n')
    child.sendline('n')
    # Add random bytes to each block header
    child.expect('\n')
    child.sendline('0')
    # Enable file-hole pass-through
    child.expect('\n')
    child.sendline('y')
    # New Encfs Password
    child.expect('\n')
    child.sendline(secret)
    # Verify Encfs Password
    child.expect('\n')
    child.sendline(secret)
    child.expect(pexpect.EOF, timeout=None)
    child.close()
    return True


def remove_folder(epath):
    """Remove EncFS item from keyring."""
    if is_folder_mounted(epath) is True:
        print('Is folder mounted')
        if unmount_folder(epath) is False:
            raise NotUnmount()
    '''
    if delete_it(epath) is False:
        raise NotUnmount()
    '''
    folder = _get_items(epath)
    if folder:
        mpoint = folder['mount-point']
        if delete_it(mpoint) is False:
            raise NotUnmount()
    configuration = Configuration()
    configuration.delete_folder(epath)
    configuration.save()
    cfipm = CFIPasswordManager()
    cfipm.removeEncriptedFolder(epath)
    return True


def delete_it(folder):
    if os.path.exists(folder):
        if os.path.isdir(folder):
            try:
                shutil.rmtree(folder)
            except Exception as e:
                print(e)
        else:
            try:
                os.remove(folder)
            except Exception as e:
                print(e)
    return True


def get_automount(epath):
    folder = _get_items(epath=epath)
    if folder:
        return folder['auto-mount'] == 'yes'
    return NoEncrypted()


def get_autodelete(epath):
    folder = _get_items(epath=epath)
    if folder:
        return folder['auto-delete'] == 'yes'
    return NoEncrypted()


def get_mpoint(epath):
    folder = _get_items(epath=epath)
    if folder:
        return folder['mount-point']
    return NoEncrypted()


def get_secret(epath):
    cfipm = CFIPasswordManager()
    ans = cfipm.find_folder(epath)
    if ans:
        return ans[1]
    return NoEncrypted()


def get_folders():
    configuration = Configuration()
    folders = []
    for folder in configuration.get('folders'):
        folder['mounted'] = is_folder_mounted(folder['encfs-path'])
        folders.append(folder)
    return folders


def _get_items(epath=None):
    configuration = Configuration()
    return configuration.get_folder(epath)


def mount_folder(epath):
    print('Folder to mount %s' % epath)
    folder = _get_items(epath=epath)
    if not folder:
        return False
    if is_folder_mounted(epath):
        return True
    mpoint = folder["mount-point"]
    print('Mounting %s on %s' % (epath, mpoint))
    secret = get_secret(epath)
    print("Mounting...")
    if not os.path.exists(mpoint):
        os.makedirs(mpoint)
    p1 = subprocess.Popen([ECHO, secret], stdout=subprocess.PIPE)
    p2 = subprocess.Popen([ENCFS, "-S", epath, mpoint, "--", "-o", "nonempty"],
                          stdin=p1.stdout, stdout=subprocess.PIPE)
    p2.communicate()[0]
    if p2.poll() is not 0:
        raise BadPassword()
    print('Mounted')
    return True


def list_items():
    """List EncFS items in keyring."""
    items = get_folders()
    for item in items:
        epath = item["encfs-path"]
        mpoint = item["mount-point"]
        amount = item["auto-mount"]
        autodelete = item["auto-delete"]
        print("* encfs path  : %s" % epath)
        print("  mount point    : %s" % mpoint)
        print("  mount at login : %s" % amount)
        print("  autodelete : %s" % autodelete)
    return True


if __name__ == '__main__':
    print(create_crypted_folder('/home/atareao/Dropbox/encfs2/',
                                '/home/atareao/Documentos/Safe2/',
                                '123456'))
    exit(0)
