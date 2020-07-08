# -*- coding: utf-8 -*-
import requests
import json

URL = 'https://planner.penguin-stats.io/plan'
HEADERS = {
    'authority': 'planner.penguin-stats.io',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://penguin-stats.io',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://penguin-stats.io/planner',
    'accept-language': 'en-US,en;q=0.9',
}

def get_route(item_requirements):
    item_requirements = json.loads(item_requirements)
    req_data = {
        'required': {},
        'owned': {},
        'exclude': (
            [f'6-{s}' for s in range(1, 18)] +
            [f'S6-{s}' for s in range(1, 5)] +
            [f'7-{s}' for s in range(1, 19)] +
            [f'S7-{s}' for s in range(1, 3)]
        ),
        'extra_outc': False,
        'exp_demand': False,
        'gold_demand': False
    }
    for item in item_requirements:
        req_data['required'][item['name']] = item['need']
        if item['have'] > 0:
            req_data['owned'][item['name']] = item['have']
    try:
        res = requests.post(URL, headers=HEADERS, json=req_data)
        return res.json()['stages']
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
