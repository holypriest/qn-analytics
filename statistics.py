from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import operator

def month_interval(start, end):
    dt_start = datetime.strptime(start, '%Y-%m-%d')
    dt_end = datetime.strptime(end, '%Y-%m-%d')
    return (dt_end.year - dt_start.year) * 12 + abs(dt_end.month - dt_start.month)

def load_article(aid):
    accesses = {}
    with open('./accesses/' + aid + '.txt', 'r') as f:
        next(f)
        for line in f:
            date, html, pdf, abstract, epdf = line.strip().split('\t')
            accesses[date] = (int(html), int(pdf), int(abstract), int(epdf))
    return accesses

def total_access_per_date(aid, articles, date):
    try:
        date_access = articles[aid][date]
    except KeyError as e:
        return 0
    return sum(date_access)

def total_access_per_interval(aid, articles, end, months):
    dt_end = datetime.strptime(end, '%Y-%m-%d')
    interval_access = 0
    for i in xrange(0, months):
        date = (dt_end + relativedelta(months=-i)).strftime('%Y-%m-%d')
        interval_access += total_access_per_date(aid, articles, date)
    return interval_access

articles = {}
for article in os.listdir('./accesses'):
    articles[article[0:23]] = load_article(article[0:23])

accesses = {}
for article in articles:
    accesses[article] = total_access_per_interval(article, articles,
            '2016-04-01', 12)
print max(accesses.iteritems(), key=operator.itemgetter(1))[0]
