# -*- coding: utf-8 -*-
from random import randint
from ..stage import Stage
from pytesseract import image_to_string
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
    def __find_stage_boxes(self):
        self.__update_screen(1)
        crop_screen = self.CURRENT_SCREEN[150:600]
        crop_screen = cv2.cvtColor(crop_screen, cv2.COLOR_BGR2HSV)
        crop_screen = cv2.GaussianBlur(crop_screen, (7, 7), 0)

        # Color segmentation to find stage boxes
        lower_red = np.array([5, 215, 75])
        upper_red = np.array([15, 255, 107])
        lower_normal = np.array([0, 0, 0])
        upper_normal = np.array([0, 255, 255])
        mask1 = cv2.inRange(crop_screen, lower_normal, upper_normal)
        mask2 = cv2.inRange(crop_screen, lower_red, upper_red)
        mask = cv2.bitwise_or(mask1, mask2)
        thres = cv2.threshold(mask, 0, 255, cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        cnts = list(filter(lambda x: cv2.contourArea(x) > 1000 and cv2.contourArea(x) < 5000, cnts))
        regions = [cv2.boundingRect(x) for x in cnts]
        return {self.ocr(Coord(x[0]+25, x[1]+2), x[2]-8, x[3], False, resize_from=1, resize_to=1.5): Coord(x[0], x[1]) for x in regions}

    @classmethod
    def ocr(self, coord, w, h, invert=False, update_screen=True, resize_from=1, resize_to=1):
        if update_screen or not self.CURRENT_SCREEN:
            self.__update_screen()
        crop_screen = self.CURRENT_SCREEN[coord.y:coord.y+h, coord.x:coord.x+w]
        cv2.imwrite('yeetcropped.png', crop_screen)
        if update_screen:
            self.__delete_screen()
        resize_param = resize_from
        while resize_param <= resize_to:
            crop_resize = cv2.resize(crop_screen.copy(), None, fx=resize_param, fy=resize_param, interpolation=cv2.INTER_CUBIC)
            thres = cv2.threshold(crop_resize, 0, 255, cv2.THRESH_OTSU)[1]
            if invert:
                thres = cv2.bitwise_not(thres.copy())
            res = image_to_string(thres, config='--psm 8')
            print(res, resize_param)
            if res:
                return res
            resize_param += 0.1
        return ''

    @classmethod
    def find_stage(self, stage):
        current_stages = self.__find_stage_boxes()
        if stage.name not in current_stages:
            current_stages = [int(Stage(x).level) for x in list(current_stages.keys())]
            swipe_modifier = 0.1
            if stage.level > max(current_stages):
                swipe_modifier = swipe_modifier * (stage.level - max(current_stages))
                Elp.swipe(Coord(640, 360), Coord(640-(640*swipe_modifier), 360))
                self.find_stage(stage)
            elif stage.level < min(current_stages):
                swipe_modifier = swipe_modifier * (min(current_stages) - stage.level)
                Elp.swipe(Coord(640, 360), Coord(640+(640*swipe_modifier), 360))
                self.find_stage(stage)
            else:
                Elp.swipe(Coord(640, 360), Coord(randint(0, 1280), 360))
                self.find_stage(stage)
        else:
            return current_stages[stage.name]
