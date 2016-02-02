# PyFileMaker - Integrating FileMaker and Python
# (c) 2014-2016 Marcin Kawa, kawa.macin@gmail.com
# (c) 2006-2008 Klokan Petr Pridal, klokan@klokan.cz
# (c) 2002-2006 Pieter Claerhout, pieter@yellowduck.be
# 
# http://code.google.com/p/pyfilemaker/
# http://www.yellowduck.be/filemaker/

__version__ = "3.1"

# Import the main modules
import sys

# Try to import the expat library
try:
	from xml.parsers import expat
except:
	print "Unable to load the EXPAT library. You need to have it installed"
	print "before you can use pyFileMaker."
	sys.exit()

# Import the FileMaker core modules
from FMServer import *
from FMError import *