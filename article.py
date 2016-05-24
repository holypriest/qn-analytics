import requests
from datetime import datetime
from collections import namedtuple
import pytz
import json

class Article(object):

    def __init__(self, cod):
        self.cod = cod
        self.file = cod + '.txt'
        self.accesses = self.get_accesses()

    def get_raw_accesses(self):
        with open('./accesses/' + self.file, 'r') as f:
            return json.loads(f.read())

    def get_accesses_by_doctype(self, doctype):
        type_number = {'html': 0, 'pdf': 1, 'abstract': 2, 'epdf': 3}
        GMT = pytz.timezone('GMT')
        local_tz = pytz.timezone('America/Sao_Paulo')
        data = self.get_raw_accesses()
        dt_accesses = {}
        for date, nacc in data[u'options'][u'series'][type_number[doctype]][u'data']:
            date = datetime.fromtimestamp(date/1000)
            date = local_tz.localize(date)
            date = date.astimezone(GMT)
            date = date.strftime('%Y-%m-%d')
            dt_accesses[date] = nacc
        if not dt_accesses:
            print('Article %s not accessed yet.' % self.cod)
            return {}
        else:
            return dt_accesses

    def get_accesses(self):
        html_acc = self.get_accesses_by_doctype('html')
        pdf_acc = self.get_accesses_by_doctype('pdf')
        abs_acc = self.get_accesses_by_doctype('abstract')
        epdf_acc = self.get_accesses_by_doctype('epdf')

        accesses = {}
        if all([html_acc, pdf_acc, abs_acc, epdf_acc]):
            acc = namedtuple('acc', 'html, pdf, abstract, epdf')
            for date in sorted(html_acc):
                accesses[date] = acc(html_acc[date], pdf_acc[date],
                        abs_acc[date], epdf_acc[date])
        return accesses
