import json

class EntityStats():

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class EntityType():

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def stats(self):
        return self._stats

    def __init__(self, name, id, data=None):
        self._name = name
        self._id = id

        if type(data) is dict:
            self._stats = EntityStats(stats)

class EntityMaster():
    _instances = {}

    def __init__(self, name):
        self._objects_id = {}
        self._objects_name = {}
        self._name = name

        EntityMaster._instances[name] = self

    def add(self, entype):
        if isinstance(entype, EntityType):
            self._objects_name[entype.name] = entype
            self._objects_id[entype.id] = entype

    def bring(self, search):
        return (self._objects_name.get(search, None) if type(search) is str else self._objects_id(search, None))
    
    @classmethod
    def get(cls, name):
        return EntityMaster._instances[name]
