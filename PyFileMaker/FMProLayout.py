# TODO!!!
# PyFileMaker 1.2 - Integrating FileMaker and Python 
# (c) 2002-2003 Pieter Claerhout, pieter@yellowduck.be
# 
# http://www.yellowduck.be/filemaker/


# Import the main modules
import string
from types import *


# Import the FMPro modules
import xml2obj
import FMProXML
from FMProError import *


class FMProLayout( FMProXML.FMProXML ):

	"""Class defining the information about a layout."""

	def __init__( self, data ):

		"""Class constructor"""

		self.data = data
		
		self.errorcode = -1
		self.product = {}
		self.name = ''
		self.database = ''
		self.metadata = {}
		self.resultset = []

		self.doParseResultset()

	def doParseResultset( self ):

		data = self.doParseXMLData()

		self.errorcode = data.getElements( 'ERRORCODE' )[0].getData()

		node = self.doGetXMLElement( data, 'PRODUCT' )
		self.product = self.doGetXMLAttributes( node )

		node = self.doGetXMLElement( data, 'DATABASE' )
		self.database = self.doGetXMLAttribute( node, 'LAYOUT' )
		self.name = self.doGetXMLAttribute( node, 'NAME' )

		node = self.doGetXMLElement( data, 'METADATA' )
		for subnode in self.doGetXMLElements( node, 'FIELD' ):
			fieldData = self.doGetXMLAttributes( subnode )
			self.metadata[fieldData['NAME']] = fieldData
			self.resultset.append( { fieldData['NAME'] : fieldData['TYPE'] } )

	def doShow( self, xml=0 ):
		
		"""Shows the contents of our resultset."""

		if xml == 0:
		
			print 'Errorcode:', self.errorcode
			print 
			
			print 'Product information:'
			for key in self.product.keys():
				print '	 ', key.encode( 'UTF-8' ),
				print '->', self.product[key].encode( 'UTF-8' )

			print
			
			print 'Layout information:'
			print
			print '	  Name ->', self.name
			print '	  Database ->', self.database
			
			print

			print 'Field information:'
			for field in self.metadata.keys():
				print
				print '	  ', field.encode( 'UTF-8' )
				for property in self.metadata[field]:
					print '		  ', property.encode( 'UTF-8' ),
					print '->', self.metadata[field][property].encode( 'UTF-8') 
			
			print

		else:

			tags = [
				'FMPXMLLAYOUT',
				'ERRORCODE',
				'PRODUCT',
				'LAYOUT',
				'FIELD',
				'STYLE',
				'VALUELISTS',
				'VALUELIST',
				'VALUE'
			]

			xml = self.data

			for tag in tags:
				xml = string.replace( xml, '></' + tag, '>\n</' + tag )
				xml = string.replace( xml, '><' + tag, '>\n<' + tag )

			print xml
