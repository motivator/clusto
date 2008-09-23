
import re
import itertools

import clusto
from clusto.schema import *
from clusto.exceptions import *

from clustodriver import *


class Driver(object):
    """
    Base Driver.
    """
    
    __metaclass__ = ClustoDriver

    meta_attrs = () # a tuple of (key, value) tuples

    _mixins = set()
    
    _clustoType = "generic"
    _driverName = "entity"
    _reservedAttrs = tuple()

    _properties = dict()
    #_defaultAttrs = tuple()

    def __new__(cls, nameDriverEntity, **kwargs):

	if isinstance(nameDriverEntity, Driver):
	    return nameDriverEntity
	else:
	    return object.__new__(cls, nameDriverEntity, **kwargs)

    def __init__(self, nameDriverEntity, **kwargs):

        if not isinstance(nameDriverEntity, (str, unicode, Entity, Driver)):
            raise TypeError("First argument must be a string, "
                            "Driver, or Entity.")

	if isinstance(nameDriverEntity, Driver):
	    return 

        if isinstance(nameDriverEntity, Entity):
            
            self.entity = nameDriverEntity
            self._chooseBestDriver()

        elif isinstance(nameDriverEntity, (str, unicode)):
            
            self.entity = Entity(nameDriverEntity)
            self.entity.driver = self._driverName
            self.entity.type = self._clustoType

        else:
            raise TypeError("Could not create driver from given arguments.")

        for key, val in kwargs.iteritems():
            if key in self._properties:
                setattr(self, key, val)
            ## unsure if I should fail on bad keys

        
    def __eq__(self, other):

        if isinstance(other, Entity):
            return self.entity.name == other.name
        elif isinstance(other, Driver):
            return self.entity.name == other.entity.name
        else:
            return False

    def __cmp__(self, other):

        return cmp(self.name, other.name)


    def __contains__(self, other):
        return self.hasAttr(key="_contains", value=other)
    
    def _chooseBestDriver(self):
        """
        Examine the attributes of our entity and set the best driver class and
        mixins.
        """

        self.__class__ = DRIVERLIST[self.entity.driver]
    
        

    name = property(lambda x: x.entity.name,
                    lambda x,y: setattr(x.entity, 'name', y))


    def _checkAttrName(self, key):
        """
        check to make sure the key does not contain invalid characters
        raise NameException if fail.
        """

        if not isinstance(key, basestring):
            raise TypeError("An attribute name must be a string.")

        if not re.match('^[A-Za-z_]+[0-9A-Za-z_]*$', key):

            raise NameException("Attribute name %s is invalid. "
                                "Attribute names may not contain periods or "
                                "comas." % key)
    
        
    def _buildKeyName(self, key, numbered=None, subkey=None):

        keyname = key
        if numbered is not None:
            if isinstance(numbered, bool):
                number = self._getAttrNumCount(key, numbered=numbered)
            elif isinstance(numbered, int):
                number = numbered
            else:
                raise TypeError("num must be either True, or an integer.")

            keyname += str(number)

        if subkey: 
            keyname += ''.join(['-', str(subkey)])

        self._checkAttrName(keyname)

        return keyname

    def _getAttrNumCount(self, key, numbered=None):
        """
        For numbered attributes return the count that exist
        """
	
	#import pdb
	#pdb.set_trace()
        attrs = self.attrs(key=key, numbered=numbered)

        return len(list(attrs))

    def _buildKeyRegex(self, key=None, value=None, numbered=None,
                    subkey=None, ignoreHidden=True, strict=False):
            regex = ["^"]

            if key and key.startswith('_'):
                ignoreHidden=False

            if ignoreHidden:
                regex.append("(?!_)")

            regex.append((key and key or ".*"))

            if isinstance(numbered, bool):
                regex.append("\d+")
            elif isinstance(numbered, int):
                regex.append(str(numbered))

            if isinstance(subkey, str):
                regex.append("-%s" % subkey)
            elif subkey is True:
                regex.append("-.+")

            if strict:
                regex.append("$")

            return regex

    @classmethod
    def attrQuery(self, querybase, key=None, value=None, numbered=None,
		  subkey=None, ignoreHidden=True, sortByKeys=True, glob=True, ):

	
	querydict = {}

	query = querybase 


	if key is not None:
	    if glob:
		query = query.filter(Attribute.key.like(key.replace('*', '%')))
	    else:
		query = query.filter_by(key=key)

 	if subkey is not None:
 	    if glob:
 		query = query.filter(Attribute.key.like(subkey.replace('*', '%')))
 	    else:
 		query = query.filter_by(subkey=subkey)

 	if value is not None:
 	    typename = Attribute.getType(value)

 	    if typename == 'relation':
 		query = query.filter_by(relation_id=value)

	    else:
		query = query.filter_by(**{typename+'_value':value})

 	if numbered is not None:
 	    if isinstance(numbered, bool):
 		if numbered == True:
 		    query.filter(Attribute.number != None)
 		else:
 		    query.filter(Attribute.number == None)
 	    elif isinstance(numbered, int):
		query.filter_by(number=numbered)
 		
 	    else:
 		raise TypeError("num must be either a boolean or an integer.")

 	if ignoreHidden:
 	    query.filter(not_(Attribute.key.like('_%')))

	if sortByKeys:
	    query = query.order_by(Attribute.key)

	return query.all()

    def _attrFilter(self, attrlist, key=None, value=None, numbered=None,
		   subkey=None, ignoreHidden=True, 
		   sortByKeys=True, 
		   regex=False, 		   
		   ):
        """
        This function lets you sort through various kinds of attribute lists.
        """


	result = attrlist

	for filterarg, attrname in [(key, 'key'),
				    (subkey, 'subkey'),
				    (value, 'value'), 

				    ]:

	    if filterarg is not None:
		if regex:
		    testregex = re.compile(regex)
		
		    result = [attr for attr in result 
			      if testregex.match(getattr(attr, attrname))]
		else:

		    result = [attr for attr in result 
			      if getattr(attr, attrname) == filterarg]


		    #result = list(result)
		    #print result
		    #print result, filterarg, attrname

	    

	
	if numbered is not None:
	    if isinstance(numbered, bool):
		if numbered:
		    result = (attr for attr in result if attr.number is not None)
		else:
		    result = (attr for attr in result if attr.number is None)

	    elif isinstance(numbered, int):
		result = (attr for attr in result if attr.number == numbered)
	    
	    else:
		raise TypeError("num must be either a boolean or an integer.")

		    
        if value:
            result = (attr for attr in result if attr.value == value)

	
	if ignoreHidden:
	    result = (attr for attr in result if not attr.key.startswith('_'))

	if sortByKeys:
	    result = sorted(result)

        return list(result)

        
    def attrs(self, *args, **kwargs):
        """
        Function to get and filter the attributes of an entity in many
        different ways.

        
        """
	#query = SESSION.query(Attribute)
	#query = query.filter_by(entity_id=self.entity.entity_id)

        #return self._attrQuery(query, *args, **kwargs)

        return self._attrFilter(self.entity._attrs, *args, **kwargs)

    def references(self, *args, **kwargs):

	attrs = self._attrFilter(self.entity._references, *args, **kwargs)

	

# 	query = SESSION.query(Attribute)
# 	query = query.filter_by(relation_id=self.entity.entity_id)

	clustotype = None
 	clustodriver = None

	if 'clustotype' in kwargs:
	    clustotype = kwargs['clustotype']
	    kwargs.pop('clustotype')

	if 'clustodriver' in kwargs:
	    clustodriver = kwargs['clustodriver']
	    kwargs.pop('clustodriver')
 	if clustotype or clustodriver:
 	    
 	    if clustodriver:
 		attrs = (attr for attr in attrs if attr.entity.driver == clustodriver)
 	    if clustotype:
 		attrs = (attr for attr in attrs if attr.entity.type == clustotype)


	return list(attrs)

# 	if clustotype or clustodriver:
# 	    query = query.filter(Entity.entity_id == Attribute.entity_id)
# 	    if clustodriver:
# 		query = query.filter(Entity.driver == clustodriver)
# 	    if clustotype:
# 		query = query.filter(Entity.typ == clustotype)
 
#         attrs = self._attrQuery(query, *args, **kwargs)

#        return attrs
                   
    def attrKeys(self, *args, **kwargs):

        return [x.key for x in self.attrs(*args, **kwargs)]

    def attrKeyTuples(self, *args, **kwargs):

	return [x.keytuple for x in self.attrs(*args, **kwargs)]

    def attrItems(self, *args, **kwargs):
        return [(x.keytuple, x.value) for x in self.attrs(*args, **kwargs)]

    def addAttr(self, key, value, numbered=None, subkey=None):
        """
        add a key/value to the list of attributes

        if numbered is True, append the next available int to the key name.
        if numbered is an int, append that int to the key name
        if subkey is specified append '_subkey' to the key name
         subkeys don't get numbered
        """

	self._checkAttrName(key)
	if subkey:
	    self._checkAttrName(subkey)

	num = None
	if numbered == True:
	    num = self._getAttrNumCount(key, numbered)
	elif isinstance(numbered, int):
	    num = numbered


        if isinstance(value, Driver):
            attr = Attribute(key, value.entity)
        else:
            attr = Attribute(key, value)

	if subkey:
	    attr.subkey = subkey

	if num is not None:
	    attr.number = num


	self.entity._attrs.append(attr)

    def delAttrs(self, *args, **kwargs):
        "delete attribute with the given key and value optionally value also"


        for i in self.attrs(*args, **kwargs):
            self.entity._attrs.remove(i)
            i.delete()

    def setAttr(self, key, value, numbered=None, subkey=None):
        """replaces all items in the list matching the given key with value
        """
        self._checkAttrName(key)
        self.delAttrs(key=key, numbered=numbered, subkey=subkey)
	self.addAttr(key, value, numbered=numbered, subkey=subkey)
	

    
    def hasAttr(self, *args, **kwargs):
        """return True if this list has an attribute with the given key"""

        for i in self.attrs(*args, **kwargs):
            return True

        return False
    
    def iterPools(self, allPools=True):
        """
        Return an iterator that iterates over the pools that a given entity is
        a member of.

        The first pool returned is the most recently added pool in a
        breadthfirst manner.

        So, say I have an entity that was added to pools A, B, C in that order
        and pool A is in pools (A1, B2), pool B is in (B1, A1), pool C is in
        (C1).  Then the returned values will be:

            C, B, A, C1, A1, B1, B2, A1

        In this way the attributes of more recent pools can override the
        attributes of older pools.
        """

        def poolGenerator(entity):


            pools = [Driver(x.entity)
                     for x in sorted(entity.references('_member',
                                                       numbered=True),
                                     cmp=lambda x,y: cmp(x.attr_id, y.attr_id),
                                     reverse=True)]

            while pools:
                pool = pools.pop(0)
                yield pool

                if allPools:
                    pools.extend(list(poolGenerator(pool)))
                            

        return poolGenerator(self)


    def insert(self, thing):
        """
        Insert the given Enity or Driver into this Entity.  Such that:

            A.insert(B)

            (B in A) == True


        """
        if isinstance(thing, Entity):
            d = Driver(Entity)
        elif isinstance(thing, Driver):
            d = thing
        else:
            raise TypeError("Can only insert an Entity or a Driver. "
                            "Tried to insert %s." % str(type(thing)))

        self.addAttr("_contains", d)
        

    @classmethod
    def getByAttr(self, *args, **kwargs):
        """
        Return a list of Instances that have the given attribute with the given
        value.
        """


	querybase = SESSION.query(Attribute)

        #attrlist = SESSION.query(Attribute).filter_by(**querydict)

	attrlist = self.attrQuery(querybase, *args, **kwargs)

        objs = [Driver(x.entity) for x in attrlist]

        return objs
            