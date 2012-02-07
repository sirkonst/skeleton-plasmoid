# -*- coding: utf-8 -*-
#   Copyright 2012 Alex Oleshkevich <alex.oleshkevich@gmail.com>
#
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License as
#   published by the Free Software Foundation; either version 2 or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#
#   GNU General Public License for more details
#
#
#   You should have received a copy of the GNU Library General Public
#   License along with this program; if not, write to the
#   Free Software Foundation, Inc.,
#
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *
from util import *
import os

class Notifications():
	def __init__(self, applet):
		self.applet = applet
		self.util = Util(self.applet)
		if not os.path.exists(self.util.kdeHome() + 'share/apps/%s/%s.notifyrc' % (self.applet.name, self.applet.name)):
			if os.path.exists(self.util.kdeHome() + 'share/apps'):
				if os.path.exists(self.applet.package().path() + 'contents/misc/%s.notifyrc' % self.applet.name):
					self.util.createNotifyrc()
		
	''' Raise notification '''
	def notify(self, ntype, message = ''):
		print '[%s]: notifying.. type "%s", message "%s"' % (self.applet.name, ntype, message)
		KNotification.event(ntype, message, QPixmap(self.applet.icon()), None, KNotification.CloseOnTimeout, 
			KComponentData(self.applet.name, self.applet.name, KComponentData.SkipMainComponentRegistration)
		)
		
	