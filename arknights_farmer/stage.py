# -*- coding: utf-8 -*-
from .utils.tools import Coord
from datetime import datetime, timedelta

class Stage:

    EVENT_STAGES = []
    CHIP_STAGES = {
        'lvlcoord': [Coord(430, 450), Coord(830, 260)],
        'a': ['mon', 'thu', 'fri', 'sun'],
        'b': ['mon', 'tue', 'fri', 'sat'],
        'c': ['wed', 'thu', 'sat', 'sun'],
        'd': ['tue', 'wed', 'sat', 'sun']
    }
    SUPPLY_STAGES = {
        'lvlcoord': [Coord(200, 570), Coord(475, 520), Coord(680, 400), Coord(850, 300), Coord(950, 180)],
        'ap': ['mon', 'thu', 'sat', 'sun'],
        'ca': ['tue', 'wed', 'fri', 'sun'],
        'ce': ['tue', 'thu', 'sat', 'sun'],
        'sk': ['mon', 'wed', 'fri', 'sat']
    }

    def __init__(self, name):
        self.name = name.lower()
        self.identify()
    
    def __hash__(self):
        return hash((self.name))
    
    def __eq__(self, other):
        return self.name == other.name

    def identify(self):
        name = self.name.split('-')
        s_prefix = name[0]
        s_suffix = name[-1:][0]
        self.level = s_suffix
        if any(char.isdigit() for char in s_prefix):
            self.classifier = 'main'
            self.issstages = not s_prefix.isdigit()
            if self.issstages:
                self.chapter = self.name[1]
            else:
                self.chapter = self.name[0]
        elif self.name not in self.EVENT_STAGES:
            if len(self.name.split('-')) == 3:
                self.classifier = 'chips'
                self.opcode = name[1]
                self.isopen = (
                    (datetime.utcnow() - timedelta(hours=7)).strftime('%a').lower()
                    in self.CHIP_STAGES[self.opcode]
                )
                self.coord = self.CHIP_STAGES['lvlcoord'][int(self.level)-1]
            else:
                self.classifier = 'supplies'
                self.opcode = s_prefix
                self.isopen = (
                    (datetime.utcnow() - timedelta(hours=7)).strftime('%a').lower() 
                    in self.SUPPLY_STAGES[self.opcode]
                    or self.opcode == 'ls'
                )
                self.coord = self.SUPPLY_STAGES['lvlcoord'][int(self.level)-1]
        else:
            self.classifier = 'event'
