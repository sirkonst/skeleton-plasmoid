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

# utilities
from util import *

# notifications
from notifications import *

class Skeleton(plasmascript.Applet):
	def __init__(self, parent, args=None):
		plasmascript.Applet.__init__(self, parent)
		self.internameName = 'skeleton-plasmoid'
		self.parent = parent

	def init(self):
		# popup window object
		self._widget = None
		self.notifications = Notifications(self)
		
		# Setup configuration
		self.settings = {}
		self.settings['version'] = 0.1
		self.settings['icon'] = 'system-run'
		
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
			# in panel
			Plasma.ToolTipManager.self().registerWidget(self.applet)
		else:
			# not in panel
			Plasma.ToolTipManager.self().unregisterWidget(self.applet)
		
		# define a popup window (on click on icon or when is places on the desktop)
		self._widget = PopupWindow(self)
		self._widget.init()
		self.setGraphicsWidget(self._widget)
		self.applet.setPassivePopup(True)
		self.setPopupIcon(self.icon())
		self.setGraphicsWidget(self._widget)
		
		
	# ---------------------- configuration ------------------------#
	# construct configuration window
	def createConfigurationInterface(self, parent):
		self.configpage = ConfigWindow(self, self.settings)
		page = parent.addPage(self.configpage, i18n(self.name()))
		page.setIcon(KIcon(self.icon()))
		
		self.connect(parent, SIGNAL('okClicked()'), self.configAccepted)
		self.connect(parent, SIGNAL('cancelClicked()'), self.configDenied)
		
	# show configuration window
	def showConfigurationInterface(self):
		plasmascript.Applet.showConfigurationInterface(self)
		return
		
	# if config accepted
	def configAccepted(self):
		icon = self.configpage.ui.icon_path.text()
		conf = self.config()
		conf.writeEntry('icon', str(icon))
		
		print 'config: accepted'
	
	# if config denied
	def configDenied(self):
		print 'config: denied'
		
	# ---------------------- /configuration ------------------------#
	
	# ---------------------- context ---------------------- #
	''' Custom contextual actions '''
	def contextualActions(self):
		actions = []

		refresh = QAction(KIcon('text-speak'), i18n('Notify'), self)
		self.connect(refresh, SIGNAL('triggered()'), self.notifyAction)
		actions.append(refresh)

		return actions
        
        
	''' notify context action '''
	def notifyAction(self):
		self.notifications.notify('button-clicked', i18n('Notification fired.'))
        
	# ---------------------- /context ---------------------- #
	
	# -------------------- utilities ------------------------------- #
def CreateApplet(parent):
	return Skeleton(parent)