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
from PyKDE4.plasma import *
from PyKDE4 import plasmascript
from PyKDE4.kdecore import *

class PopupWindow(QGraphicsWidget):
    def __init__(self, parent):
        QGraphicsWidget.__init__(self)
        self.applet = parent

    def init(self):
        # Create controls
        self.notify = Plasma.PushButton(self)
        self.notify.setText(i18n('Create notification'))
        self.notify.clicked.connect(self.applet.notifyAction)
        
        self.fromconfig = Plasma.Label(self)
        self.fromconfig.setText('From config: %s' % self.applet.settings.get('customvalue'))

        # Layout
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self)
        self.layout.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.layout.addItem(self.fromconfig)
        self.layout.addItem(self.notify)
        
        self.setLayout(self.layout)

        self.setMinimumWidth(260)
        self.setMinimumHeight(180)