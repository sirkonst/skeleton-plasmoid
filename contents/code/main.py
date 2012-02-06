# -*- coding: utf-8 -*-
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
from popup import *

# config tab
from config import *

# utilities
from utilities import *

class Skeleton(plasmascript.Applet):
	def __init__(self, parent, args=None):
		plasmascript.Applet.__init__(self,parent)

	def init(self):
		# popup window object
		self._widget = None
		
		# Setup configuration
		self.settings = {}
		self.settings['version'] = 0.1
		conf = self.config()
		
		self.settings['icon'] = conf.readEntry('icon', 'system-run').toString()
		
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
		
		kdehome = kdeHome()
		if not os.path.exists(kdehome + 'share/apps/skeleton-plasmoid/skeleton-plasmoid.notifyrc'):
			if os.path.exists(kdehome + 'share/apps'):
				createNotifyrc(kdehome)
		
		# Only register the tooltip in panels
		if ((self.formFactor() == Plasma.Horizontal) or (self.formFactor() == Plasma.Vertical)):
			# in panel
			Plasma.ToolTipManager.self().registerWidget(self.applet)
		else:
			# not in panel
			Plasma.ToolTipManager.self().unregisterWidget(self.applet)
		
		# define a popup window (on click on icon or when is places on the desktop)
		self._widget = DesktopPopup(self)
		self._widget.init()
		self.setGraphicsWidget(self._widget)
		self.applet.setPassivePopup(True)
		self.setPopupIcon(self.settings['icon'])
		self.setGraphicsWidget(self._widget)
		
		
	# ---------------------- configuration ------------------------#
	# construct configuration window
	def createConfigurationInterface(self, parent):
		self.configpage = Config(self, self.settings)
		p = parent.addPage(self.configpage, i18n('Skeleton'))
		p.setIcon(KIcon(self.icon()))
		
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
        
        # ---------------------- context actions ---------------------- #
        
	''' notify context action '''
	def notifyAction(self):
		self.notify('test-notification', i18n('Notification fired.'))
        
        # ---------------------- /context actions ---------------------- #
        
	# ---------------------- /context ---------------------- #
	
	# ---------------------- notifications ---------------------- #
	
	''' Raise notification '''
	def notify(self, ntype, message = ''):
		print '[skeleton-plasmoid]: notifying.. type "%s", message "%s"' % (ntype, message)
		KNotification.event(ntype, message, QPixmap(self.icon()), None, KNotification.CloseOnTimeout, 
			KComponentData('skeleton-plasmoid', 'skeleton-plasmoid', KComponentData.SkipMainComponentRegistration)
		)
		
	# ---------------------- /notifications  ---------------------- #
	
	
	# -------------------- utilities ------------------------------- #
def CreateApplet(parent):
	return Skeleton(parent)