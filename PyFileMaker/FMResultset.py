# PyFileMaker - Integrating FileMaker and Python
# (c) 2014-2016 Marcin Kawa, kawa.macin@gmail.com
# (c) 2006-2008 Klokan Petr Pridal, klokan@klokan.cz 
# (c) 2002-2006 Pieter Claerhout, pieter@yellowduck.be
# 
# http://code.google.com/p/pyfilemaker/
# http://www.yellowduck.be/filemaker/

# Import the main modules
import string
from types import *
import re

# Import the FMPro modules
import xml2obj
import FMXML
from FMError import *
from FMData import makeFMData

class FMResultset(FMXML.FMXML):
	"""Class defining the information about a resultset."""

	def __init__(self, data):
		"""Class constructor"""

		self.data = data
		self.errorcode = -1
		self.product = {}
		self.database = {}
		self.metadata = {}
		self.resultset = []
		self.fieldNames = []

		self.doParseResultset()

	def doParseResultset(self):
		data = self.doParseXMLData()

		self.errorcode = self.doGetXMLElement(data, 'error').getAttribute('code')

		node = self.doGetXMLElement(data, 'product')
		self.product = self.doGetXMLAttributes(node)

		node = self.doGetXMLElement(data, 'datasource')
		self.database = self.doGetXMLAttributes(node)

		node = self.doGetXMLElement(data, 'metadata')
		for subnode in self.doGetXMLElements(node, 'field-definition'):
			fieldData = self.doGetXMLAttributes(subnode)
			self.metadata[fieldData['name']] = fieldData
			self.fieldNames.append(fieldData['name'])

		node = self.doGetXMLElement(data, 'resultset')
		for record in self.doGetXMLElements(node, 'record'):

			recordDict = dict()
			for column in self.doGetXMLElements(record, 'field'):
				fieldname = self.doGetXMLAttribute(column, 'name')
				try:
					if int(self.metadata[fieldname]['max-repeat']) > 1:
						recordDict[fieldname] = [i.getData() for i in self.doGetXMLElements(column, 'data') if i.getData() != '']
					else:
						recordDict[fieldname] = self.doGetXMLElement(column, 'data').getData()
				except Exception as e:
					recordDict[fieldname] = ''.encode('UTF-8')
					# it means there are no data for this column!!!
					#  -> and it's not possible to modify it later
					#recordDict[fieldname] = None
				if fieldname.find('::') != -1:
					subfield = fieldname[:fieldname.find('::')]
					subname = fieldname[fieldname.find('::')+2:]
					if not recordDict.has_key(subfield):
						recordDict[subfield] = dict()
					recordDict[subfield][subname] = recordDict[fieldname]
					del(recordDict[fieldname])

			recordDict['RECORDID'] = int(
				re.sub('[^\d+]', '', self.doGetXMLAttribute(record, 'record-id'))
			)
			recordDict['MODID'] = int(
				self.doGetXMLAttribute(record, 'mod-id')
			)

			for subnode in self.doGetXMLElements(record, 'relatedset'):

				subnodename = subnode.getAttribute('table')
				if (subnode.getAttribute('count')) > 0 and not recordDict.has_key(subnodename):
					recordDict[subnodename] = []

				for subrecord in self.doGetXMLElements(subnode, 'record'):

					subrecordDict = dict()
					for subcolumn in self.doGetXMLElements(subrecord, 'field'):
						fieldname = self.doGetXMLAttribute(subcolumn, 'name')
						if fieldname.startswith(subnodename):
							fieldname = fieldname[len(subnodename)+2:]
						try:
							subrecordDict[fieldname] = self.doGetXMLElement(subcolumn, 'data').getData()
						except:
							subrecordDict[fieldname] = ''.encode('UTF-8')

						if fieldname.find('::') != -1:
							subfield = fieldname[:fieldname.find('::')]
							subname = fieldname[fieldname.find('::')+2:]
							if not subrecordDict.has_key(subfield):
								subrecordDict[subfield] = dict()
							subrecordDict[subfield][subname] = subrecordDict[fieldname]
							del(subrecordDict[fieldname])

					subrecordDict['RECORDID'] = int(self.doGetXMLAttribute(subrecord, 'record-id'))
					subrecordDict['MODID'] = int(self.doGetXMLAttribute(subrecord, 'mod-id'))
				   
					done = False
					for rec in recordDict[subnodename]:
						if rec['RECORDID'] == subrecordDict['RECORDID']:
							#rec.update(subrecordDict)
							for sub in subrecordDict:
								if sub in ['RECORDID','MODID']:
									pass
								elif rec.has_key(sub) and type(rec[sub])==dict:
									rec[sub].update(subrecordDict[sub])
								else:
									rec[sub] = subrecordDict[sub]

							done = True
					if not done:
						recordDict[subnodename].append(subrecordDict)

			self.resultset.append(makeFMData(recordDict))

	def doShow(self, xml=0):
		"""Shows the contents of our resultset."""

		if xml == 0:
			print 'Errorcode:', self.errorcode
			print 
			
			print 'Product information:'
			for key in self.product.keys():
				print '	 ', key.encode('UTF-8'),
				print '->', self.product[key].encode('UTF-8')
			print
			
			print 'Database information:'
			for key in self.database.keys():
				print '	 ', key.encode('UTF-8'),
				print'->', self.database[key].encode('UTF-8')
			print
			
			print 'Metadata:'
			for field in self.metadata.keys():
				print
				print '	  ', field.encode('UTF-8')
				for property in self.metadata[field]:
					print '		  ', property.encode('UTF-8'),
					print '->', self.metadata[field][property].encode('UTF-8') 
			print

			print 'Records:'
			for record in self.resultset:
				print
				for column in record:
					print '	  ', column.encode('UTF-8'),
					if type(record[column]) == UnicodeType:
						print '->', record[column].encode('UTF-8')
					else:
						print '->', record[column]

		else:
			tags = [
				'FMPXMLRESULT',
				'ERRORCODE',
				'PRODUCT',
				'DATABASE',
				'METADATA',
				'FIELD',
				'RESULTSET',
				'ROW',
				'COL',
				'DATA'
			]

			xml = self.data

			for tag in tags:
				xml = string.replace(xml, '></' + tag, '>\n</' + tag)
				xml = string.replace(xml, '><' + tag, '>\n<' + tag)

			print xml
