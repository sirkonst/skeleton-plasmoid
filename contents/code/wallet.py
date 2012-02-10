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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import *
from PyKDE4.kdeui import *

class Wallet():
	def __init__(self, applet):
		self.applet = applet
		self.wallet = None
		self.open()
		
	def open(self):
		self.wallet = KWallet.Wallet.openWallet(KWallet.Wallet.LocalWallet(), 0)
		if self.wallet <> None:
			if not self.wallet.hasFolder(self.applet._name):
				self.wallet.createFolder(self.applet._name)
		self.wallet.setFolder(self.applet._name)

	def close(self):
		self.wallet = None
		
	def readPassword(self, key):
		return self.wallet.readPassword(key)[1]
		
	def writePassword(self, key, value):
		self.wallet.writePassword(key, value)
		
	def getWallet(self):
		return self.wallet