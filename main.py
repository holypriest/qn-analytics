import requests
import sys
from datetime import datetime
import pytz
import json

def get_data(aid):

    url1 = 'http://analytics.scielo.org/w/accesses'
    url2 = 'http://analytics.scielo.org/ajx/accesses/bymonthandyear'

    params1 = {
        'document': aid,
        'range_start':'2009-01-01',
        'range_end':'2016-05-20'
    }

    params2 = {
        'code': aid,
        'collection':'scl',
        'range_start':'2009-01-01',
        'range_end':'2016-05-20',
    }
    try:
        r = requests.get(url1, params=params1)
        cookie_session = 'session=%s' % r.cookies['session']
    except requests.exceptions.ContentDecodingError as e:
        print ('%s has a fucked up page. Skipping...' % aid)
        with open('log.txt', 'a') as f:
            f.write(aid + '\n')
        return None

    headers2 = {'Cookie': cookie_session}
    r2 = requests.get(url2, params=params2, headers=headers2)
    try:
        return json.loads(r2.text)
    except ValueError as e:
        print('%s has invalid json. Skipping...' % aid)
        with open('log.txt', 'a') as f:
            f.write(aid + '\n')
        return None

def get_access(aid, doctype):

    GMT = pytz.timezone('GMT')
    local_tz = pytz.timezone('America/Sao_Paulo')
    type_number = {'html': 0, 'pdf': 1, 'abstract': 2, 'epdf': 3}

    data = get_data(aid)
    if data is None:
        return None
    else:
        accesses = {}
        for date, nacc in data[u'options'][u'series'][type_number[doctype]][u'data']:
            date = datetime.fromtimestamp(date/1000)
            date = local_tz.localize(date)
            date = date.astimezone(GMT)
            date = date.strftime('%Y-%m-%d')
            accesses[date] = nacc
        if not accesses:
            print('Article %s not accessed yet.' % aid)
        return accesses

def export_access_matrix(aid):
    html_acc = get_access(aid, 'html')
    pdf_acc = get_access(aid, 'pdf')
    abs_acc = get_access(aid, 'abstract')
    epdf_acc = get_access(aid, 'epdf')

    if all([html_acc, pdf_acc, abs_acc, epdf_acc]):
        with open('./accesses/' + aid + '.txt', 'w') as f:
            f.write('date\thtml\tpdf\tabstract\tepdf\n')
            for date in sorted(html_acc):
                f.write('%s\t%s\t%s\t%s\t%s\n' % (date, html_acc[date],
                    pdf_acc[date], abs_acc[date], epdf_acc[date]))

with open('lacking.txt', 'r') as f:
    for line in f:
        export_access_matrix(line.strip())
        print('Stripped %s graph.' % line.strip())
