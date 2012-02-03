# -*- coding: utf-8 -*-
#   Copyright 2009, 2010 Thomas Olsen <tanghus@gmail.com>
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
#
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import *
from PyKDE4 import plasmascript

class DesktopPopup(QGraphicsWidget):
    def __init__(self,parent):
        QGraphicsWidget.__init__(self)
        self.applet = parent

    def init(self):
        self.count = 0

        # Create controls
        self.edit = Plasma.LineEdit(self)
        self.edit.setText(str(self.count))

        self.button = Plasma.PushButton(self)
        self.button.setText('Change')
        self.button.clicked.connect(self.clicked)

        # Layout
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self)
        self.layout.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.layout.addItem(self.edit)
        self.layout.addItem(self.button)

        self.setLayout(self.layout)

        self.setMinimumWidth(260)
        self.setMinimumHeight(180)

    def clicked(self):
        print 'PyPopup: clicked'
        self.count += 1
        self.edit.setText(str(self.count))