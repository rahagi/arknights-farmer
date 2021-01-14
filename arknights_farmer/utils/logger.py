# -*- coding: utf-8 -*-
import os
from datetime import datetime
from .ws_client import WSClient

class Logger:

    if os.name == 'win':
        os.system('color')
    
    DEBUG = False
    MODE = {
        'info': '\033[94m',
        'warn': '\033[93m',
        'error': '\033[91m',
        'end': '\033[0m'
    }

    @classmethod
    def log(self, *msg, mode='info'):
        m = f'[{mode[0].upper()}][{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}] {" ".join(msg)}'
        WSClient.send('on-log', msg)
        print(f'{self.MODE[mode]}{m}{self.MODE["end"]}')

    @classmethod
    def log_debug(self, *msg):
        if self.DEBUG:
            print(f'{self.MODE["warn"]}[D][{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}] {" ".join(msg)}{self.MODE["end"]}')