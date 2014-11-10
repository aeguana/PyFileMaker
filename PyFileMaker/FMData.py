# PyFileMaker - Integrating FileMaker and Python 
# (c) 2006-2008 Klokan Petr Pridal, klokan@klokan.cz 
# (c) 2002-2006 Pieter Claerhout, pieter@yellowduck.be
# 
# http://code.google.com/p/pyfilemaker/
# http://www.yellowduck.be/filemaker/

# Import the main modules
try:
	from mx.DateTime import DateTime, Time, Date
except:
	from datetime import datetime as DateTime, time as Time, date as Date
from re import compile
from FMError import FMError
from UnicodeNormalizer import normalizeUnicode

reDateTime = compile('((\d{2})/(\d{2})/(\d{4}))? ?((\d{2}):(\d{2}):(\d{2}))?')

def key_dict( from_dict ):
	"""Returns dict from_dict['unicode_save_field'] = 'original key with unicode' """
	new_dict = {}
	old2new = {}
	new2old = {}
	for key in from_dict:
		k = normalizeUnicode(key,'identifier')
		if not k: # ignore empty field names
			continue
		i = ''
		while new_dict.has_key("%s%s" % (k,i) ):
			if not i:
				i = 1
			else:
				i += 1
		k = "%s%s" % (k,i)
		if k != key:
			old2new[key] = k
			new2old[k] = key
		new_dict[k] = from_dict[key]
	return (new_dict.keys(), new_dict, old2new, new2old)

def makeFMData( from_dict, locked = False):
	"""Returns FMData structure which is initialized by given dictionary"""

	class FMData(object):
		"""Datastructure where:

			- attr and dict access is equal (eg. FMData.value == FMData['value'])
			- only attributtes given during initialization are readable and writable 
			- modified attributes are tracked"""
		__modified__ = set()
		__slots__, __init_dict__, __old2new__, __new2old__ = key_dict(  from_dict )

		def __init__(self, locked = False):
			init_dict = self.__init_dict__
			for key in init_dict:
				value = init_dict[key]
				date, mo, da, ye, time, ho, mi, se = [None] * 8
				if type(value) in [str, unicode]:
					date, mo, da, ye, time, ho, mi, se = reDateTime.match( value ).groups()
				if type(init_dict[key]) == dict:
					setattr(self, key, makeFMData( init_dict[key], locked=False ) ) # lock all substructures??
				elif type(init_dict[key]) == list:
					l = []
					for d in init_dict[key]:
						if type(d) == dict:
							l.append( makeFMData (d )) # lock ??
						else:
							l.append( d )
					setattr(self, key, l )
				elif date and time:
					setattr(self, key, DateTime(int(ye), int(mo), int(da), int(ho), int(mi), int(se)))
				elif date:
					setattr(self, key, Date(int(ye), int(mo), int(da)))
				elif time:
					setattr(self, key, Time(int(ho), int(mi), int(se)))
				else:
					setattr(self, key, init_dict[key])
			if locked:
				self.__modified__.add('__locked__')

		def __setattr__(self, key, value):
			if '__locked__' in self.__modified__:
				raise AttributeError, "This substructure is read-only, so you cannot modify '%s' attribute." % key
			oldvalue = None
			if hasattr(self, key):
				oldvalue = getattr(self, key)
			#if oldvalue != None and type(oldvalue) != type(value):
			#	 raise TypeError, "Type of field '%s' is %s, you cannot insert %s" % (key, type(oldvalue), type(value))
			object.__setattr__(self, key, value)
			if oldvalue != None and value != oldvalue:
				self.__modified__.add(key)

		def __getitem__(self, key):
			if type(key) == str or type(key) == unicode:
				spl = key.split('.')
			else:
				print "-"*20, key, type(key)
			if len(spl) == 2:
				if self.__old2new__.has_key(spl[0]):
					spl[0] = self.__old2new__[spl[0]]
				if self.__old2new__.has_key(spl[1]):
					spl[1] = self.__old2new__[spl[1]]					
				return getattr( getattr(self, spl[0]), spl[1])
			if self.__old2new__.has_key(key):
				key = self.__old2new__[key]
			return getattr(self, key)

		def __setitem__(self, key, value):
			spl = key.split('.')
			if len(spl) == 2:
				if self.__old2new__.has_key(spl[0]):
					spl[0] = self.__old2new__[spl[0]]
				if self.__old2new__.has_key(spl[1]):
					spl[1] = self.__old2new__[spl[1]]					
				return setattr( getattr(self, spl[0]), spl[1], value)
			if self.__old2new__.has_key(key):
				key = self.__old2new__[key]
			return setattr(self, key, value)

		def __str__(self):
			return object.__repr__(self)

		def __iter__(self):
			l = []
			for key in self.__slots__:
				if hasattr( getattr(self, key), '__slots__'):
					for subkey in getattr(self, key).__slots__:
						l.append( "%s.%s" % (key, subkey))
				else:
					l.append( key )
			l.sort()
			for x in l:
				yield x

		def _modified(self):
			"""Returns tuple (key, value) for modified keys inside of FMData tree (recursive without lists)"""
			l = []
			for key in self.__slots__:
				if hasattr( getattr(self, key), '__modified__'):
					for subkey, value in getattr(self, key)._modified():
						yield ( "%s.%s" % (key, subkey), value )
				else:
					if key in self.__modified__:
						yield (key, getattr( self, key))

		def __repr__(self):
			#from pformat import pformat
			#return "<%s instance with %s records>\n%s" % (str(self.__class__), len(self.__slots__), pformat(dict([(value, getattr(self, value)) for value in self.__slots__])))
			#return pformat(dict([(value, getattr(self, value)) for value in self.__slots__]))
			l = []
			for key in self.__slots__:
				ukey = ""
				if self.__new2old__.has_key(key):
					ukey = " (%s)" % self.__new2old__[key]
				if hasattr( getattr(self, key), '__slots__'):
					for subkey in getattr(self, key).__slots__:
						value = getattr( getattr(self, key), subkey)
						if type(value) == str:
							value = value.decode('utf-8')
						l.append( "%s.%s = '%s'" % (key, subkey, value))
				elif type(getattr(self, key)) == list:
					l.append( "%s%s = <list with %s records>" % (key, ukey, len(getattr(self, key))))
				elif type(getattr(self, key)) == str:
					l.append( "%s%s = '%s'" % (key, ukey, getattr(self, key).decode('utf-8')))
				else:
					l.append( "%s%s = '%s'" % (key, ukey, getattr(self, key)))
			l.sort()
			return str(('\n'.join(l)).encode('utf-8'))


	return FMData( locked )
