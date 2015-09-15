#!/usr/bin/env python3

import json
from plumbum import local
from plumbum.cmd import inkscape
import tempfile

class InvalidItem(Exception):
    pass

class SVG(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.data = f.read()
    def _repr_svg_(self):
        return self.data
    def replace(self, temp, value):
        self.data = self.data.replace('{'+temp+'}', str(value))
        return self
    def colorize(self, firstcolor, secondcolor):
        self.data = self.data.replace(firstcolor, secondcolor)
        return self
    def save(self, filename):
        with tempfile.NamedTemporaryFile('w') as f:
            f.write(self.data)
            inkscape('-A',filename, f.name)


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
                tmp = valid.copy()
                tmp.update(value)
                value = tmp

            setattr(self, attrib, value)

    def __repr__(self):
        vals = ('{0}: {1}'.format(value, getattr(self,value)) for value in self.__dict__)
        return '\n'.join(vals)

    def save(self, filename):
        self.svg.save(filename)

    def __str__(self):
        return self.svg.data

    def _repr_svg_(self):
        return self.svg._repr_svg_()

class UnitCard(BaseCard):
    template = 'Unit.svg'
    def __init__(self, *args, **kargs):
        self.category = 'mortal myth hero'.split()
        self.name = None
        self.genus = 'infantry archer calvary monster winged animal'.split()
        self.cost = 0
        self.health = 0
        self.attack = 0
        self.hero_attack = 1
        self.armor = dict(slash=0, pierce=0, ranged=0, crush=0, power=0)
        self.attack_class = 'slash pierce ranged crush power'.split()
        self.picture = None
        self.artist = None
        self.special = 'tough stone defenseless ranged unstoppable companion  \
                   attractive companion quick mounted'.split()
        self.attribution = 'pd cc'.split()
        self.discription = None
        super().__init__(*args, **kargs)



    @property
    def svg(self):
        svg = SVG(self.template)
        svg.replace('A', self.attack)
        svg.replace('C', self.cost)
        svg.replace('H', self.health)
        svg.replace('A1', self.armor['slash'])
        svg.replace('A2', self.armor['pierce'])
        svg.replace('A3', self.armor['ranged'])
        svg.replace('A4', self.armor['crush'])
        svg.replace('A5', self.armor['power'])
        svg.replace('TYPE', self.category)
        svg.replace('GENUS', self.genus)
        svg.replace('NAME', self.name)
        svg.replace('DISC', self.discription)
        svg.replace('IMG', self.picture)
        svg.replace('CC', self.attribution)
        svg.replace('ARTIST', self.artist)
        return svg



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

