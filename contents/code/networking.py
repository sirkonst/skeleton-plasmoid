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

from PyQt4.QtCore import *
from PyKDE4.kdecore import *
from PyKDE4.solid import *

class Networking():
	def __init__(self, applet):
		self.connected = (Solid.Networking.status() == Solid.Networking.Connected)
		self.applet = applet
		
	def monitorState(self, onDisconnect, onConnect):
		self.applet.connect(Solid.Networking.notifier(), SIGNAL("shouldDisconnect()"), onDisconnect)
		self.applet.connect(Solid.Networking.notifier(), SIGNAL("shouldConnect()"), onConnect)