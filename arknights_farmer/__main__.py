# -*- coding: utf-8 -*-
import argparse
from .penguin import planner
from .farmer import init
from gacha_elper.adb import Adb

ap = argparse.ArgumentParser(prog='arknights-farmer')
required_args = ap.add_argument_group('required args')
optional_args = ap.add_argument_group('optional args')
required_args.add_argument('-p', '--penguin', action='store_true',
                           help='use farm route data from penguin-stats.io')
required_args.add_argument('-s', '--stage',
                           help='manually add stage(s) to farm task (e.g. 1-7:100 4-4:25 (separated by whitespace))')
optional_args.add_argument('-r', '--refill', default=0, type=int,
                           help='how many times you want to refill. default is 0')

if __name__ == '__main__':
    args = ap.parse_args()
    if not (args.penguin or args.stage):
        ap.error('no argument specified')
    if args.penguin:
        mats_data = input('Paste your material data here: ')
        task = planner.get_route(mats_data)
        init(task, args.refill) 
    else:
        init(args.stage, args.refill)