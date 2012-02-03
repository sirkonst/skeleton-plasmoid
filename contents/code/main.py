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
import ConfigParser

class PyPopup(QGraphicsWidget):
	def __init__(self,parent):
		QGraphicsWidget.__init__(self)
		self.applet = parent

	def init(self):
		self.count = 0
		
		config = ConfigParser.RawConfigParser()
		config.readfp(open(self.applet.package().path() + "contents/data/languages.ini"))
		options = config.items('languages')
		
		# Create controls
		self.selectFrom = Plasma.ComboBox(self)
		self.selectTo = Plasma.ComboBox(self)
		self.webView = Plasma.WebView(self)
		
		for i in options:
			self.selectFrom.addItem(i[0])
			self.selectTo.addItem(i[0])

		self.button = Plasma.PushButton(self)
		self.button.setText('Translate')
		self.button.clicked.connect(self.clicked)

		# Layout
		self.layout = QGraphicsLinearLayout(Qt.Vertical, self)
		self.layout.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
		self.layout.addItem(self.selectFrom)
		self.layout.addItem(self.selectTo)
		self.layout.addItem(self.webView)
		self.layout.addItem(self.button)
		self.setLayout(self.layout)

		self.setMinimumWidth(260)
		self.setMinimumHeight(180)

	def clicked(self):
		print 'PyPopup: clicked'
		self.count += 1

class Skeleton(plasmascript.Applet):
	def __init__(self, parent, args=None):
		plasmascript.Applet.__init__(self,parent)

	def init(self):
		# popup window object
		self._widget = None
		
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
		
		
		
		
		

		self.icon = Plasma.IconWidget()
		self.layout.addItem(self.icon)
		
		# Only register the tooltip in panels
		if ((self.formFactor() == Plasma.Horizontal) or (self.formFactor() == Plasma.Vertical)):
			Plasma.ToolTipManager.self().registerWidget(self.applet)
			print("PyPopupApplet: In Panel")
		else:
			Plasma.ToolTipManager.self().unregisterWidget(self.applet)
			print("PyPopupApplet: Not in Panel")

		loader = KIconLoader()
		size = min(self.icon.size().width(), self.icon.size().height()) * 2
		pix = KIconLoader.loadIcon(loader, self.package().path() + "contents/icons/google.png", KIconLoader.NoGroup, size)
		paint = QPainter(pix)
		paint.setRenderHint(QPainter.SmoothPixmapTransform)
		paint.setRenderHint(QPainter.Antialiasing)
		paint.end()
		
		self._widget = PyPopup(self)
		self._widget.init()
		self.setGraphicsWidget(self._widget)
		self.applet.setPassivePopup(True)
		self.setPopupIcon(self.package().path() + "contents/icons/google.png")
		self.setGraphicsWidget(self._widget)
		
		
	def iconClicked(self):

		print self._widget
		
def CreateApplet(parent):
	return Skeleton(parent)