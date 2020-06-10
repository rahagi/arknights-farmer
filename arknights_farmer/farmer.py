# -*- coding: utf-8 -*-
from .stage import Stage
from .utils.tools import Elp
from .utils.logger import Logger
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
        'auto_toggle': Coord(1150, 600),
        'start1': Coord(1142, 665),
        'start2': Coord(1105, 505),
        'refill': Coord(1100, 575),
        'center': Coord(720, 360)
    }
    
    def __init__(self, task, refill=0):
        self.task = task
        self.refill = refill

    def start(self):
        if not Elp.find('combat'):
            Elp.tap(self.BUTTONS['home1']) 
            Elp.tap(self.BUTTONS['combat2']) 
        else:
            Elp.tap(self.BUTTONS['combat'])
            Elp.wait_until_find('home')
        try:
            for t in self.task:
                Logger.log(f'Doing {t.name} run for {self.task[t]} time(s)')
                if t.classifier == 'supplies':
                    pass
                elif t.classifier == 'chips':
                    pass
                elif t.classifier == 'event':
                    pass
                else:
                    Elp.tap(self.BUTTONS['combat'], delay=2)
                    current_chapter = Elp.find_current_chapter()
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
                    if Elp.find('auto_off'):
                        Logger.log("You don't have auto enabled for this stage! Skipping...", mode='warn')
                        break
                while self.task[t] > 0:
                    Elp.tap(self.BUTTONS['start1'], delay=2.5)
                    if Elp.find('sanity_out', sim_to=0.75):
                        Logger.log('You ran out of sanity')
                        if self.refill <= 0:
                            Logger.log('Ending session...')
                            Logger.log('Saving task...')
                            Elp.save_task(self.task)
                            Elp.exit(0)
                        Logger.log('Refilling sanity...')
                        Elp.tap(self.BUTTONS['refill'], delay=2.6)
                        Elp.tap(self.BUTTONS['start1'])
                        self.refill -= 1
                    Elp.wait_until_find('mission_start')
                    Elp.tap(self.BUTTONS['start2'])
                    Elp.wait_until_find('trust_meter')
                    Elp.tap(self.BUTTONS['center'])
                    Elp.wait_until_find('home')
                    self.task[t] -= 1
                Elp.tap(self.BUTTONS['home1'])
                Elp.tap(self.BUTTONS['combat2'])
                del(self.task[t])
            Logger.log('Completed all task')
            Logger.log('Exiting...')
        except KeyboardInterrupt:
            Logger.log('Saving task...')
            Elp.save_task(self.task)
            Logger.log('Exiting...')
            Elp.exit(0)
        except Exception as e:
            print(e)
            Logger.log('Something went horribly wrong', mode='error')
            Logger.log('Saving task...')
            Elp.save_task(self.task)
            Logger.log('Exitting...')
            Elp.exit(0)

def parse_task(task):
    if isinstance(task[0], dict):
        return {Stage(x['stage']): int(x['count']) for x in task}
    else:
        return {Stage(x.split(':')[0]): int(float(x.split(':')[1])) for x in task.split(' ')}

def init(refill, task=None):
    task = parse_task(task) if task else Elp.get_recent_task()
    Elp.delete_task()
    if not task:
        Logger.log('Task not found', mode='error')        
        Elp.exit(1)
    c = CombatHandler(task, refill)
    c.start()
