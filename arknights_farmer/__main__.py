# -*- coding: utf-8 -*-
import argparse
from .__init__ import __version__
from .farmer import init
from .utils.tools import Elp

ap = argparse.ArgumentParser(prog='arknights-farmer')
required_args = ap.add_argument_group('required args')
optional_args = ap.add_argument_group('optional args')
required_args.add_argument('-s', '--stage', nargs='+',
                           help='manually add stage(s) to farm task (e.g. 1-7:100 4-4:25 (separated by whitespace))')
required_args.add_argument('-c', '--cont', action='store_true',
                           help='continue from the most recent farming session')
optional_args.add_argument('-r', '--refill', default=0, type=int,
                           help='how many times you want to refill. default is 0')
optional_args.add_argument('-v', '--version', action='store_true',
                           help='show version')

def main():
    args = ap.parse_args()
    if args.version:
        print(f'arknights-farmer version: {__version__}')
        Elp.exit()
    if not (args.stage or args.cont):
        ap.error('no argument specified')
    if args.cont:
        init(args.refill)
    else:
        recent_task = Elp.get_recent_task()
        if recent_task:
            print('You have an unfinished task from the last farming session:')
            for stage in recent_task:
                print(f' - {stage.name}: {recent_task[stage]} time(s)')
            if 'y' in input('Do you want to continue from where you left off? [Y/n]: ').lower():
                init(args.refill)
                Elp.exit()
        init(args.refill, args.stage)

if __name__ == '__main__':
    main()
