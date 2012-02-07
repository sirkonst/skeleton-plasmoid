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

import ConfigParser
from util import *

##
# Configuration manager
##
class Config():
	def __init__(self, applet):
		self.applet = applet
		self.util = Util(self.applet)
		self.config = ConfigParser.RawConfigParser()
		self.path = self.util.kdeHome() + 'share/apps/%s/%s.ini' % (self.applet._name, self.applet._name)
		
		if not os.path.exists(self.path):
			if os.path.exists(self.util.kdeHome() + 'share/apps'):
				if os.path.exists(self.applet.package().path() + 'contents/misc/%s.ini' % self.applet._name):
					self.util.createConfig()
					print '[%s]: config created' % self.applet._name
		
		self.config.readfp(open(self.path))
		print '[%s]: config initialized' % self.applet._name
		
	##
	# Read option from configuration file
	#
	# @param key string The option name
	# @param default mixed The default value if option is not found 
	# @param section string [optional] The section to write in
	# @return int|string The value
	def get(self, key, default = '', section = 'general'):
		option = self.config.get(section, key)
		
		if option == None:
			return default
		else:
			return option

	##
	# Set option to configuration file
	#
	# @param key string The option name
	# @param value mixed The value to set
	# @param section string [optional] The section to write in
	# @return void
	def set(self, key, value, section = 'general'):
		self.config.set(section, key, value)
		f = open(self.path, 'w')
		self.config.write(f)
		
	##
	# Get config object
	#
	# @return RawConfigParser
	def getConfig(self):
		return self.config
		
	##
	# Get configuration file path
	#
	# @return string
	def getPath(self):
		return self.path