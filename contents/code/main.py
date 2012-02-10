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
from PyKDE4.kio import *
from PyKDE4.solid import *
from PyKDE4.plasma import *
from PyKDE4 import plasmascript
from PyQt4 import QtCore

import os

# popup design
from popupwindow import *

# config tab
from configwindow import *

# notifications
from notifications import *

# config handler
from config import *

# wallet 
from wallet import *

from networking import *

class Skeleton(plasmascript.Applet):
	def __init__(self, parent, args=None):
		plasmascript.Applet.__init__(self, parent)
		self.parent = parent

	def init(self):
		# internal name of package
		self._name = str(self.package().metadata().pluginName());
		
		# popup window object
		self._widget = None
		self.notifications = Notifications(self)
		
		# Setup configuration
		self.settings = Config(self)
		
		# setup wallet
		self.wallet = Wallet(self)
		
		self.networking = Networking(self)
		self.networking.monitorState(self.networkIsDown, self.networkIsUp)
		
		# we have configuration options
		self.setHasConfigurationInterface(True)
		
		# geometry
		self.setAspectRatioMode(Plasma.Square)
		
		# layout
		self.layout = QGraphicsLinearLayout(self.applet)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		self.layout.setOrientation(Qt.Horizontal)
		
		# style
		self.theme = Plasma.Svg(self)
		
		# Only register the tooltip in panels
		if ((self.formFactor() == Plasma.Horizontal) or (self.formFactor() == Plasma.Vertical)):
			# panel mode
			
			# create and set tooltip
			tooltip = Plasma.ToolTipContent()
			tooltip.setMainText(i18n('Skeleton Plasmoid'))
			tooltip.setSubText(i18n('Sample tooltip'))
			tooltip.setAutohide(False)
			Plasma.ToolTipManager.self().setContent(self.applet, tooltip)
			
			Plasma.ToolTipManager.self().registerWidget(self.applet)
		else:
			# desktop mode
			Plasma.ToolTipManager.self().unregisterWidget(self.applet)
		
		# define a popup window
		self._widget = PopupWindow(self)
		self._widget.init()
		self.setGraphicsWidget(self._widget)
		
		self.applet.setPassivePopup(True)
		self.setPopupIcon(self.icon())
		
	# ---------------------- configuration ------------------------#
	def createConfigurationInterface(self, parent):
		self.settings.set('password', self.wallet.readPassword('password'))
		
		self.configpage = ConfigWindow(self, self.settings)
		page = parent.addPage(self.configpage, i18n(self.name()))
		page.setIcon(KIcon(self.icon()))
		
		parent.okClicked.connect(self.configAccepted)
		parent.cancelClicked.connect(self.configDenied)
		
	# show configuration window
	def showConfigurationInterface(self):
		plasmascript.Applet.showConfigurationInterface(self)
		
	# if config accepted
	def configAccepted(self):
		# set input (customvalue, see configwindow.ui) text
		self.settings.set('account', str(self.configpage.ui.account.text()))
		self._widget.fromconfig.setText(self.settings.get('account'))
		self.wallet.writePassword('password', str(self.configpage.ui.password.text()))
		print '[%s]: config accepted' % self._name
	
	# if config denied
	def configDenied(self):
		print '[%s]: config denied' % self._name
	# ---------------------- /configuration ------------------------#
	
	# ---------------------- context ---------------------- #
	''' Custom contextual actions '''
	def contextualActions(self):
		actions = []

		refresh = QAction(KIcon('text-speak'), i18n('Notify'), self)
		refresh.triggered.connect(self.notifyAction)
		actions.append(refresh)

		return actions
	# ---------------------- /context ---------------------- #
        
	''' SLOTS '''
	def notifyAction(self):
		self.notifications.notify('button-clicked', i18n('Notification fired'))
		
	def networkIsDown(self):
		self.notifications.notify('network-down', i18n('Network is down'))
		
	def networkIsUp(self):
		self.notifications.notify('network-up', i18n('Network is up'))
        
	
def CreateApplet(parent):
	return Skeleton(parent)