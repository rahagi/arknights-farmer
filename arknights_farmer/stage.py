# -*- coding: utf-8 -*-

class Stage:

    EVENT_STAGES = []
    CHIP_STAGES = {
        'a': 'solid defense',
        'b': 'fierce attack',
        'c': 'unstoppable charge',
        'd': 'fearless protection'
    }
    SUPPLY_STAGES = {
        'ap': 'tough siege',
        'ca': 'aerial threat',
        'ce': 'cargo escort',
        'ls': 'tactical drill',
        'sk': 'resource search'
    }

    def __init__(self, name):
        self.name = name.lower()
        self.identify()
    
    def __hash__(self):
        return hash((self.name))
    
    def __eq__(self, other):
        return self.name == other.name

    def identify(self):
        s_prefix = self.name.split('-')[0]
        s_suffix = self.name.split('-')[-1:][0]
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
                self.title = self.CHIP_STAGES[self.name.split('-')[1]]
            else:
                self.classifier = 'supplies'
                self.title = self.SUPPLY_STAGES[s_prefix]
        else:
            self.classifier = 'event'
        self.level = s_suffix