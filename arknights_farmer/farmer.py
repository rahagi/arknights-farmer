# -*- coding: utf-8 -*-
from .stage import Stage
from .utils.tools import Elp
from gacha_elper.elper import Coordinate as Coord

class CombatHandler:

    BUTTONS = {
        'home1': Coord(270, 38),
        'home2': Coord(90, 283),
        'combat': Coord(995, 200),
        'combat2': Coord(535, 185),
        'supplies': Coord(240, 665),
        'chips': Coord(380, 665),
        'next_chp': Coord(1185, 665),
        'prev_chp': Coord(980, 665),
        'start1': Coord(1142, 665),
        'start2': Coord(1105, 505),
        'center': Coord(720, 360)
    }
    
    def __init__(self, task, refill=0):
        self.task = task
        self.refill = 0

    def start(self):
        if not Elp.find('combat'):
            Elp.tap(self.BUTTONS['home1']) 
            Elp.tap(self.BUTTONS['combat2']) 
        else:
            Elp.tap(self.BUTTONS['combat'])
            Elp.wait_until_find('home')
        for t in self.task:
            if t.classifier == 'supplies':
                pass
            elif t.classifier == 'chips':
                pass
            elif t.classifier == 'event':
                pass
            else:
                Elp.tap(self.BUTTONS['combat'], delay=4)
                current_chapter = Elp.find_current_chapter()
                print(current_chapter)
                target_chapter = int(t.chapter)
                for _ in range(abs(target_chapter - current_chapter)):
                    if target_chapter > current_chapter:
                        Elp.tap(self.BUTTONS['next_chp'], delay=3)
                    else:
                        Elp.tap(self.BUTTONS['prev_chp'], delay=3)
                stage_coord = Elp.find_stage(t)
                Elp.tap(stage_coord)
            if Elp.find('auto_off'):
                Elp.tap(self.BUTTONS['auto_toggle'])
                if Elp.find('auto_off', update_screen=False):
                    break
            while self.task[t] > 0:
                Elp.tap(self.BUTTONS['start1'])
                if Elp.find('sanity_out'):
                    if self.refill <= 0:
                        break
                    Elp.tap(self.BUTTONS['refill'])
                    Elp.tap(self.BUTTONS['start1'], delay=3)
                Elp.wait_until_find('mission_start')
                Elp.tap(self.BUTTONS['start2'])
                Elp.wait_until_find('trust_meter')
                Elp.tap(self.BUTTONS['center'])
                Elp.wait_until_find('home')
                self.task[t] -= 1
            Elp.tap(self.BUTTONS['home1'])
            Elp.tap(self.BUTTONS['home2'])

def parse_task(task):
    if isinstance(task, dict):
        return {Stage(x['stage']): int(x['count']) for x in task}
    else:
        return {Stage(x.split(':')[0]): int(x.split(':')[1]) for x in task.split(' ')}

def init(task, refill):
    task = parse_task(task)
    c = CombatHandler(task, refill)
    c.start()
