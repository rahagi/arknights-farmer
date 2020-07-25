# -*- coding: utf-8 -*-
import argparse
from .__init__ import __version__
from .farmer import init
from .utils.tools import Elp
from .utils.logger import Logger

ap = argparse.ArgumentParser(prog='arknights-farmer')
required_args = ap.add_argument_group('required args')
optional_args = ap.add_argument_group('optional args')
required_args.add_argument('-s', '--stage', nargs='+',
                           help='manually add stage(s) to farm task (e.g. 1-7:100 4-4:25 (separated by whitespace))')
required_args.add_argument('-c', '--cont', action='store_true',
                           help='continue from the most recent farming session')
optional_args.add_argument('-r', '--refill', default=0, type=int,
                           help='how many times you want to refill. default is 0')
optional_args.add_argument('-l', '--list-task', action='store_true',
                           help='list unfinished task(s) from recent farming session')
optional_args.add_argument('-v', '--version', action='store_true',
                           help='show version')

def main():
    args = ap.parse_args()
    try:
        recent_task = Elp.get_recent_task()
    except Exception:
        Logger.log('Something went horribly wrong. Saving task...', mode='error')
        Elp.save_task(recent_task)
        Logger.log('Exiting...')
        Elp.exit(1)
    if args.version:
        print(f'arknights-farmer version: {__version__}')
        Elp.exit()
    if args.list_task:
        if recent_task:
            print('Unfinished task(s): ')
            for stage in recent_task:
                print(f' - {stage.name}: {recent_task[stage]} time(s)')
        else:
            Logger.log("You don't have unfinished task")
        Elp.exit()
    if not (args.stage or args.cont):
        ap.error('No argument specified')
    if args.cont:
        init(args.refill)
    else:
        if recent_task:
            Logger.log('You have an unfinished task from the last farming session:', mode='warn')
            for stage in recent_task:
                print(f' - {stage.name}: {recent_task[stage]} time(s)')
            if 'y' in input('Do you want to continue from where you left off? [Y/n]: ').lower():
                init(args.refill)
                Elp.exit()
        init(args.refill, args.stage)

if __name__ == '__main__':
    main()
