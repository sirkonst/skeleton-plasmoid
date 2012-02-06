# -*- coding: utf-8 -*-

# Copyright (C) 2009  Mark McCans <mjmccans@gmail.com>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
from PyKDE4.kdecore import *

def createDirectory(name):
	if not os.path.isdir(name):
		try:
			os.mkdir(name)
		except:
			print 'Failed to create directory: ' + name
			
def kdeHome():
	return unicode(KGlobal.dirs().localkdedir())
	
def createNotifyrc(kdehome):
	# Create gmail-plasmoid directory if required
	createDirectory(kdehome + 'share/apps/skeleton-plasmoid')

	# File to create
	fn = kdehome + 'share/apps/skeleton-plasmoid/skeleton-plasmoid.notifyrc'

	# File contents
	c = []
	c.append('[Global]\n')
	c.append('IconName=system-run\n')
	c.append('Comment=skeleton plasmoid\n')
	c.append('Name=Skeleton Applet\n')
	c.append('\n')
	c.append('[Event/test-notification]\n')
	c.append('Name=Test notification\n')
	c.append('Name[be]=Теставая апавяшчэнне\n')
	c.append("Sound=KDE-Im-New-Mail.ogg\n")
	c.append("Action=Popup|Sound\n")
	c.append('\n')
	c.append('[Event/button-clicked]\n')
	c.append('Name=Button clicked\n')
	c.append('Name[be]=Кнопка нацiснута\n')
	c.append('Action=Popup\n')

	# Write file
	try:
		f = open(fn, 'w')
		f.writelines(c)
		f.close()
	except:
		print 'Problem writing to file: ' + fn