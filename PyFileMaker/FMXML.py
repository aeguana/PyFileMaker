# PyFileMaker - Integrating FileMaker and Python 
# (c) 2006-2008 Klokan Petr Pridal, klokan@klokan.cz 
# (c) 2002-2006 Pieter Claerhout, pieter@yellowduck.be
# 
# http://code.google.com/p/pyfilemaker/
# http://www.yellowduck.be/filemaker/

# Import the main modules
import string
from types import *
from pprint import pformat


# Import the FM modules
import xml2obj
from FMError import *


class FMXML:

	"""Class defining a basic FMPro XML result."""

	def doParseXMLData( self ):
		
		"""This function parses the XML output of FileMaker."""

		parser = xml2obj.Xml2Obj()
		# Not valid document comming from FMServer
		if self.data[-6:] == '</COL>':
			self.data += '</ROW></RESULTSET></FMPXMLRESULT>'
		xobj = parser.ParseString( self.data )

		try:
			el = xobj.getElements( 'ERRORCODE')
			if el:
				self.errorcode = int( el[0].getData() )
			else:
				self.errorcode = int( xobj.getElements('error')[0].getAttribute('code') )
		except:
			FMErrorByNum( 954 )

		if self.errorcode != 0:
			FMErrorByNum( self.errorcode )

		return xobj


	def __getitem__( self, key ):
		
		"""Returns a specific element from the resultset."""

		return self.resultset[key]


	def __repr__( self ):

		return "<%s instance WITH LIST OF %s RECORDS (total-count is %d)>\n%s" % (str(self.__class__), len(self), int(self.database['total-count']), pformat( self.resultset))
		#return "<%s instance with %s records>\n%s" % (str(self.__class__), len(self), pformat(self.resultset))

	def __len__( self ):
		
		"""Returns the length of the resultset. This is the same as the number
		of records that were found."""

		return len( self.resultset )


	def doGetXMLElement( self, dom, elementName ):
		
		"""Get a single element from a DOM element."""

		return dom.getElements( elementName )[0]


	def doGetXMLElements( self, dom, elementName ):
		
		"""Get a list of elements from a DOM element."""

		return dom.getElements( elementName )


	def doGetXMLAttribute( self, dom, attribute ):
		
		"""Get a list of elements from a DOM element."""

		return dom.getAttribute( attribute )


	def doGetXMLAttributes( self, dom ):
		
		"""Get a list of attributes from a DOM element."""

		return dom.attributes
