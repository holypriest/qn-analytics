import requests
from datetime import datetime
from collections import namedtuple
import pytz
import json

class Article(object):

    def __init__(self, cod):
        self.cod = cod
        self.file = cod + '.txt'
        self.year = int(cod[10:14])
        self.accesses = self.accesses()

    def raw_accesses(self):
        ''' Get all accesses in a raw format from file '''
        with open('./accesses/' + self.file, 'r') as f:
            return json.loads(f.read())

    def accesses_by_doctype(self, doctype):
        ''' Get all accesses to a specific document format '''
        type_number = {'html': 0, 'pdf': 1, 'abstract': 2, 'epdf': 3}
        GMT = pytz.timezone('GMT')
        local_tz = pytz.timezone('America/Sao_Paulo')
        data = self.raw_accesses()
        dt_accesses = {}
        for date, nacc in data[u'options'][u'series'][type_number[doctype]][u'data']:
            date = datetime.fromtimestamp(date/1000)
            date = local_tz.localize(date)
            date = date.astimezone(GMT)
            date = date.strftime('%Y-%m-%d')
            dt_accesses[date] = nacc
        return dt_accesses

    def accesses(self):
        ''' Returns accesses data in a structured way '''
        html_acc = self.accesses_by_doctype('html')
        pdf_acc = self.accesses_by_doctype('pdf')
        abs_acc = self.accesses_by_doctype('abstract')
        epdf_acc = self.accesses_by_doctype('epdf')

        accesses = {}
        acc = namedtuple('acc', 'html, pdf, abstract, epdf')
        if all([html_acc, pdf_acc, abs_acc, epdf_acc]):
            for date in sorted(html_acc):
                try:
                    accesses[date] = acc(html_acc[date], pdf_acc[date],
                        abs_acc[date], epdf_acc[date])
                except KeyError as e:
                    accesses[date] = acc(0, 0, 0, 0)
        return accesses

    def accumulated_access(self):
        ''' Returns monthly accumulated access data '''
        acc_before = 0
        acc_data = {}
        for date in sorted(self.accesses):
            acc_data[date] = sum(self.accesses[date]) + acc_before
            acc_before = acc_data[date]
        return acc_data

    def accesses_in_time_interval(self, start, end):
        ''' Returns accesses between start and end (including borders) '''
        acc_data = self.accumulated_access()
        try:
            acc_end = acc_data[end]
        except KeyError as e:
            acc_end = 0
        try:
            acc_start = acc_data[start]
        except KeyError as e:
            acc_start = 0
        try:
            return acc_end - acc_start + sum(self.accesses[start])
        except KeyError as e:
            return acc_end
