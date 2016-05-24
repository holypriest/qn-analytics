#!/usr/bin/python
# -*- coding: utf-8 -*-

''' dump.py: Dumps SciELO Analytics database for Química Nova Journal. This script should run once in a month to update access files '''

import requests
from datetime import datetime
from collections import namedtuple
import pytz
import json

def write_log(cod):
    ''' If something goes wrong, write article cod to log.txt '''
    with open('log.txt', 'a') as f:
        f.write(cod + '\n')

def get_cookie_session(cod):
    ''' Returns the cookie session needed for further access '''
    url = 'http://analytics.scielo.org/w/accesses'
    params = {
        'document': cod,
        'range_start': '0',
        'range_end': datetime.today().strftime('%Y-%m-%d')
    }

    try:
        r = requests.get(url, params=params)
        cookie_session = 'session=%s' % r.cookies['session']
        return cookie_session
    except requests.exceptions.ContentDecodingError as e:
        print('Problem with the %s page request. Skipping...' % cod)
        write_log(cod)
        return None

def get_raw_accesses(cod):
    ''' Returns the raw text containing access data (JSON format) '''
    url = 'http://analytics.scielo.org/ajx/accesses/bymonthandyear'
    params = {
        'code': cod,
        'collection': 'scl',
        'range_start': '0',
        'range_end': datetime.today().strftime('%Y-%m-%d')
    }

    cookie_session = get_cookie_session(cod)

    if cookie_session is None:
        return None
    else:
        headers = {'Cookie': cookie_session}
        try:
            r = requests.get(url, params = params, headers = headers)
            json.loads(r.text)
            return r.text
        except ValueError as e:
            print('Problem with JSON load for %s. Skipping...' % cod)
            write_log(cod)
            return None

def export_raw_accesses(cod):
    ''' Export raw text containing data to a file named "cod.txt"'''
    data = get_raw_accesses(cod)
    if data is not None:
        with open('./accesses2/'+ cod + '.txt', 'w') as f:
            f.write(data)
        return 1
    else:
        return None

with open('manuscript_ids.txt', 'r') as f:
    for line in f:
        raw_access = export_raw_accesses(line.strip())
        if raw_access is not None:
            print('Stripped %s data.' % line.strip())
