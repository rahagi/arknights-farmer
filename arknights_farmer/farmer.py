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
        'next_chp': Coord(1185, 665),
        'prev_chp': Coord(980, 665),
        'auto_toggle': Coord(1150, 600),
        'start1': Coord(1142, 665),
        'start2': Coord(1105, 505),
        'refill': Coord(1100, 575),
        'center': Coord(720, 360),
        'chips': Coord(400, 650),
        'supplies': Coord(250, 650)
    }
    
    def __init__(self, task, refill=0):
        self.task = task
        self.refill = refill

    def terminate(self, code=0):
        Logger.log('Saving task...')
        Elp.save_task(self.task)
        Logger.log('Exitting...')
        Elp.exit(code)

    def start(self):
        if not Elp.find('combat'):
            Elp.tap(self.BUTTONS['home1'])
            Elp.tap(self.BUTTONS['combat2'])
        else:
            Elp.tap(self.BUTTONS['combat'])
            Elp.wait_until_find('home')
        try:
            for stage in list(self.task.keys()):
                Logger.log(f'Doing {stage.name} run for {self.task[stage]} time(s)')
                if stage.classifier == 'supplies' or stage.classifier == 'chips':
                    if not stage.isopen:
                        Logger.log(f'{stage.name.upper()} is currently not open', mode='warn')
                        continue
                    Elp.tap(self.BUTTONS[stage.classifier])
                    op_coord = Elp.find(f'daily_resources/{stage.opcode}', sim_from=0.98, sim_to=0.9)
                    Elp.tap(op_coord)
                    Elp.tap(stage.coord)
                elif stage.classifier == 'event':
                    continue
                else:
                    Elp.tap(self.BUTTONS['combat'], delay=3.5)
                    current_chapter = Elp.find_current_chapter()
                    target_chapter = int(stage.chapter)
                    for _ in range(abs(target_chapter - current_chapter)):
                        if target_chapter > current_chapter:
                            Elp.tap(self.BUTTONS['next_chp'], delay=3)
                        else:
                            Elp.tap(self.BUTTONS['prev_chp'], delay=3)
                    stage_coord = Elp.find_stage(stage)
                    Elp.tap(stage_coord, random_radius=5)
                if Elp.find('auto_off', sim_from=0.9, sim_to=0.8):
                    Elp.tap(self.BUTTONS['auto_toggle'])
                    if Elp.find('auto_off', sim_from=0.9, sim_to=0.8):
                        Logger.log("You don't have auto enabled for this stage! Skipping...", mode='warn')
                        continue
                while self.task[stage] > 0:
                    Elp.tap(self.BUTTONS['start1'], delay=3)
                    if Elp.find('sanity_out', sim_to=0.75):
                        Logger.log('You ran out of sanity')
                        if self.refill <= 0:
                            self.terminate()
                        Logger.log('Refilling sanity...')
                        Elp.tap(self.BUTTONS['refill'], delay=2.6)
                        Elp.tap(self.BUTTONS['start1'])
                        self.refill -= 1
                    Elp.wait_until_find('mission_start')
                    Elp.tap(self.BUTTONS['start2'])
                    Elp.wait_until_find('trust_meter', crop_from=Coord(822, 443), crop_to=Coord(880, 516), interval=1.5)
                    Elp.tap(self.BUTTONS['center'])
                    Elp.wait_until_find('home')
                    self.task[stage] -= 1
                Elp.tap(self.BUTTONS['home1'])
                Elp.tap(self.BUTTONS['combat2'])
                del(self.task[stage])
            Logger.log('Completed all task')
            Logger.log('Exiting...')
        except KeyboardInterrupt:
            self.terminate()
        except Exception as e:
            Logger.log('Something went horribly wrong', mode='error')
            self.terminate(1)

def parse_task(task):
    if isinstance(task[0], dict):
        return {Stage(x['stage']): int(float(x['count'])) for x in task}
    return {Stage(k): int(v) for k, v in (x.split(':') for x in task)}

def init(refill, task=None):
    task = parse_task(task) if task else Elp.get_recent_task()
    Elp.delete_task()
    if not task:
        Logger.log('Task not found', mode='error')        
        Elp.exit(1)
    c = CombatHandler(task, refill)
    c.start()
