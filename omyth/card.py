#!/usr/bin/env python3

import json

class InvalidItem(Exception):
    pass

class BaseCard(object):
    def __init__(self, filename):
        if isinstance(filename, dict):
            j = filename
        else:
            with open(filename) as f:
                j = json.load(f)
        for attrib in j:
            value = j[attrib]
            valid = getattr(self, attrib)
            if isinstance(valid, str):
                if valid != value:
                    raise InvalidItem(attrib + ' of ' + value + ' does not use this class')
            if isinstance(valid, list):
                if isinstance(value, str):
                    if value not in valid:
                        raise InvalidItem(value + ' not in ' +str(valid))
                elif isinstance(value, (list, tuple)):
                    if len(set(value) - set(valid)) > 0:
                        raise InvalidItem('The only valid keys are '+ str(valid))
                else:
                    raise InvalidItem(attrib + ' must be a string')
            elif isinstance(valid, int):
                if not isinstance(value, int):
                    raise InvalidItem(attrib + ' must be a number')
            if isinstance(valid, dict):
                if not isinstance(value, dict):
                    raise InvalidItem(attrib + ' must be a dictionary')
                if len(set(value.keys()) - set(valid.keys())) > 0:
                    raise InvalidItem('The only valid keys are '+ str(list(valid.keys())))

            setattr(self, attrib, value)

    def to_latex

    def __str__(self):
        vals = ('{0}: {1}'.format(value, getattr(self,value)) for value in self.__dict__)
        return '\n'.join(vals)

class UnitCard(BaseCard):
    category = 'mortal, myth, hero'.split(', ')
    name = None
    genus = 'infantry, archer, calvary, monster, winged, animal'.split(', ')
    cost = 0
    health = 0
    attack = dict(normal=0, hero=0, myth=0, mortal=0, player=0)
    picture = None
    artist = None
    special = 'tough, stone, defenseless, massive, companion'.split(', ')
    attribution = 'pd, cc'.split(', ')
    discription = None

class PowerCard(BaseCard):
    category = 'power'
    cost = 0
    special = None
    discription = None

class GodCard(BaseCard):
    category = 'god'
    discription = None
    power = None
    cost = 0
    uses = 1

class AnyCard(UnitCard, PowerCard, GodCard):
    def __new__(cls, filename):
        if isinstance(filename, dict):
            j = filename
        else:
            with open(filename) as f:
                j = json.load(f)
        category = j['category']
        if category == 'power':
            return PowerCard(j)
        elif category == 'god':
            return GodCard(j)
        else:
            return UnitCard(j)

