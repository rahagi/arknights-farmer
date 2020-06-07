# -*- coding: utf-8 -*-
import argparse
from .penguin import planner
from .farmer import init
from .utils.tools import Elp

ap = argparse.ArgumentParser(prog='arknights-farmer')
required_args = ap.add_argument_group('required args')
optional_args = ap.add_argument_group('optional args')
required_args.add_argument('-p', '--penguin', action='store_true',
                           help='use farm route data from penguin-stats.io')
required_args.add_argument('-s', '--stage',
                           help='manually add stage(s) to farm task (e.g. 1-7:100 4-4:25 (separated by whitespace))')
required_args.add_argument('-c', '--cont', action='store_true',
                           help='continue from the most recent farming session')
optional_args.add_argument('-r', '--refill', default=0, type=int,
                           help='how many times you want to refill. default is 0')

if __name__ == '__main__':
    args = ap.parse_args()
    if not (args.penguin or args.stage or args.cont):
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
        if args.penguin:
            mats_data = input('Paste your material data here:')
            task = planner.get_route(mats_data)
            init(args.refill, task)
        else:
            init(args.refill, args.stage)
