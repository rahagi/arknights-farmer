# -*- coding: utf-8 -*-
import os
from random import randint
from ..stage import Stage
from gacha_elper.elper import Elper, cv2, np
from gacha_elper.elper import Coordinate as Coord
from gacha_elper.adb import Adb

class Elp(Elper):

    @classmethod
    def __update_screen(self, bgr=0):
        self.CURRENT_SCREEN = self.__get_current_screen(bgr)

    @classmethod
    def __get_current_screen(self, bgr=0):
        img = None
        while img is None:
            img = cv2.imdecode(np.fromstring(Adb.exec_out('screencap -p'), dtype=np.uint8), bgr)
        return img

    @classmethod
    def __delete_screen(self):
        self.CURRENT_SCREEN = np.array([[]])

    @classmethod
    def __find_stage_boxes(self, stage):
        self.__update_screen()
        subdir = f'stages/{stage.chapter}/s' if stage.issstages else f'stages/{stage.chapter}'
        maps = {}
        for file_ in os.scandir(f'{self.CURRENT_DIR}/assets/{subdir}'):
            if file_.is_file():
                stage_name = file_.name.split('.')[0]
                stage_coord = Elp.find(f'{subdir}/{stage_name}', sim_from=0.98, sim_to=0.95, update_screen=False)
                if stage_coord:
                    maps[stage_name] = stage_coord
        return maps

    @classmethod
    def find_current_chapter(self):
        self.__update_screen()
        self.CURRENT_SCREEN = self.CURRENT_SCREEN[670:700, 1058:1111]
        for i in range(1, 6):
            if Elp.find(f'chapter/{i}', sim_from=0.95, sim_to=0.9, update_screen=False):
                cv2.imwrite('yeet.png', self.CURRENT_SCREEN)
                return i

    @classmethod
    def find_stage(self, stage):
        current_stages = self.__find_stage_boxes(stage)
        if stage.name not in current_stages:
            current_stages = [int(x.split('-')[1]) for x in list(current_stages.keys())]
            stage_level = int(stage.level)
            swipe_modifier = 0.2
            if stage_level > max(current_stages):
                swipe_modifier = swipe_modifier * (stage_level - max(current_stages))
                Elp.swipe(Coord(640, 360), Coord(640-(640*swipe_modifier), 360))
                self.find_stage(stage)
            elif stage_level < min(current_stages):
                swipe_modifier = swipe_modifier * (min(current_stages) - stage_level)
                Elp.swipe(Coord(640, 360), Coord(640+(640*swipe_modifier), 360))
                self.find_stage(stage)
            else:
                Elp.swipe(Coord(640, 360), Coord(randint(0, 1280), 360))
                self.find_stage(stage)
        else:
            return current_stages[stage.name]
